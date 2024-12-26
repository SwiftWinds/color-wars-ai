from game import Game


def print_board(board):
    """Print the game board in a readable format."""
    print()  # Add blank line before board
    for i in range(5):
        row = board[i * 5 : (i + 1) * 5]  # Fixed slice end index
        # Convert numbers to colored text representations
        cells = []
        for value in row:
            if value > 0:
                cells.append(f"\033[94m{value:2d}\033[0m")  # Blue for player 1
            elif value < 0:
                cells.append(f"\033[91m{value:2d}\033[0m")  # Red for player 2
            else:
                cells.append(f"{value:2d}")  # No color for empty
        print(" ".join(cells))
    print()  # Add blank line after board


def get_move():
    """Get a valid move from the user."""
    while True:
        try:
            print("Enter row (0-4) and column (0-4) separated by space: ")
            row, col = map(int, input().split())
            if 0 <= row <= 4 and 0 <= col <= 4:
                return row * 5 + col
            print("Invalid coordinates. Must be between 0 and 4.")
        except ValueError:
            print("Invalid input. Please enter two numbers separated by space.")


def main():
    game = Game()

    print("\nColor Wars - Player vs Player")
    print("Player 1: Blue (+)")
    print("Player 2: Red (-)")
    print("Enter moves as 'row col' (e.g., '2 3' for row 2, column 3)")

    while True:
        print_board(game._board)
        current_player = 1 if game.is_player_1_turn() else 2

        # Check if current player has any valid moves
        if not game.possible_next_moves():
            # Current player has no moves, so the other player wins
            winner = 2 if game.is_player_1_turn() else 1
            print(f"Game over! Player {winner} wins!")
            break

        print(f"Player {current_player}'s turn")

        try:
            move = get_move()
            game.play(move)
        except ValueError as e:
            print(f"Invalid move: {e}")
            continue


if __name__ == "__main__":
    main()
