# BEGIN state
# fmt: off
input = [
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 6, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
]
# fmt: on
move = 12
is_first_round = False
is_player_one = True
# END state

# derived convenience variable
multiplier = 1 if is_player_one else -1


def print_board():
    # print as a 5x5 grid
    for i in range(5):
        print(input[i * 5 : (i + 1) * 5])


dirs = (-5, 5, -1, 1)


def do_step(spread_from):
    to_cleanup = []
    for i in spread_from:
        # Define adjacent cell conditions
        adjacency_rules = (
            i - 5 >= 0,
            i + 5 < 25,
            i % 5 != 0,
            i % 5 != 4,
        )

        # Add valid adjacent cells to queue
        for is_valid, offset in zip(adjacency_rules, dirs):
            if not is_valid:
                continue
            j = i + offset
            input[j] = input[j] * (1 if input[j] ^ multiplier >= 0 else -1) + multiplier
            if abs(input[j]) >= 4:
                to_cleanup.append(j)

        # cleanup cell
        input[i] = 0
    return to_cleanup


def simulate():
    global is_first_round, is_player_one
    if is_first_round:
        if input[move] != 0:
            raise ValueError("Invalid first round move. Cell already occupied.")
        input[move] = 3 * multiplier
        if not is_player_one:
            is_first_round = False
    else:
        if input[move] * multiplier <= 0:
            raise ValueError("Invalid move. Either opponent's or unclaimed cell.")
        input[move] += multiplier
        if abs(input[move]) < 4:
            return
        spread_from = [move] * (abs(input[move]) - 3)
        while len(to_cleanup := do_step(spread_from)) > 0:
            spread_from = to_cleanup
    is_player_one = not is_player_one


simulate()
print_board()
