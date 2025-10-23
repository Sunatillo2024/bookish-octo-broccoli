# 🚀 API Endpoints - Qisqa Qo'llanma

## 📍 Base URL
```
http://localhost:8000
https://your-domain.com
```

---

## 🔐 AUTHENTICATION

### 1. Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "api_key": "demo-api-key-12345"
}
```
**Response:** `{ "access_token": "...", "token_type": "bearer", "expires_in": 1800 }`

### 2. Token Tekshirish
```http
GET /api/auth/verify
Authorization: Bearer YOUR_TOKEN
```

---

## 💰 PRICING (PUBLIC - Token siz)

### 3. Barcha Paketlar
```http
GET /api/pricing/tiers
```
**Response:** Narx paketlari ro'yxati (UZS)

### 4. Har Slide Narxi
```http
GET /api/pricing/per-slide
```
**Response:** `{ "price_per_slide": 12500, "currency": "UZS" }`

---

## 💰 PRICING (PROTECTED - Token kerak)

### 5. Narx Hisoblash (GET)
```http
GET /api/pricing/calculate?num_slides=10
Authorization: Bearer YOUR_TOKEN
```

### 6. Narx Hisoblash (POST)
```http
POST /api/pricing/estimate
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "num_slides": 15
}
```

### 7. API Key bilan Narx
```http
GET /api/pricing/calculate-with-key?num_slides=10
X-API-Key: demo-api-key-12345
```

---

## 🎨 PRESENTATIONS (Token kerak)

### 8. Presentation Yaratish
```http
POST /api/presentations
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "title": "Mavzu",
  "author": "Muallif",
  "slides": [
    {
      "type": "title",
      "title": "Sarlavha",
      "content": "Kichik matn"
    }
  ]
}
```
**Response:** `{ "task_id": "550e8400-...", "status": "pending" }`

### 9. Status Tekshirish
```http
GET /api/presentations/{task_id}
```
**Response:** 
- `pending` - Kutilmoqda
- `processing` - Ishlanmoqda  
- `completed` - Tayyor (file_url bor)
- `failed` - Xato

### 10. PDF dan Yaratish
```http
POST /api/presentations/from-pdf
Content-Type: multipart/form-data

pdf_file: [FILE]
title: "Sarlavha"
author: "Muallif"
num_slides: 10
```

---

## 📥 FILE OPERATIONS

### 11. Fayl Yuklab Olish
```http
GET /download/{file_name}
```
**Example:** `/download/550e8400-e29b-41d4-a716-446655440000.pptx`

### 12. Task O'chirish
```http
DELETE /api/task/{task_id}
```

---

## 🛠️ UTILITY

### 13. Health Check
```http
GET /health
```
**Response:** `{ "status": "healthy", "service": "presentation-generator" }`

### 14. Root Info
```http
GET /
```
**Response:** API ma'lumotlari va endpoint ro'yxati

### 15. API Documentation
```http
GET /docs
```
**Swagger UI** - Interaktiv dokumentatsiya

### 16. ReDoc
```http
GET /redoc
```
**ReDoc** - Alternativ dokumentatsiya

---

## 📋 SLIDE TURLARI

### Title Slide
```json
{
  "type": "title",
  "title": "Asosiy sarlavha",
  "content": "Kichik sarlavha"
}
```

### Content Slide
```json
{
  "type": "content",
  "title": "Slide nomi",
  "content": "To'liq matn..."
}
```

### Bullet Points
```json
{
  "type": "bullet_points",
  "title": "Ro'yxat",
  "bullet_points": ["Item 1", "Item 2", "Item 3"]
}
```

### Two Column
```json
{
  "type": "two_column",
  "title": "Taqqoslash",
  "column1": "Chap tomon",
  "column2": "O'ng tomon"
}
```

### Image Slide
```json
{
  "type": "image",
  "title": "Rasm",
  "image_url": "https://example.com/image.jpg"
}
```

---

## 🔥 QUICK START - 3 QADAM

### QADAM 1: Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key":"demo-api-key-12345"}'
```

### QADAM 2: Presentation Yaratish
```bash
curl -X POST http://localhost:8000/api/presentations \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test",
    "author": "User",
    "slides": [
      {"type": "title", "title": "Hello", "content": "World"}
    ]
  }'
```

### QADAM 3: Status va Download
```bash
# Status
curl http://localhost:8000/api/presentations/TASK_ID

# Download (link tayyor bo'lgandan keyin)
curl -O http://localhost:8000/download/FILE_NAME.pptx
```

---

## 📱 PHP MISOL

```php
<?php
// 1. Login
$ch = curl_init('http://localhost:8000/api/auth/login');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['api_key' => 'demo-api-key-12345']));
$response = curl_exec($ch);
$token = json_decode($response, true)['access_token'];

// 2. Create
$ch = curl_init('http://localhost:8000/api/presentations');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    "Authorization: Bearer $token"
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
    'title' => 'Test',
    'author' => 'PHP',
    'slides' => [
        ['type' => 'title', 'title' => 'Hello', 'content' => 'World']
    ]
]));
$response = curl_exec($ch);
$task_id = json_decode($response, true)['task_id'];

// 3. Wait & Download
sleep(10);
$ch = curl_init("http://localhost:8000/api/presentations/$task_id");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$status = json_decode(curl_exec($ch), true);

if ($status['status'] === 'completed') {
    file_put_contents('presentation.pptx', file_get_contents($status['file_url']));
    echo "✅ Tayyor: presentation.pptx\n";
}
?>
```

---

## ⚡ STATUS KODLAR

| Kod | Ma'no |
|-----|-------|
| 200 | ✅ OK |
| 201 | ✅ Created |
| 400 | ❌ Bad Request |
| 401 | 🔒 Unauthorized |
| 404 | 🔍 Not Found |
| 500 | 💥 Server Error |

---

## 💡 MUHIM ESLATMALAR

- **Token amal qilish:** 30 daqiqa
- **Maksimal slide:** 50 ta
- **Fayl saqlash:** 24 soat
- **Rate limit:** 10 so'rov/daqiqa
- **PDF max size:** 10 MB
- **Kutish vaqti:** 5-30 sekund

---

## 🧪 TEST QILISH

### Browser'da
```
http://localhost:8000/docs
```

### Terminal'da
```bash
# Health
curl http://localhost:8000/health

# Pricing
curl http://localhost:8000/api/pricing/tiers

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"api_key":"demo-api-key-12345"}'
```

---

## 📞 SUPPORT

- **Docs:** http://localhost:8000/docs
- **Telegram:** @your_username
- **Email:** support@example.com

---

**🎯 Ready to use!** Copy-paste qiling va ishlatishni boshlang!
