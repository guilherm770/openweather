from fastapi import status, HTTPException, Depends, APIRouter
from .. import models
from ..task.weatherTask import process_weather_document
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/weather",
    tags=['Weather']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def WeatherVerifier(db: Session = Depends(get_db)):
    doc = models.WeatherDocument()

    db.add(doc)
    db.commit()

    doc = db.query(models.WeatherDocument
                ).filter(models.WeatherDocument.id == doc.id).first()

    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Weather document was not found")

    process_weather_document.delay(doc.id)

    return doc.id

@router.get("/results/{id}")
def RetriveWeatherDocument(id: int, db: Session = Depends(get_db)):
    doc = db.query(models.WeatherDocument
                ).filter(models.WeatherDocument.id == id).first()
    
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Weather document with id: {id} was not found")

    return doc.status.name