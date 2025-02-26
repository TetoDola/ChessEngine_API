import os

import chess.engine
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load Env
load_dotenv()

# App Initialization
app = FastAPI(
    title="Chess Engine API",
    description="An API for an AI Chess Bot",
    version="1.0",
)

# Engine Initialization
CHESSENGINE_PATH = os.getenv("CHESSENGINE_PATH")
if not CHESSENGINE_PATH:
    raise RuntimeError("CHESSENGINE_PATH not set")

# Initialize Engine
engine = chess.engine.SimpleEngine.popen_uci(CHESSENGINE_PATH)

# Models for request and response
# Using BaseModel allows to validate incoming Json in FastAPI. :) Interesting stuff.
class MoveRequest(BaseModel):
    fen: str
    user_move: str # Required or not? For testing it might be useful to not need. Also how do i know which user's turn it is ?
    engine_elo: int = 1200
    depth: int = 15

class MoveResponse(BaseModel):
    updated_fen: str
    best_move: str
    engine_elo: int

# Move
@app.post("/move", response_model=MoveResponse)
def get_engine_move(req: MoveRequest):
    # Initialize board from FEN
    try:
        board = chess.Board(req.fen)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid FEN string")

    # User Move Req validation
    if req.user_move:
        try:
            user_move_obj = chess.Move.from_uci(req.user_move)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid move notation")

        if user_move_obj in board.legal_moves:
            board.push(user_move_obj)
        else:
            raise HTTPException(status_code=400, detail="Illegal move")

    # Engine Config
    try:
        engine.configure({"UCI_LimitStrength": True, "UCI_Elo": req.engine_elo})
    except (chess.engine.EngineError, chess.engine.EngineTerminatedError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to configure engine with ELO: {e}"
        )
    # Engine Move
    try:
        result = engine.play(board, limit=chess.engine.Limit(depth=req.depth))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine error: {e}")

    # Move Piece
    board.push(result.move)


    return MoveResponse(
        updated_fen=board.fen(),
        best_move=result.move.uci(),
        engine_elo=req.engine_elo,
    )
