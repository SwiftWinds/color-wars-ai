import random

from perfect_set import PerfectSet


class GameOverException(Exception):
    """Exception raised when the game is over (no more valid moves available)."""

    pass


class DuplicateOutputException(Exception):
    """Exception raised when the output is a duplicate."""

    pass


dirs = (-5, 5, -1, 1)


class Game:
    def __init__(self):
        self.board = [0] * 25  # Initialize 5x5 board with zeros
        self.is_player_1_turn = True
        self.is_first_round = True
        self.player_1_territory = PerfectSet()
        self.player_2_territory = PerfectSet()

    def possible_next_moves(self):
        if self.is_player_1_turn:
            return self.player_1_territory
        return self.player_2_territory

    def play(self, move):
        if self.is_first_round:
            if self.board[move] != 0:
                raise ValueError("Invalid first round move. Cell already occupied.")
            multiplier = 1 if self.is_player_1_turn else -1
            self.board[move] = 3 * multiplier
            # Add first move to territory
            if self.is_player_1_turn:
                self.player_1_territory.add(move)
            else:
                self.player_2_territory.add(move)
            if not self.is_player_1_turn:
                self.is_first_round = False
        else:
            multiplier = 1 if self.is_player_1_turn else -1
            if self.board[move] * multiplier <= 0:
                raise ValueError("Invalid move. Either opponent's or unclaimed cell.")
            self.board[move] += multiplier
            if abs(self.board[move]) < 4:
                return
            spread_from = [move]
            while len(to_cleanup := self._do_step(spread_from)) > 0:
                spread_from = to_cleanup
        self.is_player_1_turn = not self.is_player_1_turn

    def _do_step(self, spread_from):
        to_cleanup = []
        multiplier = 1 if self.is_player_1_turn else -1

        for i in spread_from:
            # Define adjacent cell conditions
            adjacency_rules = (
                i - 5 >= 0,  # Can go up
                i + 5 < 25,  # Can go down
                i % 5 != 0,  # Can go left
                i % 5 != 4,  # Can go right
            )

            # Add valid adjacent cells to queue
            for is_valid, offset in zip(adjacency_rules, dirs):
                if not is_valid:
                    continue
                j = i + offset
                old_value = self.board[j]
                self.board[j] = (
                    self.board[j] * (1 if self.board[j] ^ multiplier >= 0 else -1)
                    + multiplier
                )

                # Update territories based on new value
                if old_value >= 0 and self.board[j] < 0:
                    self.player_1_territory.remove(j)
                    self.player_2_territory.add(j)
                elif old_value <= 0 and self.board[j] > 0:
                    self.player_2_territory.remove(j)
                    self.player_1_territory.add(j)

                if abs(self.board[j]) >= 4:
                    to_cleanup.append(j)

            # cleanup cell and remove from territories
            self.board[i] = 0
            self.player_1_territory.remove(i)
            self.player_2_territory.remove(i)
        return to_cleanup


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
