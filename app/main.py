from fastapi import FastAPI
from app.api.routes import auth, tasks

app = FastAPI(
    title="TestWork0001",
    version="1.0.0",
    description="Task management service with authorization via JWT",
)

# Connecting routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
