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

    wins_1 = []
    wins_2 = []

    # check wins
    for square in player:
        for combination in game_win:
            if len([x for x in square if x in combination]) == 3 and not any(x in combination for x in bot[player.index(square)]) and not (chr(player.index(square)+97) in invalid):
                print(f"Player Wins {chr(player.index(square)+97)}")
                invalid.append(chr(player.index(square)+97))
                player_win.append(chr(player.index(square)+97))

    for square in bot:
        for combination in game_win:
            if len([x for x in square if x in combination]) == 3 and not any(x in combination for x in player[bot.index(square)]) and not (chr(bot.index(square)+97) in invalid):
                print(f"Bot Wins {chr(bot.index(square)+97)}")
                invalid.append(chr(bot.index(square)+97))
                bot_win.append(chr(bot.index(square)+97))

    # draw boards
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

    # global win
    for combination in game_win:
        if len([x for x in wins_1 if x in combination]) == 3:
            print("Bot wins!")
            no_win = False

        elif len([x for x in wins_2 if x in combination]) == 3:
            print("Player wins!")
            no_win = False

    if len(invalid) == 9:
        print("Draw")
        break

    if move_curr == "player":
        print(player_move_func())
        continue

    # ---------------- BOT TURN ----------------

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

            # w1
            w1 = 0.5
            for c in game_win:
                if len(set(a)&set(c))==2 and not(set(b)&set(c)) and i in c:
                    w1 = 1
                    break
                if len(set(b)&set(c))==2 and not(set(a)&set(c)) and i in c:
                    w1 = 0.9
                    break

            # w2
            w2 = 0.5
            if chr(i+96) in invalid:
                w2 = 0.1

            bot[board_index].append(i)

            a_ = bot[i-1]
            b_ = player[i-1]
            res2 = list(set(moves)-set(a_)-set(b_))

            w3_list = []

            for j in res2:

                w3 = 0.5
                for c in game_win:
                    if len(set(a_)&set(c))==2 and not(set(b_)&set(c)) and j in c:
                        w3 = 0.9
                        break
                    if len(set(b_)&set(c))==2 and not(set(a_)&set(c)) and j in c:
                        w3 = 0.8
                        break

                if chr(j+96) in invalid:
                    w3 = 1

                bot[i-1].append(j)

                a__ = bot[j-1]
                b__ = player[j-1]
                res3 = list(set(moves)-set(a__)-set(b__))

                w4_list = []

                for k in res3:

                    w4 = 0.5
                    for c in game_win:
                        if len(set(a__)&set(c))==2 and not(set(b__)&set(c)) and k in c:
                            w4 = 0.9
                            break
                        if len(set(b__)&set(c))==2 and not(set(a__)&set(c)) and k in c:
                            w4 = 0.8
                            break

                    if chr(k+96) in invalid:
                        w4 = 1

                    bot[j-1].append(k)

                    a___ = bot[k-1]
                    b___ = player[k-1]
                    res4 = list(set(moves)-set(a___)-set(b___))

                    w5_list = []

                    for l in res4:

                        w5 = 0.5
                        for c in game_win:
                            if len(set(a___)&set(c))==2 and not(set(b___)&set(c)) and l in c:
                                w5 = 0.9
                                break
                            if len(set(b___)&set(c))==2 and not(set(a___)&set(c)) and l in c:
                                w5 = 0.8
                                break

                        if chr(l+96) in invalid:
                            w5 = 1

                        w5_list.append(w5)

                    bot[j-1].pop()

                    if w5_list:
                        w4 *= sum(w5_list)/len(w5_list)

                    w4_list.append(w4)

                bot[i-1].pop()

                if w4_list:
                    w3 *= sum(w4_list)/len(w4_list)

                w3_list.append(w3)

            bot[board_index].pop()

            if w3_list:
                w2 *= sum(w3_list)/len(w3_list)

            rating = w1 * w2
            rating_moves[f"{ltr}{i}"] = rating

    if not rating_moves:
        continue

    best_score = max(rating_moves.values())
    best_moves = [m for m in rating_moves if rating_moves[m]==best_score]

    center_moves = [m for m in best_moves if int(m[1:])==5]
    corner_moves = [m for m in best_moves if int(m[1:]) in corners]

    if center_moves:
        best_move = random.choice(center_moves)
    elif corner_moves:
        best_move = random.choice(corner_moves)
    else:
        best_move = random.choice(best_moves)

    bot[ord(best_move[0])-97].append(int(best_move[1:]))
    print(f"Bot played {best_move}")

    latest_move = best_move
    move_curr = "player"
    rating_moves.clear()