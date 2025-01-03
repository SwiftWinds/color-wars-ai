from game import Game
from ai import get_ai_move


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
            print(
                "Enter row (0-4) and column (0-4) separated by space, or 'u' to undo: "
            )
            move = input().strip()
            if move.lower() == "u":
                return "undo"
            row, col = map(int, move.split())
            if 0 <= row <= 4 and 0 <= col <= 4:
                return row * 5 + col
            print("Invalid coordinates. Must be between 0 and 4.")
        except ValueError:
            print("Invalid input. Please enter two numbers separated by space or 'u'.")


def main():
    print("\nColor Wars")
    print("1. Player vs Player")
    print("2. Player vs AI")
    choice = input("Select game mode (1/2): ").strip()

    game = Game()
    ai_mode = choice == "2"

    print("\nPlayer 1: Blue (+)")
    print("Player 2: Red (-)" + " (AI)" if ai_mode else "")
    print("Enter moves as 'row col' (e.g., '2 3' for row 2, column 3)")
    print("Enter 'u' to undo last move")

    while True:
        print_board(game._board)
        current_player = 1 if game.is_player_1_turn() else 2

        # Check if current player has any valid moves
        if not game.possible_next_moves():
            winner = 2 if game.is_player_1_turn() else 1
            print(f"Game over! Player {winner} wins!")
            break

        print(f"Player {current_player}'s turn")

        try:
            if ai_mode and current_player == 2:
                # AI's turn
                best_move = get_ai_move(game)
                game.play(best_move)
                row, col = best_move // 5, best_move % 5
                print(f"AI plays: {row} {col}")
            else:
                # Human's turn
                move = get_move()
                if move == "undo":
                    if game.turn_count > 0:
                        # Undo twice in AI mode to get back to human's turn
                        game.unplay()
                        if ai_mode and game.turn_count > 0:
                            game.unplay()
                    else:
                        print("Cannot undo at the start of the game!")
                    continue
                game.play(move)
        except ValueError as e:
            print(f"Invalid move: {e}")
            continue


if __name__ == "__main__":
    main()
