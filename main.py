from fastapi import FastAPI
from activities import controller as activity_controller

app = FastAPI()

app.include_router(activity_controller.router, prefix="/activities")
