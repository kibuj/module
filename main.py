from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import Tuple, List
from Logic import *


app = FastAPI()


engine = create_engine('sqlite:///chess_game.db', echo=True)
Base = declarative_base()


class Move(Base):
    __tablename__ = 'moves'

    id = Column(Integer, primary_key=True)
    player = Column(String)
    start = Column(String)
    end = Column(String)
    game_id = Column(Integer, ForeignKey('games.id'))


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    current_player = Column(String)
    moves = relationship('Move', backref='game')

Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


class MoveRequest(BaseModel):
    player: str
    start: Tuple[int, int]
    end: Tuple[int, int]
    game_id: int

class GameResponse(BaseModel):
    id: int
    current_player: str

# Define abstract base class for chess pieces


# Initialize the game
game = Game(current_player="white")
board = Board()

# Define FastAPI routes
@app.post("/start_game/")
def start_game():
    new_game = Game(current_player="white")
    session.add(new_game)
    session.commit()
    return {"message": "Game started", "game_id": new_game.id}

@app.post("/move/")
def move(move: MoveRequest):
    game = session.query(Game).filter_by(id=move.game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.current_player != move.player:
        raise HTTPException(status_code=400, detail="It's not your turn")

    if not board.is_valid_move(move.start, move.end):
        raise HTTPException(status_code=400, detail="Invalid move")

    board.move_piece(move.start, move.end)
    game.current_player = "black" if game.current_player == "white" else "white"
    session.commit()

    return {"message": "Move made", "game_id": game.id, "current_player": game.current_player}

@app.post("/end_game/")
def end_game(game_id: int):
    game = session.query(Game).filter_by(id=game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    session.delete(game)
    session.commit()
    return {"message": "Game ended"}

@app.get("/get_board/{game_id}")
def get_board(game_id: int):
    game = session.query(Game).filter_by(id=game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    serialized_board = []
    for row in board.board:
        serialized_row = []
        for piece in row:
            serialized_row.append(piece.serialize() if piece is not None else None)
        serialized_board.append(serialized_row)

    return serialized_board

@app.get("/initial_board/")
def get_initial_board():
    initial_board = board.serialize_board()
    return initial_board


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)


