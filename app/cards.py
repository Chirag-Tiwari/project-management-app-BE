from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/columns", tags=["Cards"])

@router.get("/{column_id}/cards", response_model=List[schemas.Card])
def get_cards(column_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    column = db.query(models.ColumnModel).join(models.Board).filter(models.ColumnModel.id == column_id, models.Board.owner_id == current_user.id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return column.cards

@router.post("/{column_id}/cards", response_model=schemas.Card)
def create_card(column_id: int, card: schemas.CardCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    column = db.query(models.ColumnModel).join(models.Board).filter(models.ColumnModel.id == column_id, models.Board.owner_id == current_user.id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    # Restrict creation to Todo column
    if column.name.lower() != "todo":
        raise HTTPException(status_code=400, detail="Cards can only be created in Todo column")

    new_card = models.Card(title=card.title, description=card.description, column_id=column.id)
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

@router.put("/cards/{card_id}", response_model=schemas.Card)
def update_card(card_id: int, updated_card: schemas.CardCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    card = db.query(models.Card).join(models.ColumnModel).join(models.Board).filter(models.Card.id == card_id, models.Board.owner_id == current_user.id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    card.title = updated_card.title #type:ignore
    card.description = updated_card.description #type:ignore
    db.commit()
    db.refresh(card)
    return card

@router.delete("/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    card = db.query(models.Card).join(models.ColumnModel).join(models.Board).filter(models.Card.id == card_id, models.Board.owner_id == current_user.id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(card)
    db.commit()
    return {"detail": "Card deleted"}
