import random

game_win = [
    [1,2,3],[4,5,6],[7,8,9],
    [1,4,7],[2,5,8],[3,6,9],
    [1,5,9],[3,5,7]
]

player = [[], [], [], [], [], [], [], [], []]
bot = [[], [], [], [], [], [], [], [], []]
player_win = []
bot_win = []
corners = [1,3,7,9]
moves = [1,2,3,4,5,6,7,8,9]
invalid = []
no_win = True
latest_move = ""
move_curr = ""
rating_moves = {}
m_i = int()

def player_move_func():
    global latest_move, move_curr
    
    player_move = input("Move: ")
    square = int(player_move[1:])
    alphabet_pos = ord(player_move[0]) - ord('a')

    player[alphabet_pos].append(square)
    latest_move = player_move
    move_curr = "bot"
    return ""

start = random.randint(1,2)

if start == 1:
    print(player_move_func())

    if latest_move != "e5":
        index = int(latest_move[1:])-1
        letter = chr(int(latest_move[1:])+96)

        bot[index].append(5)
        latest_move = f"{letter}5"
        print(f"Bot played {letter}5")

    else:
        rand_choice = random.choice(corners)
        bot[4].append(rand_choice)
        print(f"Bot Played e{rand_choice}")
        latest_move = f"e{rand_choice}"

    print(player_move_func())

else:
    bot[4].append(5)
    print("Bot Played e5")
    latest_move = "e5"

    print(player_move_func())

    index = int(latest_move[1:])-1
    letter = chr(int(latest_move[1:])+96)

    bot[index].append(5)
    latest_move = f"{letter}5"
    print(f"Bot played {letter}5")

    move_curr = "player"

while no_win:
    if not no_win:
        break

    wins_1 = []
    wins_2 = []

    for square in player:
        for combination in random.sample(game_win, len(game_win)):
            if len([x for x in square if x in combination]) == 3 and not any(x in combination for x in bot[player.index(square)]) and not (chr(player.index(square)+97) in invalid):
                print(f"Player Wins {chr(player.index(square)+97)}")
                invalid.append(chr(player.index(square)+97))
                player_win.append(chr(player.index(square)+97))

    for square in bot:
        for combination in random.sample(game_win, len(game_win)):
            if len([x for x in square if x in combination]) == 3 and not any(x in combination for x in player[bot.index(square)]) and not (chr(bot.index(square)+97) in invalid):
                print(f"Bot Wins {chr(bot.index(square)+97)}")
                invalid.append(chr(bot.index(square)+97))
                bot_win.append(chr(bot.index(square)+97))

    for i in range(9):
        if bot[i] and player[i]:
            if len(bot[i]) + len(player[i]) == 9:
                letter = chr(i+97)
                if letter not in invalid:
                    print(f"Draw {letter}")
                    invalid.append(letter)

    for win in bot_win:
        wins_1.append(ord(win)-96)

    for win in player_win:
        wins_2.append(ord(win)-96)

    for combination in random.sample(game_win, len(game_win)):
        if len([x for x in wins_1 if x in combination]) == 3 and not any(x in combination for x in wins_2):
            print("Bot wins!")
            no_win = False
            continue

        elif len([x for x in wins_2 if x in combination]) == 3 and not any(x in combination for x in wins_1):
            print("Player wins!")
            no_win = False
            continue

    if len(invalid) == 9:
        print("Draw")
        no_win = False
        break

    if move_curr == "player":
        print(player_move_func())
        continue

    else:
        target = int(latest_move[1:]) - 1
        ltr = chr(target + 97)
        boards_to_check = []

        if ltr not in invalid:
            boards_to_check.append(target)

        else:
            for k in range(9):
                if chr(k+97) not in invalid:
                    boards_to_check.append(k)

        for board_index in boards_to_check:

            ltr = chr(board_index + 97)
            a = bot[board_index]
            b = player[board_index]
            result = list(set(moves) - set(a) - set(b))

            for i in result:

                m = []
                w_1 = 0.5

                for combination in random.sample(game_win, len(game_win)):
                    if len(set(a) & set(combination)) == 2 and not (set(b) & set(combination)) and i in combination:
                        w_1 = 1
                        break

                    if len(set(b) & set(combination)) == 2 and not (set(a) & set(combination)) and i in combination:
                        w_1 = 0.9
                        break

                w_2 = 0.5
                ltr2 = chr(int(i) + 96)

                for combination in random.sample(game_win, len(game_win)):
                    if len([x for x in player[i-1] if x in combination]) == 2 and not any(x in combination for x in bot[i-1]):
                        w_2 = 0.2
                        break

                    if len([x for x in bot[i-1] if x in combination]) == 2 and not any(x in combination for x in player[i-1]):
                        w_2 = 0.2
                        break

                if ltr2 in invalid:
                    w_2 = 0.1

                a_ = bot[int(i-1)]
                b_ = player[int(i-1)]
                result_ = list(set(moves)-set(a_)-set(b_))

                for j in result_:

                    m_i = 0.5

                    for combination in random.sample(game_win, len(game_win)):
                        if len(set(a_) & set(combination)) == 2 and not (set(b_) & set(combination)) and j in combination:
                            m_i = 0.9
                            break

                        if len(set(b_) & set(combination)) == 2 and not (set(a_) & set(combination)) and j in combination:
                            m_i = 0.8
                            break

                    ltr3 = chr(int(j) + 96)

                    if ltr3 in invalid:
                        m_i = 1

                    m.append(m_i)

                w_3 = sum(m)/len(m)
                rating = w_1*w_2*w_3
                rating_moves[f"{ltr}{i}"] = rating

        if not rating_moves:
            continue

        best_score = max(rating_moves.values())

        best_moves = [
            move for move in rating_moves
            if rating_moves[move] == best_score
        ]

        center_moves = [m for m in best_moves if int(m[1:]) == 5]
        corner_moves = [m for m in best_moves if int(m[1:]) in corners]

        if center_moves:
            best_move = random.choice(center_moves)

        elif corner_moves:
            best_move = random.choice(corner_moves)

        else:
            best_move = random.choice(best_moves)

        alphabet_pos = ord(best_move[0]) - ord('a')
        square = int(best_move[1:])

        bot[alphabet_pos].append(square)
        print(f"Bot played {best_move}")

        latest_move = best_move
        move_curr = "player"
        rating_moves.clear()