from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/boards", tags=["Boards"])

class BoardListResponse(BaseModel):
    data: List[schemas.Board]

@router.get("/", response_model= BoardListResponse)
def get_boards(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    boards = db.query(models.Board).filter(models.Board.owner_id == current_user.id).all()
    return {"data":boards}

@router.post("/", response_model=schemas.Board)
def create_board(board: schemas.BoardCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_board = models.Board(name=board.name,description=board.description, owner_id=current_user.id)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

@router.get("/{board_id}", response_model=schemas.Board)
def get_board(board_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board

@router.put("/{board_id}", response_model=schemas.Board)
def update_board(board_id: int, updated_board: schemas.BoardCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    board.name = updated_board.name # type:ignore
    board.description = updated_board.description # type:ignore
    db.commit()
    db.refresh(board)
    return board

@router.delete("/{board_id}")
def delete_board(board_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    db.delete(board)
    db.commit()
    return {"message": "Board deleted successfully"}
