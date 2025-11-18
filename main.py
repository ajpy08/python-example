"""FastAPI application main file."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from infrastructure.api.routers.usuario_router import router as usuario_router
from infrastructure.config.settings import settings
from infrastructure.database.init_db import init_db

# Initialize database tables (only if database is available)
# Uncomment the line below or set INIT_DB=true in .env to auto-initialize
# init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST para gestión de usuarios con Clean Architecture",
    docs_url="/docs",
    redoc_url=None,  # Disable default ReDoc to use custom endpoint below
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(usuario_router)


@app.get("/", tags=["root"])
def root() -> dict:
    """Root endpoint."""
    return {
        "message": "Usuarios API",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/redoc", include_in_schema=False)
async def redoc_html() -> HTMLResponse:
    """Custom ReDoc endpoint that injects OpenAPI schema directly to avoid CORB issues."""
    import json
    openapi_schema = app.openapi()
    schema_json = json.dumps(openapi_schema)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Usuarios API - ReDoc</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <div id="redoc-container"></div>
            <script>
                window.OPENAPI_SPEC = {schema_json};
            </script>
            <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
            <script>
                Redoc.init(window.OPENAPI_SPEC, {{
                    scrollYOffset: 0,
                    hideDownloadButton: false,
                    disableSearch: false,
                }}, document.getElementById('redoc-container'));
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

