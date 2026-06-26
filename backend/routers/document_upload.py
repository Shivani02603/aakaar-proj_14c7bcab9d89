from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from database.models import Document
from backend.services.document_upload_service import (
    upload_document_service,
    list_documents_service,
)
from database.config import get_db

router = APIRouter()

@router.post("/upload", response_model=Document, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    user_id: UUID = Depends(),  # Assuming user_id is extracted from authentication middleware
    db: Session = Depends(get_db),
):
    """
    Endpoint to upload a document.
    """
    try:
        document = await upload_document_service(file, user_id, db)
        return document
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.get("/", response_model=List[Document], status_code=status.HTTP_200_OK)
async def list_documents(
    user_id: UUID = Depends(),  # Assuming user_id is extracted from authentication middleware
    db: Session = Depends(get_db),
):
    """
    Endpoint to list all documents for a user.
    """
    try:
        documents = await list_documents_service(user_id, db)
        return documents
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )