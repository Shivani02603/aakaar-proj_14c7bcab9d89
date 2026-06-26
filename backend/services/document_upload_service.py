from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from database.models import Document
import os
import shutil
from datetime import datetime

UPLOAD_DIR = "uploads"

async def upload_document_service(file: UploadFile, user_id: UUID, db: Session) -> Document:
    """
    Service to handle document upload.
    """
    try:
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Save file to disk
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create document record in the database
        document = Document(
            id=str(UUID()),
            user_id=str(user_id),
            filename=file.filename,
            original_filename=file.filename,
            file_size=os.path.getsize(file_path),
            file_path=file_path,
            status="uploaded",
            created_at=datetime.utcnow(),
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        return document
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}",
        )

async def list_documents_service(user_id: UUID, db: Session) -> list[Document]:
    """
    Service to list all documents for a user.
    """
    try:
        documents = db.query(Document).filter(Document.user_id == str(user_id)).all()
        return documents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list documents: {str(e)}",
        )