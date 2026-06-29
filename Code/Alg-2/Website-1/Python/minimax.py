WEIGHTS = {
    # overall board
    "center_win":    1000,
    "corner_win":    700,
    "edge_win":      500,

    "center_board":  50,     # Controlling center local board
    "corner_board":  30,     # Controlling corner local boards
    "edge_board":    20,     # Controlling edge local boards

    # local board
    "two_in_row":    10,     # Two in a row in a local board (unblocked)
    "center_moves":   5,     # Center cell of a local board
    "corner_moves":   3,     # Corner cell of a local board
    "edge_moves":     1
}

game_win = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    [1,4,7],
    [2,5,8],
    [3,6,9],
    [1,5,9],
    [3,5,7]
]

def has_won(moves: list[int]) -> bool:
    moves_set = set(moves)

    for combo in game_win:
        if set(combo).issubset(moves_set):
            return True

    return False

def evaluate(nought_: dict[str, list[int]], cross_: dict[str, list[int]], player) -> int:
    nought_score: int = 0
    cross_score: int = 0

    nought_wins: list[str] = []
    cross_wins: list[str] = []

    for board in "ABCDEFGHI":
        # Local Boards Won
        if has_won(nought_[board]):
            nought_wins.append(board)
        if has_won(cross_[board]):
            cross_wins.append(board)

        # Two in a Row
        for line in game_win:
            if not board in nought_wins and not board in cross_wins:
                nought_in_line = sum(1 for cell in line if cell in nought_[board])
                cross_in_line = sum(1 for cell in line if cell in cross_[board])

                if nought_in_line == 2 and cross_in_line == 0:
                    nought_score += WEIGHTS["two_in_row"]
                if cross_in_line == 2 and nought_in_line == 0:
                    cross_score += WEIGHTS["two_in_row"]

        # Number of Moves
        for i in nought_[board]:
            if i == 5:
                nought_score += WEIGHTS["center_moves"]
            elif i in [1, 3, 7, 9]:
                nought_score += WEIGHTS["corner_moves"]
            else:
                nought_score += WEIGHTS["edge_moves"]
        for i in cross_[board]:
            if i == 5:
                cross_score += WEIGHTS["center_moves"]
            elif i in [1, 3, 7, 9]:
                cross_score += WEIGHTS["corner_moves"]
            else:
                cross_score += WEIGHTS["edge_moves"]

        # Controlling Boards
        nought_count = len(nought_[board])
        cross_count = len(cross_[board])
        if nought_count > cross_count:
            controlling = "nought"
        elif cross_count > nought_count:
            controlling = "cross"
        else:
            controlling = None

        if board == "E":
            if controlling == "nought":
                nought_score += WEIGHTS["center_board"]
            elif controlling == "cross":
                cross_score += WEIGHTS["center_board"]
        elif board in "ACGI":
            if controlling == "nought":
                nought_score += WEIGHTS["corner_board"]
            elif controlling == "cross":
                cross_score += WEIGHTS["corner_board"]
        else:
            if controlling == "nought":
                nought_score += WEIGHTS["edge_board"]
            elif controlling == "cross":
                cross_score += WEIGHTS["edge_board"]

    # Adding win scores
    for board in nought_wins:
        if board == "E":
            nought_score += WEIGHTS["center_win"]
        elif board in "ACGI":
            nought_score += WEIGHTS["corner_win"]
        else:
            nought_score += WEIGHTS["edge_win"]
    for board in cross_wins:
        if board == "E":
            cross_score += WEIGHTS["center_win"]
        elif board in "ACGI":
            cross_score += WEIGHTS["corner_win"]
        else:
            cross_score += WEIGHTS["edge_win"]

    # Returning Score
    if player == "cross":
        return cross_score - nought_score
    else:
        return nought_score - cross_score

def minimax(nought_: dict[str, list[int]], cross_: dict[str, list[int]],
            current_board: str, depth: int, alpha: float, beta: float,
            maximizing: bool, player: str) -> int:

    # Check overall win
    nought_wins = [b for b in "ABCDEFGHI" if has_won(nought_[b])]
    cross_wins = [b for b in "ABCDEFGHI" if has_won(cross_[b])]

    if has_won([ord(b) - 64 for b in nought_wins]):
        return -10000 if player == "cross" else 10000
    if has_won([ord(b) - 64 for b in cross_wins]):
        return 10000 if player == "cross" else -10000
    if depth == 0:
        return evaluate(nought_, cross_, player)

    # Generate legal moves respecting current_board rule
    def minimax_legal_moves():
        boards_to_check = []

        if current_board == "0":
            # Free choice — any unfinished board
            boards_to_check = list("ABCDEFGHI")
        else:
            boards_to_check = [current_board]

        moves = []
        for board in boards_to_check:
            if has_won(nought_[board]) or has_won(cross_[board]):
                continue
            occupied = set(nought_[board] + cross_[board])
            if len(occupied) == 9:
                continue
            for cell in range(1, 10):
                if cell not in occupied:
                    moves.append((board, cell))

        # If restricted board is finished, fall back to free choice
        if not moves and current_board != "0":
            for board in "ABCDEFGHI":
                if has_won(nought_[board]) or has_won(cross_[board]):
                    continue
                occupied = set(nought_[board] + cross_[board])
                for cell in range(1, 10):
                    if cell not in occupied:
                        moves.append((board, cell))

        return moves

    legal_moves = minimax_legal_moves()

    if not legal_moves:
        return 0  # Draw

    if maximizing:
        best = float('-inf')
        for board, cell in legal_moves:
            cross_[board].append(cell)
            # Cell played determines next board
            next_board = chr(64 + cell)
            if has_won(nought_[next_board]) or has_won(cross_[next_board]) or \
               len(nought_[next_board]) + len(cross_[next_board]) == 9:
                next_board = "0"
            score = minimax(nought_, cross_, next_board, depth - 1, alpha, beta, False, player)
            cross_[board].pop()

            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best

    else:
        best = float('inf')
        for board, cell in legal_moves:
            nought_[board].append(cell)
            next_board = chr(64 + cell)
            if has_won(nought_[next_board]) or has_won(cross_[next_board]) or \
               len(nought_[next_board]) + len(cross_[next_board]) == 9:
                next_board = "0"
            score = minimax(nought_, cross_, next_board, depth - 1, alpha, beta, True, player)
            nought_[board].pop()

            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

def get_best_move(nought_: dict[str, list[int]], cross_: dict[str, list[int]],
                  current_board: str, player: str, depth: int = 3):
    best_score = float('-inf')
    best_move = None

    # Get legal moves for the root
    boards_to_check = list("ABCDEFGHI") if current_board == "0" else [current_board]
    legal_moves = []
    for board in boards_to_check:
        if has_won(nought_[board]) or has_won(cross_[board]):
            continue
        occupied = set(nought_[board] + cross_[board])
        for cell in range(1, 10):
            if cell not in occupied:
                legal_moves.append((board, cell))

    for board, cell in legal_moves:
        if player == "cross":
            cross_[board].append(cell)
        else:
            nought_[board].append(cell)

        next_board = chr(64 + cell)
        if has_won(nought_[next_board]) or has_won(cross_[next_board]) or \
           len(nought_[next_board]) + len(cross_[next_board]) == 9:
            next_board = "0"

        score = minimax(nought_, cross_, next_board, depth - 1, float('-inf'), float('inf'),
                       player != "cross", player)

        if player == "cross":
            cross_[board].pop()
        else:
            nought_[board].pop()

        if score > best_score:
            best_score = score
            best_move = (board, cell)

    return best_move


