import os

import chess
import chess.engine
import os
from dotenv import load_dotenv

load_dotenv()

#bruhss
engine = chess.engine.SimpleEngine.popen_uci(os.getenv('CHESSENGINE_PATH'))

def initialize_board():
    board = chess.Board()
    fen = input("Enter the FEN: ")
    user_move = input("Enter your move: ")

    try:
        board = chess.Board(fen)
        print(board)
        print(board.turn)
    except Exception as error:
        print(error)

    try:
        move = chess.Move.from_uci(user_move)
        if move in board.legal_moves:
            board.push(move)
            print(board)
            return board
        else:
            print("Invalid move")
            initialize_board()
    except Exception as error:
        print(error)

def main():
    b = initialize_board()
    result = engine.play(b, chess.engine.Limit(time=0.1))
    print(f"Engine move: {result.move}")

if __name__ == "__main__":
    main()
