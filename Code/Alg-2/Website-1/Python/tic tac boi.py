import pyperclip
import time
from pynput.mouse import Controller, Button
import random
from minimax import has_won, get_best_move

mouse = Controller()

last = ""
initiated = False
calibrated = False

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

calibration_code = input("Please enter the calibration code: ")

while not calibrated:
    try:
        start_temp, small_gap, big_gap = calibration_code.split(".")

        start = tuple(map(int, start_temp.split(":")))
        small_gap = int(small_gap)
        big_gap = int(big_gap)

        print(f"Calibrated.")
        print(f"Start: {start}")
        print(f"Small gap: {small_gap}")
        print(f"Big gap: {big_gap}")
        calibrated = True


    except Exception as e:
        print("Invalid calibration code")
        print(e)


print("\nRun `pythonGameplaySetup();` to begin playing.")
pyperclip.copy("pythonGameplaySetup();")
print("Copied Automatically!")

turn: str = "bot"
current_board: str = ""


boards_covered = []
player_boards = []
bot_boards = []

playable_moves = []
player_turns = {
    "A": [],
    "B": [],
    "C": [],
    "D": [],
    "E": [],
    "F": [],
    "G": [],
    "H": [],
    "I": []
}
bot_turns = {
    "A": [],
    "B": [],
    "C": [],
    "D": [],
    "E": [],
    "F": [],
    "G": [],
    "H": [],
    "I": []
}

def move_to_position(board_: str, pos: int) -> tuple[int, int]:
    board_index = ord(board_) - ord('A')

    board_x = board_index % 3
    board_y = board_index // 3

    cell_x = (pos - 1) % 3
    cell_y = (pos - 1) // 3

    board_size = 3 * small_gap

    x = start[0] + board_x * (board_size + big_gap) + cell_x * small_gap
    y = start[1] + board_y * (board_size + big_gap) + cell_y * small_gap

    return int(x), int(y)

def click_at(x, y):
    mouse.position = (x, y)
    mouse.click(Button.left, 1)

def get_available_moves(board_: str) -> list[int]:
    taken = set(player_turns[board_]) | set(bot_turns[board_])
    return [i for i in range(1, 10) if i not in taken]

while True:
    move = pyperclip.paste()
    if move == "Initiation Complete" and not initiated:
        print("\nInitiated")
        initiated = True

    if move != last and initiated and len(move) == 2:
        print("Move played:", move)
        board = move[0]
        cell = int(move[1])

        if turn == "player":
            player_turns[board].append(cell)
        else:
            bot_turns[board].append(cell)

        if turn == "bot":
            if has_won(bot_turns[board]):
                boards_covered.append(board)
                bot_boards.append(board)
        else:
            if has_won(player_turns[board]):
                boards_covered.append(board)
                player_boards.append(board)

        current_board = chr(ord('A') + cell - 1)
        if current_board in boards_covered:
            current_board = "0"

        if turn == "bot" or turn == "player":
            """ if current_board == "0":
                playable_moves = [
                    f"{board}{cell}"
                    for board in "ABCDEFGHI"
                    if board not in boards_covered
                    for cell in get_available_moves(board)
                ]
            else:
                playable_moves = [
                    f"{current_board}{cell}"
                    for cell in get_available_moves(current_board)
                ]
            play_move = random.choice(playable_moves) """
            play_move = get_best_move(bot_turns, player_turns, current_board, "nought", 7)
            pos_x, pos_y = move_to_position(play_move[0], play_move[1])
            click_at(pos_x, pos_y)



        print(turn)
        turn = "player" if turn == "bot" else "bot"
        last = move
