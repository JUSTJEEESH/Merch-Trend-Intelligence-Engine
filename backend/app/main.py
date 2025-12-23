"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .database import init_db
from .routes import phrases, patterns, trademarks, scraping, seo, export, dashboard, ideas, tools


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown."""
    # Startup
    print(f"Starting {settings.APP_NAME}...")
    init_db()
    print("Database initialized.")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Private phrase and pattern research tool for Amazon Merch on Demand",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard.router, prefix="/api", tags=["Dashboard"])
app.include_router(phrases.router, prefix="/api/phrases", tags=["Phrases"])
app.include_router(patterns.router, prefix="/api/patterns", tags=["Patterns"])
app.include_router(trademarks.router, prefix="/api/trademarks", tags=["Trademarks"])
app.include_router(scraping.router, prefix="/api/scrape", tags=["Scraping"])
app.include_router(seo.router, prefix="/api/seo", tags=["SEO"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])
app.include_router(ideas.router, prefix="/api/ideas", tags=["Ideas"])
app.include_router(tools.router, tags=["Tools"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
