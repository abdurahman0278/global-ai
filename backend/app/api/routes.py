from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.models.schemas import FormData, ComparisonResult, ComparisonResponse
from app.services.ocr_service import OCRService
from app.services.similarity_service import SimilarityService
from app.services.db_service import DatabaseService
from pathlib import Path
import json
from datetime import datetime

router = APIRouter()
ocr_service = OCRService()
similarity_service = SimilarityService()
db_service = DatabaseService()

@router.post("/compare", response_model=ComparisonResponse)
async def compare_data(
    first_name: str = Form(...),
    last_name: str = Form(...),
    nationality: str = Form(...),
    date_of_birth: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        upload_dir = Path("backend/data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        image_path = upload_dir / f"{datetime.now().timestamp()}_{image.filename}"
        with open(image_path, "wb") as f:
            content = await image.read()
            f.write(content)
        
        form_data = {
            "first_name": first_name,
            "last_name": last_name,
            "nationality": nationality,
            "date_of_birth": date_of_birth
        }
        
        raw_text = ocr_service.extract_text_from_image(str(image_path))
        extracted_data = ocr_service.parse_handwritten_data(raw_text)
        
        score, field_scores = similarity_service.calculate_similarity(form_data, extracted_data)
        
        comparison_id = await db_service.save_comparison(score, form_data, extracted_data, field_scores)
        
        result = ComparisonResult(
            id=comparison_id,
            similarity_score=score,
            form_data=FormData(**form_data),
            extracted_data=extracted_data,
            field_scores=field_scores,
            timestamp=datetime.now()
        )
        
        return ComparisonResponse(success=True, result=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history(limit: int = 10):
    try:
        history = await db_service.get_history(limit)
        
        for item in history:
            item['form_data'] = json.loads(item['form_data'])
            item['extracted_data'] = json.loads(item['extracted_data'])
            item['field_scores'] = json.loads(item['field_scores'])
        
        return {"success": True, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comparison/{comparison_id}")
async def get_comparison(comparison_id: int):
    try:
        comparison = await db_service.get_comparison(comparison_id)
        if not comparison:
            raise HTTPException(status_code=404, detail="Comparison not found")
        
        comparison['form_data'] = json.loads(comparison['form_data'])
        comparison['extracted_data'] = json.loads(comparison['extracted_data'])
        comparison['field_scores'] = json.loads(comparison['field_scores'])
        
        return {"success": True, "comparison": comparison}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

