import random,csv
NUM_BOTS=10000
GAMES_PER_BOT=50
game_win=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
moves=[1,2,3,4,5,6,7,8,9]
bots=[]
for i in range(NUM_BOTS):
    bot={
    "id":i,
    "w1_win":random.uniform(0.85,0.99),
    "w1_block":random.uniform(0.75,0.9),
    "w1_neutral":random.uniform(0.4,0.7),
    "w2_win":random.uniform(0.7,0.95),
    "w2_lose":random.uniform(0.1,0.35),
    "w2_invalid":random.uniform(0.01,0.15),
    "w2_neutral":random.uniform(0.4,0.7),
    "w3_win":random.uniform(0.7,0.95),
    "w3_lose":random.uniform(0.2,0.4),
    "w3_invalid":random.uniform(0.01,0.2),
    "w3_neutral":random.uniform(0.4,0.7),
    "score":0
    }
    bots.append(bot)
def check_small_win(board):
    for combo in game_win:
        if len(set(board)&set(combo))==3:
            return True
    return False
def best_move(bot,player,enemy,invalid,latest):
    rating_moves={}
    target=int(latest[1:])-1
    boards=[]
    if chr(target+97) not in invalid:
        boards.append(target)
    else:
        for k in range(9):
            if chr(k+97) not in invalid:
                boards.append(k)
    for board_index in boards:
        a=player[board_index]
        b=enemy[board_index]
        result=list(set(moves)-set(a)-set(b))
        for i in result:
            w1=bot["w1_neutral"]
            for combo in game_win:
                if len(set(a)&set(combo))==2 and not set(b)&set(combo) and i in combo:
                    w1=bot["w1_win"]
                if len(set(b)&set(combo))==2 and not set(a)&set(combo) and i in combo:
                    w1=bot["w1_block"]
            ltr=chr(i+96)
            if ltr in invalid:
                w2=bot["w2_invalid"]
            else:
                if check_small_win(player[i-1]):
                    w2=bot["w2_win"]
                elif check_small_win(enemy[i-1]):
                    w2=bot["w2_lose"]
                else:
                    w2=bot["w2_neutral"]
            a2=player[i-1]
            b2=enemy[i-1]
            result2=list(set(moves)-set(a2)-set(b2))
            scores=[]
            for j in result2:
                score=bot["w3_neutral"]
                for combo in game_win:
                    if len(set(a2)&set(combo))==2 and j in combo:
                        score=bot["w3_win"]
                    if len(set(b2)&set(combo))==2 and j in combo:
                        score=bot["w3_lose"]
                if chr(j+96) in invalid:
                    score=bot["w3_invalid"]
                scores.append(score)
            if scores:
                w3=sum(scores)/len(scores)
            else:
                w3=0.5
            rating=w1*w2*w3
            move=f"{chr(board_index+97)}{i}"
            rating_moves[move]=rating
    if not rating_moves:
        return None
    best=max(rating_moves.values())
    best_moves=[m for m in rating_moves if rating_moves[m]==best]
    return random.choice(best_moves)
def play_game(bot1,bot2):
    player=[[],[],[],[],[],[],[],[],[]]
    enemy=[[],[],[],[],[],[],[],[],[]]
    invalid=[]
    player_won=[]
    enemy_won=[]
    latest="e5"
    turn=random.randint(1,2)
    for turn_count in range(81):
        if turn==1:
            move=best_move(bot1,player,enemy,invalid,latest)
            if move==None:
                break
            board=ord(move[0])-97
            sq=int(move[1:])
            player[board].append(sq)
            latest=move
            if check_small_win(player[board]):
                if move[0] not in invalid:
                    invalid.append(move[0])
                    player_won.append(ord(move[0])-96)
            turn=2
        else:
            move=best_move(bot2,enemy,player,invalid,latest)
            if move==None:
                break
            board=ord(move[0])-97
            sq=int(move[1:])
            enemy[board].append(sq)
            latest=move
            if check_small_win(enemy[board]):
                if move[0] not in invalid:
                    invalid.append(move[0])
                    enemy_won.append(ord(move[0])-96)
            turn=1
    p_sq=len(player_won)
    e_sq=len(enemy_won)
    for combo in game_win:
        if len(set(player_won)&set(combo))==3:
            return 1,p_sq,e_sq
        if len(set(enemy_won)&set(combo))==3:
            return 2,p_sq,e_sq
    if p_sq>e_sq:
        return 1,p_sq,e_sq
    if e_sq>p_sq:
        return 2,p_sq,e_sq
    return 0,p_sq,e_sq
print("TRAINING STARTED")
for i in range(NUM_BOTS):
    for j in range(GAMES_PER_BOT):
        opponent=random.randint(0,NUM_BOTS-1)
        if opponent==i:
            continue
        print("\n====================")
        print(f"Bot {i} vs Bot {opponent}")
        result,p_sq,e_sq=play_game(bots[i],bots[opponent])
        print("Squares won:",p_sq,"vs",e_sq)
        if result==1:
            bots[i]["score"]+=3
            bots[i]["score"]+=p_sq
            bots[opponent]["score"]+=e_sq
            print("WINNER:",i)
        elif result==2:
            bots[opponent]["score"]+=3
            bots[i]["score"]+=p_sq
            bots[opponent]["score"]+=e_sq
            print("WINNER:",opponent)
        else:
            bots[i]["score"]+=p_sq
            bots[opponent]["score"]+=e_sq
            print("DRAW")
print("\nTRAINING FINISHED")
bots.sort(key=lambda x:x["score"],reverse=True)
print("\nTOP 10 BOTS:")
for i in range(10):
    print(bots[i])
with open("Data/values.csv","w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["w1_win","w1_block","w1_neutral","w2_win","w2_lose","w2_invalid","w2_neutral","w3_win","w3_lose","w3_invalid","w3_neutral","score"])
    for bot in bots:
        writer.writerow([bot["w1_win"],bot["w1_block"],bot["w1_neutral"],bot["w2_win"],bot["w2_lose"],bot["w2_invalid"],bot["w2_neutral"],bot["w3_win"],bot["w3_lose"],bot["w3_invalid"],bot["w3_neutral"],bot["score"]])
print("\nvalues.csv created")