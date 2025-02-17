import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\Teto\Downloads\stockfish-windows-x86-64-avx2 (1)\stockfish\stockfish-windows-x86-64-avx2.exe")
board = chess.Board()
while not board.is_game_over():
    print(board)
    if board.turn == chess.WHITE:
        print("White's turn")
        try:
            move = chess.Move.from_uci(input("Enter your move: "))
            if move in board.legal_moves:
                board.push(move)
        except Exception as e:
            print(e)
            continue
    else:
        print("Black's turn")
    result = engine.play(board, chess.engine.Limit(time=0.1))
    print(result)
    board.push(result.move)
    print(board)

engine.quit()