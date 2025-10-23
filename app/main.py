import os
from fastapi import FastAPI, BackgroundTasks, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from celery.result import AsyncResult
from typing import Optional

from app.models import PresentationRequest, PDFPresentationRequest, PresentationResponse, PresentationStatus
from app.config import settings
from app.pdf_processor import PDFProcessor
from celery_app.tasks import generate_presentation_task

# Pricing router import qilish
from app.routes.pricing import router as pricing_router

app = FastAPI(title=settings.APP_NAME)

# Pricing router ni qo'shish
app.include_router(pricing_router)

# Mount storage directory for file downloads
app.mount("/download", StaticFiles(directory=settings.STORAGE_PATH), name="download")

@app.get("/")
async def root():
    """API Root endpoint"""
    return {
        "message": "Presentation Generator API",
        "version": "1.0.0",
        "endpoints": {
            "presentations": "/api/presentations",
            "pricing": "/api/pricing",
            "docs": "/docs"
        }
    }

@app.post("/api/presentations", response_model=PresentationResponse)
async def create_presentation(request: PresentationRequest):
    """Submit a new presentation generation task"""
    # Submit task to Celery
    task = generate_presentation_task.delay(request.model_dump())

    return PresentationResponse(task_id=task.id)

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

    return PresentationResponse(task_id=task.id)

@app.get("/api/presentations/{task_id}", response_model=PresentationStatus)
async def get_presentation_status(task_id: str):
    """Get the status of a presentation generation task"""
    task_result = AsyncResult(task_id)

    if task_result.state == 'PENDING':
        return PresentationStatus(
            task_id=task_id,
            status="pending",
            message="Task is pending"
        )
    elif task_result.state == 'FAILURE':
        return PresentationStatus(
            task_id=task_id,
            status="failed",
            message=str(task_result.info.get('message', 'Unknown error'))
        )
    elif task_result.state == 'SUCCESS':
        result = task_result.get()
        return PresentationStatus(
            task_id=task_id,
            status="completed",
            file_url=result.get('file_url'),
            message=result.get('message')
        )
    else:
        return PresentationStatus(
            task_id=task_id,
            status=task_result.state.lower(),
            message="Task is in progress"
        )

@app.get("/api/download/{file_id}")
async def download_presentation(file_id: str):
    """Download a generated presentation"""
    file_path = os.path.join(settings.STORAGE_PATH, file_id)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=f"presentation_{file_id}")