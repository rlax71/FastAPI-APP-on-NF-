from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Tic Tac Toe board
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

class Move(BaseModel):
    row: int
    col: int

@app.post("/move/")
def make_move(move: Move):
    global current_player
    if move.row < 0 or move.row > 2 or move.col < 0 or move.col > 2:
        raise HTTPException(status_code=400, detail="Invalid move")
    if board[move.row][move.col] != "":
        raise HTTPException(status_code=400, detail="Cell already occupied")
    board[move.row][move.col] = current_player
    winner = check_winner()
    if winner:
        reset_board()
        return {"message": f"Player {winner} wins!"}
    if all(all(cell != "" for cell in row) for row in board):
        reset_board()
        return {"message": "It's a draw!"}
    current_player = "O" if current_player == "X" else "X"
    return {"message": "Move accepted", "board": board}

@app.get("/board/")
def get_board():
    return {"board": board}

@app.post("/reset/")
def reset_board():
    global board, current_player
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    return {"message": "Board reset", "board": board}