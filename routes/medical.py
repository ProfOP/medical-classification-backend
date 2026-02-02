from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.services.medical_summary import (
    build_medical_context,
    generate_summary_from_context
)

from backend.database import get_db
from backend.services.dependencies import get_current_user
from backend.models.user import User
from backend.models.medical_artifact import MedicalArtifact
from backend.models.medical_schemas import (
    MedicalArtifactCreate,
    MedicalArtifactResponse
)

router = APIRouter(
    prefix="/medical",
    tags=["Medical Memory"]
)


@router.post("/artifacts", response_model=MedicalArtifactResponse)
def create_artifact(
    artifact: MedicalArtifactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_artifact = MedicalArtifact(
        user_id=current_user.id,
        **artifact.model_dump()
    )

    db.add(db_artifact)
    db.commit()
    db.refresh(db_artifact)

    return db_artifact


@router.get("/artifacts", response_model=list[MedicalArtifactResponse])
def list_artifacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(MedicalArtifact)
        .filter(MedicalArtifact.user_id == current_user.id)
        .order_by(MedicalArtifact.event_date.desc().nulls_last())
        .all()
    )
@router.get("/summary")
def medical_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    artifacts = (
        db.query(MedicalArtifact)
        .filter(MedicalArtifact.user_id == current_user.id)
        .order_by(MedicalArtifact.event_date.asc().nulls_last())
        .all()
    )

    context = build_medical_context(artifacts)
    summary = generate_summary_from_context(context)

    return {
        "summary": summary,
        "context_used": context
    }

