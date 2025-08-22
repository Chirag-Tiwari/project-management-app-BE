from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/boards", tags=["Columns"])

@router.get("/{board_id}/columns", response_model=List[schemas.Column])
def get_columns(board_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board.columns

@router.post("/{board_id}/columns", response_model=schemas.Column)
def create_column(board_id: int, column: schemas.ColumnCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    new_column = models.ColumnModel(name=column.name, order=column.order, board_id=board.id)
    db.add(new_column)
    db.commit()
    db.refresh(new_column)
    return new_column

@router.put("/columns/{column_id}", response_model=schemas.Column)
def update_column(column_id: int, updated_column: schemas.ColumnCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    column = db.query(models.ColumnModel).join(models.Board).filter(models.ColumnModel.id == column_id, models.Board.owner_id == current_user.id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    column.name = updated_column.name # type:ignore
    column.order = updated_column.order # type:ignore
    db.commit()
    db.refresh(column)
    return column

@router.delete("/columns/{column_id}")
def delete_column(column_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    column = db.query(models.ColumnModel).join(models.Board).filter(models.ColumnModel.id == column_id, models.Board.owner_id == current_user.id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    db.delete(column)
    db.commit()
    return {"detail": "Column deleted"}
