# Hadith API Documentation

## Overview
The Hadith API provides endpoints to retrieve, search, and interact with the Forty Hadith Annawawi collection. All endpoints return JSON responses with a consistent structure.

## Base URL
```
http://localhost:5000/api/hadiths
```

## Response Format
All successful API responses follow this structure:
```json
{
  "status": "success",
  "data": { /* response data */ }
}
```

Error responses:
```json
{
  "status": "error",
  "message": "Error description"
}
```

---

## Endpoints

### 1. Get All Hadiths
**Endpoint:** `GET /api/hadiths`

**Description:** Retrieve all hadiths with pagination and optional filtering.

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1, min: 1)
- `per_page` (integer, optional): Results per page (default: 10, max: 50)
- `search` (string, optional): Search term to filter hadiths by text or narrator
- `hadith_number` (integer, optional): Filter by specific hadith number (1-42)

**Example Request:**
```bash
GET /api/hadiths?page=1&per_page=5&search=knowledge
```

**Example Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "hadith_number": 1,
      "arabic_text": "إنما الأعمال بالنيات...",
      "english_text": "Actions are judged by intentions...",
      "narrator": "Umar ibn Al-Khattab",
      "book_reference": "Book 15: Forty Hadith of al-Nawawi",
      "source_url": "https://sunnah.com",
      "created_at": "2026-06-03T12:00:00"
    },
    // ... more hadiths
  ],
  "pagination": {
    "current_page": 1,
    "per_page": 5,
    "total_items": 42,
    "total_pages": 9,
    "has_next": true,
    "has_prev": false,
    "next_page": 2,
    "prev_page": null
  }
}
```

**Status Code:** 200 OK

---

### 2. Get Single Hadith by ID
**Endpoint:** `GET /api/hadiths/<id>`

**Description:** Retrieve a single hadith by its database ID.

**Path Parameters:**
- `id` (integer, required): The hadith ID

**Example Request:**
```bash
GET /api/hadiths/1
```

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "hadith_number": 1,
    "arabic_text": "إنما الأعمال بالنيات...",
    "english_text": "Actions are judged by intentions...",
    "narrator": "Umar ibn Al-Khattab",
    "book_reference": "Book 15: Forty Hadith of al-Nawawi",
    "source_url": "https://sunnah.com",
    "created_at": "2026-06-03T12:00:00"
  }
}
```

**Status Codes:**
- 200 OK: Hadith found
- 404 Not Found: Hadith not found

---

### 3. Get Hadith by Number
**Endpoint:** `GET /api/hadiths/number/<hadith_number>`

**Description:** Retrieve a single hadith by its hadith number (1-42).

**Path Parameters:**
- `hadith_number` (integer, required): The hadith number (1-42)

**Example Request:**
```bash
GET /api/hadiths/number/5
```

**Example Response:**
Same as endpoint 2.

**Status Codes:**
- 200 OK: Hadith found
- 404 Not Found: Hadith not found

---

### 4. Get Random Hadith
**Endpoint:** `GET /api/hadiths/random`

**Description:** Retrieve a random hadith from the collection.

**Example Request:**
```bash
GET /api/hadiths/random
```

**Example Response:**
Same as endpoint 2.

**Status Codes:**
- 200 OK: Success
- 404 Not Found: No hadiths in database

**Use Case:** Perfect for "Hadith of the Day" or motivational displays.

---

### 5. Get Hadith Statistics
**Endpoint:** `GET /api/hadiths/stats`

**Description:** Retrieve statistics about the hadith collection.

**Example Request:**
```bash
GET /api/hadiths/stats
```

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "total_hadiths": 42,
    "min_hadith_number": 1,
    "max_hadith_number": 42,
    "narrators_count": 15
  }
}
```

**Status Codes:**
- 200 OK: Success
- 404 Not Found: No hadiths in database

---

## Search Examples

### Search by Keyword
```bash
# Search for hadiths containing "knowledge"
GET /api/hadiths?search=knowledge
```

### Search by Narrator
```bash
# Search for hadiths narrated by Abu Hurayrah
GET /api/hadiths?search=Abu%20Hurayrah
```

### Filter by Specific Hadith Number
```bash
# Get hadith number 10
GET /api/hadiths?hadith_number=10
```

### Combine Search and Pagination
```bash
# Get page 2 with 5 results per page, searching for "patience"
GET /api/hadiths?page=2&per_page=5&search=patience
```

---

## Error Handling

### Common Error Responses

**404 Not Found:**
```json
{
  "status": "error",
  "message": "Hadith with ID 999 not found"
}
```

**500 Internal Server Error:**
```json
{
  "status": "error",
  "message": "Error retrieving hadiths: [error details]"
}
```

---

## Pagination Details

The `pagination` object in responses includes:
- `current_page`: Current page number
- `per_page`: Number of results per page
- `total_items`: Total number of items matching the query
- `total_pages`: Total number of pages
- `has_next`: Boolean indicating if there's a next page
- `has_prev`: Boolean indicating if there's a previous page
- `next_page`: Next page number (null if on last page)
- `prev_page`: Previous page number (null if on first page)

---

## Rate Limiting

Currently, there is no rate limiting on the API. However, please use the API responsibly.

---

## Field Descriptions

- **id**: Unique database identifier for the hadith
- **hadith_number**: The hadith number in the Forty Hadith collection (1-42)
- **arabic_text**: The original Arabic text of the hadith
- **english_text**: English translation of the hadith
- **narrator**: The companion who narrated the hadith
- **book_reference**: Reference to the source book
- **source_url**: URL to the original source (sunnah.com)
- **created_at**: ISO 8601 timestamp of when the record was created

---

## Use Cases

### 1. Hadith of the Day
```javascript
fetch('/api/hadiths/random')
  .then(res => res.json())
  .then(data => console.log(data.data));
```

### 2. Search Functionality
```javascript
fetch('/api/hadiths?search=knowledge&per_page=10')
  .then(res => res.json())
  .then(data => console.log(data.data));
```

### 3. Retrieve Specific Hadith
```javascript
fetch('/api/hadiths/number/1')
  .then(res => res.json())
  .then(data => console.log(data.data));
```

### 4. Collection Statistics
```javascript
fetch('/api/hadiths/stats')
  .then(res => res.json())
  .then(data => console.log(`Total hadiths: ${data.data.total_hadiths}`));
```

---

## Future Enhancements

- [ ] Filter by narrator
- [ ] Sort by different fields
- [ ] Advanced search with boolean operators
- [ ] Caching for frequently accessed hadiths
- [ ] API authentication and rate limiting
- [ ] Export hadiths in different formats (CSV, PDF)
- [ ] Audio pronunciations of Arabic text
- [ ] Related hadiths suggestions

