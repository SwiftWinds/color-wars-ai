import signal
from game import Game
from ai import get_ai_move


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException()


def nth_letter(n):
    """Convert a board position (0-24) to a letter (a-y)."""
    return chr(ord("a") + n)


def process_game(moves, time_limit=5000000):
    game = Game()

    # Play all moves except the last one
    for move in moves:
        pos = ord(move.lower()) - ord("a")
        game.play(pos)

    # Set timeout handler
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(time_limit)

    try:
        best_move = get_ai_move(game)
        signal.alarm(0)  # Disable alarm
        return nth_letter(best_move)
    except TimeoutException:
        return "TLE"
    except Exception as e:
        print(f"Error processing move: {e}")
        return "ERR"
    finally:
        signal.alarm(0)  # Ensure alarm is disabled


def main():
    with open("dataset.txt", "r") as f_in, open("predictions.txt", "w") as f_out:
        for line_num, line in enumerate(f_in):
            moves = line.strip()
            print(f"Processing game {line_num + 1}: {moves}")

            prediction = process_game(moves)
            f_out.write(f"{prediction}\n")


if __name__ == "__main__":
    main()
