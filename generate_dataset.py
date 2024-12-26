import random

from game import Game, GameOverException


class DuplicateOutputException(Exception):
    """Exception raised when the output is a duplicate."""

    pass


def nth_letter(n):
    return chr(ord("a") + n)


def play_n_moves(n):
    if n == 0:
        return ""
    if n == 1:
        return nth_letter(random.randint(0, 24))
    game = Game()
    moves = [None] * n

    # First move (unchanged logic)
    first_move = random.randint(0, 24)
    game.play(first_move)
    moves[0] = nth_letter(first_move)

    # Second move (unchanged logic)
    second_move = random.randint(0, 23)
    if second_move >= first_move:
        second_move += 1
    game.play(second_move)
    moves[1] = nth_letter(second_move)

    for i in range(2, n):
        possible_moves = game.possible_next_moves()
        if not possible_moves:
            raise GameOverException

        # Select random move from possible moves
        move = random.choice(possible_moves)
        game.play(move)
        moves[i] = nth_letter(move)

    # Check if game is in winning state
    if not game.possible_next_moves():
        # and if so, we should not add this to the dataset
        raise GameOverException

    return "".join(moves)


outputs = set()
for i in range(6000):
    attempts = 1
    while True:
        moves = random.randint(0, 49)
        try:
            output = play_n_moves(moves)
            if output in outputs:
                raise DuplicateOutputException
        except GameOverException:
            print(f"WARN: got GameOverException on try #{attempts} ({moves} moves)")
            attempts += 1
            continue
        except DuplicateOutputException:
            print(
                f"WARN: got DuplicateOutputException on try #{attempts} ({moves} moves)"
            )
            attempts += 1
            continue
        outputs.add(output)
        break

with open("dataset.txt", "w") as f:
    for output in outputs:
        f.write(output + "\n")
