import random

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

player = []
bot = []
moves = [1,2,3,4,5,6,7,8,9]
corners = [1,3,7,9]

move_curr = ""

def player_move_func():
    player_move = int(input("Move: "))
    if player_move in player or player_move in bot:
        return "invalid"
    else:
        player.append(player_move)
        return ""


no_win = True
start = random.randint(1,2)
if start == 1:
    print(player_move_func())
    if player[0] == 5:
        bot.append(random.choice(corners))
        print(f"Bot Played {bot[-1]}")
    else:
        bot.append(5)
        print(f"Bot Played {bot[-1]}")
    print(player_move_func())
    move_curr = "bot"

else:
    bot.append(5)
    print(f"Bot Played {bot[-1]}")
    print(player_move_func())
    bot.append(random.choice([x for x in corners if x not in player]))
    print(f"Bot Played {bot[-1]}")
    move_curr = "player"


while no_win:
    for combination in random.sample(game_win, len(game_win)):
        if len([x for x in player if x in combination]) == 3:
            print("Player Wins!")
            no_win = False
            continue

    if len(player) + len(bot) == 9:
        print("Draw")
        no_win = False
        continue

    if move_curr == "player":
        print(player_move_func())
        move_curr = "bot"

    else:
        for combination in random.sample(game_win, len(game_win)):
            if len([x for x in bot if x in combination]) == 2 and not any(x in combination for x in player):
                if len([x for x in combination if x not in bot]) == 1:
                    bot.append([x for x in combination if x not in bot][0])
                    print(f"Bot Played {bot[-1]}")
                    print("Bot Wins!")
                    no_win = False
                    break

        for combination in random.sample(game_win, len(game_win)):
            if len([x for x in player if x in combination]) == 2 and not any(x in combination for x in bot):
                bot.append([x for x in combination if x not in player][0])
                print(f"Bot Played {bot[-1]}")
                move_curr = "player"
                break
        
        if move_curr == "player":
            continue

        for combination in random.sample(game_win, len(game_win)):
            if any(x in combination for x in bot) and not any(x in combination for x in player):
                if len([x for x in combination if x not in bot]) > 1:
                    bot.append(random.choice([x for x in combination if x not in bot]))
                    print(f"Bot Played {bot[-1]}")
                    move_curr = "player"
                    break
        
        if move_curr == "player":
            continue
        else:
            if no_win == True:
                bot.append([x for x in moves if x not in player and x not in bot][0])
                print(f"Bot Played {bot[-1]}")
