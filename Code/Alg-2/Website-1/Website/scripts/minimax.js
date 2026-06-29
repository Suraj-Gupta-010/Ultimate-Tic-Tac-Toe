const game_win = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    [1,4,7],
    [2,5,8],
    [3,6,9],
    [1,5,9],
    [3,5,7]
]

const WEIGHTS = {
    center_win: 1000, corner_win: 700, edge_win: 500,
    center_board: 50, corner_board: 30, edge_board: 20,
    two_in_row: 10, center_moves: 5, corner_moves: 3, edge_moves: 1
}

function hasWon(moves) {
    return game_win.some(combo => combo.every(pos => moves.includes(pos)));
}

function evaluate(nought_, cross_, player) {
    let nought_score = 0;
    let cross_score = 0;

    const nought_wins = [];
    const cross_wins = [];

    for (const board of "ABCDEFGHI") {
        // Local Boards Won
        if (hasWon(nought_[board])) nought_wins.push(board);
        if (hasWon(cross_[board])) cross_wins.push(board);

        // Two in a Row
        for (const line of game_win) {
            if (!nought_wins.includes(board) && !cross_wins.includes(board)) {
                const nought_in_line = line.filter(cell => nought_[board].includes(cell)).length;
                const cross_in_line = line.filter(cell => cross_[board].includes(cell)).length;

                if (nought_in_line === 2 && cross_in_line === 0) nought_score += WEIGHTS.two_in_row;
                if (cross_in_line === 2 && nought_in_line === 0) cross_score += WEIGHTS.two_in_row;
            }
        }

        // Number of Moves
        for (const i of nought_[board]) {
            if (i === 5) nought_score += WEIGHTS.center_moves;
            else if ([1,3,7,9].includes(i)) nought_score += WEIGHTS.corner_moves;
            else nought_score += WEIGHTS.edge_moves;
        }
        for (const i of cross_[board]) {
            if (i === 5) cross_score += WEIGHTS.center_moves;
            else if ([1,3,7,9].includes(i)) cross_score += WEIGHTS.corner_moves;
            else cross_score += WEIGHTS.edge_moves;
        }

        // Controlling Boards
        const nought_count = nought_[board].length;
        const cross_count = cross_[board].length;
        let controlling = null;
        if (nought_count > cross_count) controlling = "nought";
        else if (cross_count > nought_count) controlling = "cross";

        if (board === "E") {
            if (controlling === "nought") nought_score += WEIGHTS.center_board;
            else if (controlling === "cross") cross_score += WEIGHTS.center_board;
        } else if ("ACGI".includes(board)) {
            if (controlling === "nought") nought_score += WEIGHTS.corner_board;
            else if (controlling === "cross") cross_score += WEIGHTS.corner_board;
        } else {
            if (controlling === "nought") nought_score += WEIGHTS.edge_board;
            else if (controlling === "cross") cross_score += WEIGHTS.edge_board;
        }
    }

    // Adding win scores
    for (const board of nought_wins) {
        if (board === "E") nought_score += WEIGHTS.center_win;
        else if ("ACGI".includes(board)) nought_score += WEIGHTS.corner_win;
        else nought_score += WEIGHTS.edge_win;
    }
    for (const board of cross_wins) {
        if (board === "E") cross_score += WEIGHTS.center_win;
        else if ("ACGI".includes(board)) cross_score += WEIGHTS.corner_win;
        else cross_score += WEIGHTS.edge_win;
    }

    // Returning Score
    return player === "cross" ? cross_score - nought_score : nought_score - cross_score;
}
