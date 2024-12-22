from perfect_set import PerfectSet


class GameOverException(Exception):
    """Exception raised when the game is over (no more valid moves available)."""

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
                    if not self.player_1_territory:
                        return []
                    self.player_2_territory.add(j)
                elif old_value <= 0 and self.board[j] > 0:
                    self.player_2_territory.remove(j)
                    if not self.player_2_territory:
                        return []
                    self.player_1_territory.add(j)

                if abs(self.board[j]) >= 4:
                    to_cleanup.append(j)

            # cleanup cell and remove from territories
            self.board[i] = 0
            self.player_1_territory.remove(i)
            self.player_2_territory.remove(i)
        return to_cleanup
