# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[], player_history=[], score=[], K=4):
    # if its the start of the game
    if not prev_play:
        opponent_history.clear()
        player_history.clear()
        score.clear()
        guess = 'R'
        player_history.append(guess)
        return guess
    else:
        opponent_history.append(prev_play)
        score.append(check_winner(player_history[-1], opponent_history[-1]))
    if len(opponent_history) < K + 1:
        guess = 'R'
        player_history.append(guess)
        return guess

    moves, opp_next_pred = get_predictions(opponent_history, player_history, score, K)
    guess = fallback_fn(opp_next_pred, moves)
    player_history.append(guess)
    return guess


def get_predictions(opponent_history, player_history, score, K):
    '''
    iterate over the opponent history using a sliding window
    and compare it to last K moves
    returns two dictionaries 
    moves: considering sequences of opponent's moves equal to
    the last K moves, returns a mapping of PLAYER moves to their the count
    of their appearances after such sequences where the player has won
    opponent_predicted_move: considering sequences of opponent's moves equal to
    the last K moves, returns a mapping of OPPONENT moves to their the count
    of their appearances after such sequences
    '''
    moves = {}
    opp_next_pred = {}
    last_k_moves = opponent_history[-K:]
    for i in range(len(opponent_history) - K - 1):
        # "visible" in the sliding window
        current = opponent_history[i:i + K]
        if last_k_moves == current:
            # check what move I made and if I won
            if score[i + K] == 2:
                move_made_to_win = player_history[i + K]
                if move_made_to_win not in moves:
                    moves[move_made_to_win] = 0
                moves[move_made_to_win] += 1
            # see what move the opponent made either way
            move_opp_made = opponent_history[i + K]
            if move_opp_made not in opp_next_pred:
                opp_next_pred[move_opp_made] = 0
            opp_next_pred[move_opp_made] += 1
    return moves, opp_next_pred


def fallback_fn(opp_next_pred, historically_winning_mv, default='P'):
    '''
    a function that resolves cases where the one of the moves dicts
    is empty, and falls back to a dict of lesser importance or a
    default value
    historically_winning_mv -> opp_next_pred -> default
    '''
    if len(historically_winning_mv) < 1:
        if len(opp_next_pred) > 0:
            guess = winning_move(max(opp_next_pred, key=opp_next_pred.get))
        else:
            guess = default
    else:
        guess = max(historically_winning_mv, key=historically_winning_mv.get)
    return guess


def check_winner(player, opponent):
    if player == opponent:
        return 1
    if player == 'R':
        if opponent == 'P':
            return 0
        else:
            return 2
    elif player == 'P':
        if opponent == 'S':
            return 0
        else:
            return 2
    else:
        if opponent == 'R':
            return 0
        else:
            return 2

def winning_move(move):
    moves = {'R':'P', 'S':'R', 'P':'S'}
    return moves[move]

