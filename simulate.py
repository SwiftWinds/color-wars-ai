# fmt: off
input = [
    0, 0, 0, 0, 0,
    0, 3, 3, 0, 0,
    0, 3, 3, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
]
# fmt: on
move = 6


def print_board():
    # print as a 5x5 grid
    for i in range(5):
        print(input[i * 5 : (i + 1) * 5])


dirs = (-5, 5, -1, 1)


def do_round(spread_from):
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
            input[j] += 1
            if input[j] >= 4:
                to_cleanup.append(j)

        # cleanup cell
        input[i] = 0
    return to_cleanup


def simulate(move):
    input[move] += 1
    if input[move] < 4:
        return
    spread_from = [move]
    while len(to_cleanup := do_round(spread_from)) > 0:
        spread_from = to_cleanup


simulate(move)
print_board()
