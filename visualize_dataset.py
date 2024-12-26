from game import Game


def nth_position(letter):
    """Convert a letter (a-y) to a board position (0-24)."""
    return ord(letter.lower()) - ord("a")


def print_board(board):
    """Print the game board in a readable format."""
    print()  # Add blank line before board
    for i in range(5):
        row = board[i * 5 : (i + 1) * 5]
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


def simulate_moves(moves):
    """Simulate a game given a sequence of moves."""
    game = Game()

    for move in moves:
        pos = nth_position(move)
        game.play(pos)

    return game._board


def main():
    with open("dataset.txt", "r") as f:
        for line_num, line in enumerate(f):
            moves = line.strip()

            try:
                board = simulate_moves(moves)
                print(f"Game #{line_num} - Moves: {moves}")
                print_board(board)
                input("Press Enter to continue...")  # Pause between boards
            except ValueError as e:
                print(f"Error processing game #{line_num} ({moves}): {e}")
                continue


if __name__ == "__main__":
    main()
