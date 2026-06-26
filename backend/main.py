from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.auth import router as auth_router
from backend.routers.document_upload import router as document_upload_router
from ai.routes import router as ai_router
from database.config import init_db, check_db_connection

# Initialize FastAPI application
app = FastAPI(title="Aakaar Project", version="1.0.0")

# CORS Middleware
origins = [
    "http://localhost:3000",  # Frontend origin
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix='/api/auth', tags=['Auth'])
app.include_router(document_upload_router, prefix='/api/documents', tags=['Document Upload'])
app.include_router(ai_router, prefix='/api/ai', tags=['AI'])

# Application startup event
@app.on_event("startup")
async def startup_event():
    await init_db()
    check_db_connection()

# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    pass  # Add any cleanup logic if necessary