# GlobalAI - Data Comparison Platform

AI-powered platform for comparing form data with ID document images using OCR and similarity scoring.

## Features

- OCR extraction from ID documents using Tesseract
- Fuzzy string matching for similarity scoring
- Historical comparison tracking
- RESTful API with FastAPI
- Modern Next.js frontend with Tailwind CSS

## Prerequisites

- Python 3.11+
- Node.js 18+
- GPU (optional but recommended for faster OCR processing)
  - macOS: Metal-capable GPU (built-in on Apple Silicon)
  - Linux: NVIDIA GPU with CUDA
  - Windows: NVIDIA GPU with CUDA

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (this may take a few minutes for PyTorch)
pip install -r requirements.txt

# Note: On first run, EasyOCR will download English language models (~40-100MB)
# This is a one-time download and will be cached locally

# Start backend server (runs on http://localhost:8000)
uvicorn app.main:app --reload
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start frontend server (runs on http://localhost:3000)
npm run dev
```

### 3. Access the Application

Open your browser and navigate to:
- **Frontend:** http://localhost:3000
- **Backend API Docs:** http://localhost:8000/docs

## API Endpoints

### POST /api/compare
Compare form data with ID document image
- **Body:** multipart/form-data with form fields and image file
- **Returns:** Similarity score and field-by-field comparison

### GET /api/history?limit=10
Retrieve comparison history
- **Returns:** List of past comparisons

### GET /api/comparison/{id}
Get specific comparison details
- **Returns:** Complete comparison data for given ID

## Project Structure

```
globalai/
├── backend/
│   ├── app/
│   │   ├── api/routes.py       # API endpoints
│   │   ├── main.py             # FastAPI app
│   │   ├── models/schemas.py   # Data models
│   │   └── services/           # Business logic
│   │       ├── db_service.py
│   │       ├── ocr_service.py
│   │       └── similarity_service.py
│   └── requirements.txt
├── frontend/
│   ├── app/                    # Next.js App Router
│   ├── components/             # React components
│   └── lib/api.ts             # API client
└── sample-data/               # Test images
```

## Usage Example

1. Fill in the form with:
   - First Name
   - Last Name
   - Nationality
   - Date of Birth

2. Upload an ID document image (passport, driver's license, etc.)

3. Click "Compare Data" to see:
   - Overall similarity score
   - Field-by-field match percentages
   - Extracted OCR text

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Testing
Use the sample images in `sample-data/` directory for testing.

## Technology Stack

**Backend:**
- FastAPI
- EasyOCR with PyTorch (GPU-accelerated OCR)
- RapidFuzz (Fuzzy matching)
- aiosqlite (Database)

**Frontend:**
- Next.js 15
- React 19
- Tailwind CSS
- Axios

## License

MIT
