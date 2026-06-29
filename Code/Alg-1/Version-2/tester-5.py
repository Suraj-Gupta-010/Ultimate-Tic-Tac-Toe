import random

# ANSI colors
GREEN = '\033[92m'
BLUE = '\033[94m'
GRAY = '\033[90m'
RESET = '\033[0m'

game_win = [
[1,2,3],[4,5,6],[7,8,9],
[1,4,7],[2,5,8],[3,6,9],
[1,5,9],[3,5,7]
]

# ---------------- BOT 1 ----------------

class Bot:

    def __init__(self,w):
        self.w1 = w[0:3]
        self.w2 = w[3:7]
        self.w3 = w[7:11]
        self.moves=[[] for _ in range(9)]

    def evaluate_square(self,me,opp):
        score=0
        for win in game_win:
            if sum(x in me for x in win)==2 and sum(x in opp for x in win)==0:
                score+=self.w1[0]
            if sum(x in opp for x in win)==2 and sum(x in me for x in win)==0:
                score+=self.w1[1]
        score+=self.w1[2]
        return score

    def evaluate_send(self,target):
        score=0
        my=self.moves[target]
        opp=opponent.moves[target]

        if len(my)+len(opp)==9:
            score+=self.w2[2]
        else:
            my_score=self.evaluate_square(my,opp)
            opp_score=self.evaluate_square(opp,my)

            if my_score>opp_score:
                score+=self.w2[0]
            if my_score<opp_score:
                score+=self.w2[1]

            score+=self.w2[3]

        return score

    def best_move(self,square):
        my=self.moves[square]
        opp=opponent.moves[square]

        possible=[x for x in range(1,10) if x not in my and x not in opp]

        best=-999
        best_move=None

        for move in possible:
            score=0
            score+=self.w3[3]
            score+=self.evaluate_send(move-1)

            if score>best:
                best=score
                best_move=move

        return best_move


# ---------------- BOT 2 (5-PLY) ----------------

class DeepBot:

    def __init__(self):
        self.moves=[[] for _ in range(9)]

    def best_move(self, square):

        my=self.moves[square]
        opp=opponent.moves[square]

        possible=[x for x in range(1,10) if x not in my and x not in opp]

        best_score=-999
        best_move=None

        for i in possible:

            w1=0.5
            for c in game_win:
                if len(set(my)&set(c))==2 and not(set(opp)&set(c)) and i in c:
                    w1=1
                if len(set(opp)&set(c))==2 and not(set(my)&set(c)) and i in c:
                    w1=0.9

            self.moves[square].append(i)

            res2=[x for x in range(1,10) if x not in self.moves[i-1] and x not in opponent.moves[i-1]]

            w3_list=[]

            for j in res2:

                w3=0.5
                self.moves[i-1].append(j)

                res3=[x for x in range(1,10) if x not in self.moves[j-1] and x not in opponent.moves[j-1]]

                w4_list=[]

                for k in res3:

                    w4=0.5
                    self.moves[j-1].append(k)

                    res4=[x for x in range(1,10) if x not in self.moves[k-1] and x not in opponent.moves[k-1]]

                    w5_list=[]

                    for l in res4:
                        w5=0.5
                        w5_list.append(w5)

                    self.moves[j-1].pop()

                    if w5_list:
                        w4*=sum(w5_list)/len(w5_list)

                    w4_list.append(w4)

                self.moves[i-1].pop()

                if w4_list:
                    w3*=sum(w4_list)/len(w4_list)

                w3_list.append(w3)

            self.moves[square].pop()

            w2=sum(w3_list)/len(w3_list) if w3_list else 0.5

            score=w1*w2

            if score>best_score:
                best_score=score
                best_move=i

        return best_move


# ---------------- GAME LOGIC ----------------

def check_square(me,opp):
    for win in game_win:
        if all(x in me for x in win): return 1
        if all(x in opp for x in win): return 2
    if len(me)+len(opp)==9: return 3
    return 0


def check_global_win(bot1, bot2):
    results=[check_square(bot1.moves[i],bot2.moves[i]) for i in range(9)]

    b1=[i+1 for i,x in enumerate(results) if x==1]
    b2=[i+1 for i,x in enumerate(results) if x==2]

    for win in game_win:
        if all(x in b1 for x in win): return 1
        if all(x in b2 for x in win): return 2

    return 0


def print_board(bot1,bot2):

    symbols=[]

    for sq in range(9):
        board=[]
        for pos in range(1,10):
            if pos in bot1.moves[sq]: board.append("O")
            elif pos in bot2.moves[sq]: board.append("X")
            else: board.append(" ")
        symbols.append(board)

    results=[check_square(bot1.moves[i],bot2.moves[i]) for i in range(9)]

    horizontal="===============++===============++================="

    for big_row in range(3):

        print(horizontal)

        for small_row in range(3):

            row=""

            for big_col in range(3):

                idx=big_row*3+big_col

                color=""
                if results[idx]==1: color=GREEN
                elif results[idx]==2: color=BLUE
                elif results[idx]==3: color=GRAY

                start=small_row*3

                row+=color
                row+=" | "+symbols[idx][start]
                row+=" | "+symbols[idx][start+1]
                row+=" | "+symbols[idx][start+2]+" | "
                row+=RESET
                row+="||"

            print(row)

            if small_row<2:
                print("---------------||---------------||---------------")

    print(horizontal)

    return results


# ---------------- RUN ----------------

print("\nWeights for BOT1")
w1=[0.966,0.876,0.477,0.831,0.344,0.141,0.562,0.752,0.370,0.035,0.655]
print(w1)

print("\nBOT2 = 5-ply chaos bot")

bot1=Bot(w1)
bot2=DeepBot()

current=bot1
square=random.randint(0,8)

winner=0
global opponent

for turn in range(81):

    opponent = bot2 if current==bot1 else bot1

    move=current.best_move(square)

    if move is None:
        square=random.randint(0,8)
        continue

    current.moves[square].append(move)
    square=move-1

    winner = check_global_win(bot1,bot2)
    if winner != 0:
        break

    current = bot2 if current==bot1 else bot1


print("\nFINAL BOARD:\n")

results=print_board(bot1,bot2)

bot1_sq=results.count(1)
bot2_sq=results.count(2)
draw_sq=results.count(3)

print("GREEN -> BOT1")
print("BLUE -> BOT2")

print("\nRESULTS:\n")

print("Bot1 won",bot1_sq,"squares")
print("Bot2 won",bot2_sq,"squares")
print(draw_sq,"squares were drawn")

if winner==1:
    print("\n🏆 BOT1 WINS THE GAME")
elif winner==2:
    print("\n🏆 BOT2 WINS THE GAME")
else:
    print("\n🤝 GAME DRAW")

print("")