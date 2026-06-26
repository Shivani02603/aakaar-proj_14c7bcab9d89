import os
import uuid
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    ForeignKey,
    Boolean,
    DateTime,
    JSON,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pgvector.sqlalchemy import Vector

DATABASE_URL_ENV = "DATABASE_URL"
DATABASE_URL = os.environ.get(DATABASE_URL_ENV)

Base = declarative_base()

# Database engine and session setup
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    documents = relationship("Document", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="documents")
    document_chunks = relationship("DocumentChunk", back_populates="document")
    chat_sessions = relationship("ChatSession", back_populates="document")

    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename})>"

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="document_chunks")

    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, chunk_index={self.chunk_index})>"

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="chat_sessions")
    document = relationship("Document", back_populates="chat_sessions")
    chat_messages = relationship("ChatMessage", back_populates="session")

    def __repr__(self):
        return f"<ChatSession(id={self.id}, title={self.title})>"

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    chunk_references = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship("ChatSession", back_populates="chat_messages")

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, role={self.role})>"

# Index definitions
Index("ix_documents_user_id", Document.user_id)
Index("ix_document_chunks_document_id", DocumentChunk.document_id)
Index("ix_chat_sessions_user_id", ChatSession.user_id)
Index("ix_chat_sessions_document_id", ChatSession.document_id)
Index("ix_chat_messages_session_id", ChatMessage.session_id)