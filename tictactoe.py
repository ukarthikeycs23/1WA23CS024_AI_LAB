import random

def print_board(board):
    # Print the board rows with separators
    for row in board:
        print(" | ".join(row))
        print("-" * 9) # Separator line between rows


def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

# Function to handle the player's move
def player_move(board):
    """Handles the player's input for their move and updates the board."""
    while True:
        try:
            row = int(input("Enter row (0, 1, 2): "))
            col = int(input("Enter column (0, 1, 2): "))
            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
                board[row][col] = "X" # Place player's mark
                break # Exit the loop after a valid move
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter numbers.")


def computer_move(board):
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == " ":
            board[row][col] = "O"
            break

def check_hardcoded_win(board, player):
    win_conditions = [
        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]
    for condition in win_conditions:
        if all(board[r][c] == player for r, c in condition):
            return True
    return False


def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic Tac Toe!")
    print_board(board)

    while True:
        player_move(board)
        print_board(board)
        if check_hardcoded_win(board, "X"):
            print("Congratulations! You win!")
            break
        if is_board_full(board):
            print("It's a draw!")
            break

        computer_move(board)
        print("Computer's move:")
        print_board(board)
        if check_hardcoded_win(board, "O"):
            print("Computer wins!")
            break
        if is_board_full(board):
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()
