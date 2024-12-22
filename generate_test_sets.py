import random


class GameOverException(Exception):
    """Exception raised when the game is over (no more valid moves available)."""

    pass


class Game:
    def __init__(self):
        self.board = 0
        self.is_player_1_turn = True

    def possible_next_moves(self):
        next_moves = 0
        num_moves = 0
        # make a copy of the board
        board = self.board
        if self.is_player_1_turn:
            # repeat 25 times
            for _ in range(25):
                # mask the last 3 bits
                v = board & 0x7
                if 1 <= v <= 3:
                    # shift next_moves left by 3
                    next_moves <<= 3
                    # add v to next_moves
                    next_moves |= v
                    num_moves += 1
                # shift board right by 3
                board >>= 3
        else:
            # repeat 25 times
            for _ in range(25):
                # mask the last 3 bits
                v = board & 0x7
                if v >= 5:
                    # shift next_moves left by 3
                    next_moves <<= 3
                    # add v to next_moves
                    next_moves |= v
                    num_moves += 1
                # shift board right by 3
                board >>= 3
        # shift next_moves left by 5
        next_moves <<= 5
        # add num_moves to next_moves
        next_moves |= num_moves
        return next_moves

    def play(self, move):
        self.board <<= 3
        self.board |= move
        self.is_player_1_turn = not self.is_player_1_turn


def nth_letter(n):
    return chr(ord("a") + n)


def play_n_moves(n):
    game = Game()
    # generate moves list
    moves = [None] * n
    # the first player can play anywhere on the board
    first_move = random.randint(0, 24)
    game.play(first_move)
    moves[0] = nth_letter(first_move)
    # the second player can play anywhere on the board except the first move
    second_move = random.randint(0, 23)
    if second_move >= first_move:
        second_move += 1
    game.play(second_move)
    moves[1] = nth_letter(second_move)
    for i in range(2, n):
        possible_moves = game.possible_next_moves()
        # mask the last 5 bits
        num_moves = possible_moves & 0x1F
        # shift possible_moves right by 5
        possible_moves >>= 5
        # if num_moves is 0, raise GameOverException
        if num_moves == 0:
            raise GameOverException
        # get a random move from the possible moves
        i = random.randint(0, num_moves - 1)
        # shift the board left by 3 * i
        game.board <<= 3 * i
        # mask the last 3 bits
        move = possible_moves & 0x7
        # play the move
        game.play(move)
        # add the move to the moves list
        moves[i] = nth_letter(move)
    # if the game is in a winning state, raise GameOverException
    if game.possible_next_moves() & 0x1F == 0:
        raise GameOverException
    return "".join(moves)


with open("output.txt", "w") as f:
    for i in range(6000):
        attempts = 1
        while True:
            moves = random.randint(0, 49)
            try:
                f.write(play_n_moves(moves) + "\n")
                break
            except GameOverException:
                print(f"WARN: got GameOverException on try #{attempts} ({moves} moves)")
                attempts += 1
                continue
