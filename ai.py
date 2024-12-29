from inverted_int import InvertedInt
import time

# Add global counters
positions_evaluated = 0
start_time = None


def static_eval(P, maximizing_player):
    # naively count the number of cells in each player's territory
    ours = 0
    theirs = 0
    for territory in P._player_1_territory:
        ours += P._board[territory]
    for territory in P._player_2_territory:
        theirs += -P._board[territory]
    if not maximizing_player:
        ours, theirs = theirs, ours
    eval = ours - theirs
    if eval > 0 and P.turn_count % 2 == 1 or eval < 0 and P.turn_count % 2 == 0:
        return InvertedInt(-(P.turn_count + eval))
    return InvertedInt(P.turn_count + eval)


def minimax(P, alpha, beta, depth=10, maximizing_player=True):
    """
    Recursively solve a Color Wars position using negamax variant of min-max algorithm.
    @return the score of a position
    """
    global positions_evaluated
    positions_evaluated += 1

    if not P.possible_next_moves():
        return InvertedInt(P.turn_count * (-1 if maximizing_player else 1))

    if depth <= 0:
        return static_eval(P, maximizing_player)

    if maximizing_player:
        best_score = InvertedInt(-max(P.turn_count, 1))
        for x in P.possible_next_moves():
            P.play(x)
            score = minimax(P, alpha, beta, depth - 1, False)
            P.unplay()
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = InvertedInt(P.turn_count)
        for x in P.possible_next_moves():
            P.play(x)
            score = minimax(P, alpha, beta, depth - 1, True)
            P.unplay()
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score


def get_ai_move(P):
    global positions_evaluated, start_time
    positions_evaluated = 0
    start_time = time.time()

    best_score = InvertedInt(-1) if P.turn_count % 2 == 0 else InvertedInt(0)
    best_move = None
    alpha = InvertedInt(-1)
    beta = InvertedInt(0)
    if P.turn_count % 2 == 0:
        best_score = InvertedInt(-max(P.turn_count, 1))
        for x in P.possible_next_moves():
            P.play(x)
            score = minimax(P, alpha, beta, 10, False)
            P.unplay()
            if score > best_score:
                best_score = score
                best_move = x
            alpha = max(alpha, score)
            if beta <= alpha:
                break
    else:
        best_score = InvertedInt(P.turn_count)
        for x in P.possible_next_moves():
            P.play(x)
            score = minimax(P, alpha, beta, 10, True)
            P.unplay()
            if score < best_score:
                best_score = score
                best_move = x
            beta = min(beta, score)
            if beta <= alpha:
                break

    # Calculate metrics
    end_time = time.time()
    elapsed_time = end_time - start_time
    positions_per_second = positions_evaluated / elapsed_time if elapsed_time > 0 else 0

    print(f"Time: {elapsed_time:.3f}s")
    print(f"Positions evaluated: {positions_evaluated}")
    print(f"Positions/second: {positions_per_second:.0f}")

    print(f"best_score: {best_score}")

    return best_move
