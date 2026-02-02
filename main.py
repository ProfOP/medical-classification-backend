from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from backend.models.medical_artifact import MedicalArtifact
from backend.routes.medical import router as medical_router

from backend.database import Base, engine
from backend.models.user import User
from backend.routes.users import router as users_router
from backend.routes.auth import router as auth_router


app = FastAPI(title="Medical Memory Backend")

Base.metadata.create_all(bind=engine)

app.include_router(users_router)

app.include_router(auth_router)

app.include_router(medical_router)

@app.get("/")
def root():
    return {"message": "Medical Memory Backend Running"}
