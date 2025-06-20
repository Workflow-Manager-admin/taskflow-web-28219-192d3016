from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import auth, users, tasks


# PUBLIC_INTERFACE
def get_app():
    """Create and return FastAPI app with middleware, router, and metadata setup."""
    app = FastAPI(
        title="Task Manager API",
        description=(
            "Backend API for the Task Manager application. "
            "Provides user authentication, user management, and task CRUD operations."
        ),
        version="1.0.0",
        openapi_tags=[
            {"name": "auth", "description": "Authentication & JWT"},
            {"name": "users", "description": "User management"},
            {"name": "tasks", "description": "Task management"},
        ],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(tasks.router)

    @app.get("/", tags=["root"])
    def health_check():
        """Health check endpoint. Returns a confirmation JSON to verify backend is running."""
        return {"message": "Healthy"}

    return app


app = get_app()
