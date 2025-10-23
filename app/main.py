import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from typing import Optional

from app.models import PresentationRequest, PDFPresentationRequest, PresentationResponse, PresentationStatus
from app.config import settings
from app.pdf_processor import PDFProcessor
from celery_app.tasks import generate_presentation_task

# Routers import qilish
from app.routes.pricing import router as pricing_router
from app.routes.auth import router as auth_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI-powered presentation generator with pricing and authentication",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware qo'shish (Frontend uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production da specific domain qo'ying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers ni qo'shish
app.include_router(auth_router)
app.include_router(pricing_router)

# Mount storage directory for file downloads
os.makedirs(settings.STORAGE_PATH, exist_ok=True)
app.mount("/download", StaticFiles(directory=settings.STORAGE_PATH), name="download")


def get_base_url(request: Request) -> str:
    """Get base URL from request"""
    return f"{request.url.scheme}://{request.url.netloc}"


@app.get("/")
async def root():
    """API Root endpoint"""
    return {
        "message": "Presentation Generator API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "auth": "/api/auth/login",
            "presentations": "/api/presentations",
            "pricing": "/api/pricing",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "presentation-generator",
        "version": "1.0.0"
    }


@app.post("/api/presentations", response_model=PresentationResponse)
async def create_presentation(request: PresentationRequest):
    """Submit a new presentation generation task"""
    try:
        # Submit task to Celery
        task = generate_presentation_task.delay(request.model_dump())

        return PresentationResponse(
            task_id=task.id,
            status="pending"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create presentation: {str(e)}"
        )


@app.post("/api/presentations/from-pdf", response_model=PresentationResponse)
async def create_presentation_from_pdf(
        pdf_file: UploadFile = File(...),
        title: Optional[str] = Form(None),
        author: str = Form("Generated Presentation"),
        theme: str = Form("default"),
        num_slides: int = Form(5)
):
    """Submit a presentation generation task from PDF file"""
    if not pdf_file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        # Read PDF file content
        pdf_content = await pdf_file.read()

        # Extract text from PDF
        processor = PDFProcessor()
        pdf_text = processor.extract_text_from_pdf(pdf_content)

        # Create request object
        request = PDFPresentationRequest(
            title=title or f"Presentation based on {pdf_file.filename}",
            author=author,
            theme=theme,
            num_slides=num_slides
        )

        # Submit task to Celery
        task = generate_presentation_task.delay(pdf_text, request.model_dump())

        return PresentationResponse(task_id=task.id, status="pending")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )


@app.get("/api/presentations/{task_id}", response_model=PresentationStatus)
async def get_presentation_status(task_id: str, request: Request):
    """Get the status of a presentation generation task"""
    try:
        task_result = AsyncResult(task_id)
        base_url = get_base_url(request)

        if task_result.state == 'PENDING':
            return PresentationStatus(
                task_id=task_id,
                status="pending",
                message="Task is pending"
            )
        elif task_result.state == 'FAILURE':
            error_message = str(task_result.info) if task_result.info else 'Unknown error'
            return PresentationStatus(
                task_id=task_id,
                status="failed",
                message=error_message
            )
        elif task_result.state == 'SUCCESS':
            result = task_result.get()
            file_url = result.get('file_url', '')

            # To'liq URL yaratish
            if file_url and not file_url.startswith('http'):
                file_url = f"{base_url}{file_url}"

            return PresentationStatus(
                task_id=task_id,
                status="completed",
                file_url=file_url,
                message=result.get('message', 'Presentation generated successfully')
            )
        else:
            return PresentationStatus(
                task_id=task_id,
                status=task_result.state.lower(),
                message="Task is in progress"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get task status: {str(e)}"
        )


@app.get("/api/download/{file_id}")
async def download_presentation(file_id: str):
    """Download a generated presentation"""
    file_path = os.path.join(settings.STORAGE_PATH, file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=file_id,
        media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
    )