from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    boards = relationship("Board", back_populates="owner")


class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="boards")
    columns = relationship("ColumnModel", back_populates="board", cascade="all, delete-orphan") #cascade="all, delete-orphan" This tells SQLAlchemy what to do with related objects when their parent is changed or deleted.



class ColumnModel(Base):
    __tablename__ = "columns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    order = Column(Integer, default=0)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)

    board = relationship("Board", back_populates="columns")
    cards = relationship("Card", back_populates="column", cascade="all, delete-orphan")

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    column_id = Column(Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)

    column = relationship("ColumnModel", back_populates="cards")


# User - can have many Boards.

# Board → belongs to one User and can have many Columns.

# Column → belongs to one Board and can have many Cards.

# Card → belongs to one Column.

# Cascade + back_populates:

# Deleting a User → deletes all their Boards → deletes all their Columns → deletes all their Cards.

# Deleting a Board → deletes all its Columns → deletes all their Cards.

# Removing a Column from board.columns → deletes that Column from DB.

# Removing a Card from column.cards → deletes that Card from DB.