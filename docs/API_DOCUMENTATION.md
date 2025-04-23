# 🔌 Waselni API Documentation

## Authentication

### Login
```http
POST /api/auth/login/
```

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "secure_password"
}
```

**Response:**
```json
{
    "token": "jwt_token_here",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "name": "User Name"
    }
}
```

## Trip Management

### Create Trip
```http
POST /api/trips/create/
```

**Request Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request Body:**
```json
{
    "start_location": "Tunis",
    "end_location": "Sfax",
    "departure_time": "2025-04-23T10:00:00Z",
    "available_seats": 3,
    "price_per_seat": 25.00
}
```

### Search Trips
```http
GET /api/trips/search?start=Tunis&end=Sfax&date=2025-04-23
```

## AI Services

### Sentiment Analysis
```http
POST /api/ai/analyze-sentiment/
```

**Request Body:**
```json
{
    "text": "Great ride, very comfortable!",
    "language": "en"
}
```

### Voice Recognition
```http
POST /api/ai/voice-transcribe/
```

**Request Body:**
```
multipart/form-data
file: audio_file.wav
```

## User Management

### User Profile
```http
GET /api/users/profile/
PUT /api/users/profile/
```

### User Ratings
```http
POST /api/users/rate/
```

**Request Body:**
```json
{
    "rated_user_id": 123,
    "trip_id": 456,
    "rating": 5,
    "comment": "Excellent driver!"
}
```

## Reservations

### Book Trip
```http
POST /api/reservations/create/
```

**Request Body:**
```json
{
    "trip_id": 123,
    "seats_count": 2
}
```

### Cancel Reservation
```http
DELETE /api/reservations/{reservation_id}/
```

## Complaints

### File Complaint
```http
POST /api/complaints/create/
```

**Request Body:**
```json
{
    "trip_id": 123,
    "type": "SAFETY",
    "description": "Driver was speeding",
    "evidence": "file_upload.jpg"
}
```

## Error Responses

### Common Error Codes
```json
{
    "400": "Bad Request - Invalid input",
    "401": "Unauthorized - Invalid/missing token",
    "403": "Forbidden - Insufficient permissions",
    "404": "Not Found - Resource doesn't exist",
    "500": "Internal Server Error"
}
```

## Rate Limiting

- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

## Webhook Notifications

### Trip Status Updates
```http
POST /api/webhooks/trips/
```

**Payload:**
```json
{
    "trip_id": 123,
    "status": "STARTED",
    "timestamp": "2025-04-23T10:00:00Z"
}
```

## Development Environment

### Base URL
- Development: `http://localhost:8000/api/`
- Production: `https://api.waselni.com/`

### Testing Credentials
```json
{
    "email": "test@waselni.com",
    "password": "test123"
}
```

## SDK Examples

### Python
```python
from waselni_client import WaselniAPI

api = WaselniAPI(api_key="your_api_key")
trips = api.search_trips(start="Tunis", end="Sfax")
```

### JavaScript
```javascript
const WaselniAPI = require('waselni-js');

const api = new WaselniAPI('your_api_key');
const trips = await api.searchTrips({
    start: 'Tunis',
    end: 'Sfax'
});
```