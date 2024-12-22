from collections import deque

input = [
    0, 0, 0, 0, 0,
    0, 3, 3, 0, 0,
    0, 3, 3, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
]
move = 6



def print_board():
    # print as a 5x5 grid
    for i in range(5):
        print(input[i * 5 : (i + 1) * 5])


def bfs(move):
    # Initialize queue with starting position
    q = deque([move])

    # Process all positions in queue
    while q:
        current = q.popleft()
        input[current] += 1

        if (v := input[current]) >= 4:
            input[current] = 0

            # Define adjacent cell conditions
            adjacency_rules = [
                (current - 5 >= 0, -5),  # up
                (current + 5 < 25, 5),  # down
                (current % 5 != 0, -1),  # left
                (current % 5 != 4, 1),  # right
            ]

            # Add valid adjacent cells to queue
            for is_valid, offset in adjacency_rules:
                if is_valid:
                    for _ in range(v - 3):
                        q.append(current + offset)

    return input


bfs(move)
print_board()