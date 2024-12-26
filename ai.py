from inverted_int import InvertedInt


def negamax(P):
    """
    Recursively solve a Color Wars position using negamax variant of min-max algorithm.
    @return the score of a position:
    - 0 for a draw game
    - positive score if you can win whatever your opponent is playing. Your score is
      1 / turn count of win (the faster you win, the higher your score)
    - negative score if your opponent can force you to lose. Your score is -1 / turn
      count of loss (the faster you lose, the lower your score).
    """
    best_score = InvertedInt(-P.turn_count)
    for x in P.possible_next_moves():
        P.play(x)
        score = -negamax(P)
        if score > best_score:
            best_score = score
        P.unplay()
    return best_score


def get_ai_move(P):
    best_score = InvertedInt(-P.turn_count)
    best_move = None
    for x in P.possible_next_moves():
        P.play(x)
        score = -negamax(P)
        P.unplay()
        if score > best_score:
            best_score = score
            best_move = x
    return best_move
