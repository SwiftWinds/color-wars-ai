from inverted_int import InvertedInt
import time

# Add global counters
positions_evaluated = 0
start_time = None


def negamax(P, alpha, beta):
    """
    Recursively solve a Color Wars position using negamax variant of min-max algorithm.
    @return the score of a position
    """
    global positions_evaluated
    positions_evaluated += 1  # Count each position evaluation

    for x in P.possible_next_moves():
        P.play(x)
        if not P.possible_next_moves():
            P.unplay()
            return InvertedInt(P.turn_count // 2 + 1)
        P.unplay()

    max_score = InvertedInt(P.turn_count // 2 + 2)
    if beta > max_score:
        beta = max_score
        if alpha >= beta:
            return beta

    for x in P.possible_next_moves():
        P.play(x)
        score = -negamax(P, -beta, -alpha)
        P.unplay()
        if score >= beta:
            return score
        if score > alpha:
            alpha = score
    return alpha


def get_ai_move(P):
    global positions_evaluated, start_time
    positions_evaluated = 0  # Reset counter
    start_time = time.time()  # Start timing

    best_score = InvertedInt(-max(P.turn_count // 2, 1))
    best_move = None
    for x in P.possible_next_moves():
        P.play(x)
        score = -negamax(
            P,
            InvertedInt(-max(P.turn_count // 2, 1)),
            InvertedInt(max(P.turn_count // 2, 1)),
        )
        P.unplay()
        if score > best_score:
            best_score = score
            best_move = x

    # Calculate metrics
    end_time = time.time()
    elapsed_time = end_time - start_time
    positions_per_second = positions_evaluated / elapsed_time if elapsed_time > 0 else 0

    print(f"Time: {elapsed_time:.3f}s")
    print(f"Positions evaluated: {positions_evaluated}")
    print(f"Positions/second: {positions_per_second:.0f}")

    return best_move
