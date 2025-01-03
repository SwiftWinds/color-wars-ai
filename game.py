from perfect_set import PerfectSet
from perfect_dict import PerfectDict
import itertools


class GameOverException(Exception):
    """Exception raised when the game is over (no more valid moves available)."""

    pass


dirs = (-5, 5, -1, 1)


def increment_turn(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.turn_count += 1
        return result

    return wrapper


def decrement_turn(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.turn_count -= 1
        return result

    return wrapper


# we start with a max undo depth of 1000 to minimize resize overhead
INITIAL_MAX_UNDO_DEPTH = 1000


class Game:
    def __init__(self):
        self._board = [0] * 25  # Initialize 5x5 board with zeros
        self._player_1_territory = PerfectSet()
        self._player_2_territory = PerfectSet()
        self._undo_board_steps = [None] * INITIAL_MAX_UNDO_DEPTH
        self.turn_count = 0  # needed to calculate score in negamax

    def possible_next_moves(self):
        if self.turn_count == 0:
            return range(25)
        if self.turn_count == 1:
            return [i for i in range(25) if self._board[i] == 0]
        if self.is_player_1_turn():
            return self._player_1_territory
        return self._player_2_territory

    @increment_turn
    def play(self, move):
        if not 0 <= move < 25:
            raise ValueError("Invalid move. Cell out of bounds.")
        if self.turn_count <= 1:  # first round
            if self._board[move] != 0:
                raise ValueError("Invalid first round move. Cell already occupied.")
            multiplier = 1 if self.is_player_1_turn() else -1
            if self.turn_count == len(self._undo_board_steps):
                print(f"WARNING: Resizing undo board steps to {self.turn_count + 1}")
                self._undo_board_steps.append(PerfectDict())
            elif self.turn_count > len(self._undo_board_steps):
                raise ValueError(
                    "Undo steps somehow exceeded max undo depth and we didn't automatically resize"
                )
            if self._undo_board_steps[self.turn_count] is not None:
                self._undo_board_steps[self.turn_count].clear()
            self._set(move, 3 * multiplier)
        else:
            multiplier = 1 if self.is_player_1_turn() else -1
            if self._board[move] * multiplier <= 0:
                raise ValueError("Invalid move. Either opponent's or unclaimed cell.")
            self._prepare_undo_board_steps()
            self._add(move, multiplier)
            if abs(self._board[move]) < 4:
                return
            spread_from = [move]
            while len(to_cleanup := self._do_step(spread_from)) > 0:
                spread_from = to_cleanup

    @decrement_turn
    def unplay(self):
        for i, old_value in self._undo_board_steps[self.turn_count - 1].items():
            self._set(i, old_value, track=False)

    def is_player_1_turn(self):
        return self.turn_count % 2 == 0

    def reset(self):
        for territory in itertools.chain(
            self._player_1_territory, self._player_2_territory
        ):
            self._set(territory, 0, track=False)
        self.turn_count = 0

    def _prepare_undo_board_steps(self):
        if self.turn_count == len(self._undo_board_steps):
            print(f"WARNING: Resizing undo board steps to {self.turn_count + 1}")
            self._undo_board_steps.append(PerfectDict())
        elif self.turn_count > len(self._undo_board_steps):
            raise ValueError(
                "Undo steps somehow exceeded max undo depth and we didn't automatically resize"
            )
        if self._undo_board_steps[self.turn_count] is not None:
            self._undo_board_steps[self.turn_count].clear()

    def _track(self, i, old_value, new_value):
        if self._undo_board_steps[self.turn_count] is None:
            self._undo_board_steps[self.turn_count] = PerfectDict()
        return_to_value = self._undo_board_steps[self.turn_count].get(i, None)

        # Case 1: No edits tracked yet (returnToValue is None)
        if return_to_value is None:
            self._undo_board_steps[self.turn_count][i] = old_value

        # Case 2: Existing edits tracked (returnToValue is not None)
        elif return_to_value == new_value:  # No longer need cache
            del self._undo_board_steps[self.turn_count][i]

    def _update_territories(self, i, old_value, new_value):
        if new_value == 0:
            self._player_1_territory.remove(i)
            self._player_2_territory.remove(i)
        elif old_value >= 0 and new_value < 0:
            self._player_1_territory.remove(i)
            self._player_2_territory.add(i)
        elif old_value <= 0 and new_value > 0:
            self._player_2_territory.remove(i)
            self._player_1_territory.add(i)

    def _set(self, i, new_value, track=True):
        old_value = self._board[i]
        if old_value == new_value:
            return
        if track:
            self._track(i, old_value, new_value)
        self._board[i] = new_value
        self._update_territories(i, old_value, new_value)

    def _add(self, i, value):
        self._set(i, self._board[i] + value)

    def _do_step(self, spread_from):
        to_cleanup = []
        multiplier = 1 if self.is_player_1_turn() else -1

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
                self._set(
                    j,
                    self._board[j] * (1 if self._board[j] ^ multiplier >= 0 else -1)
                    + multiplier,
                )
                if not self._player_1_territory or not self._player_2_territory:
                    return []

                if abs(self._board[j]) >= 4:
                    to_cleanup.append(j)

            # cleanup cell and remove from territories
            self._set(i, 0)
        return to_cleanup
