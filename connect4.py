"""
Ricardo Leguizamon
Diego Seo
Lorenzo Cabrera


En esta tarea implementamos la busqueda con adversario con
un limite de profundidad
las funciones implementadas son: minimax, alphabeta y expectiminimax

en el conecta4, dos jugadores colocan discos en una tabla 6x7
uno por uno. los discos se colocan en la ultima fila posible colocandolos
en una columna por turno. el jugador gana si 4 de estos estan
conectados en una linea


"""



import math

def get_child_boards(player, board):

    res = []
    for c in range(board.cols):
        if board.placeable(c):
            tmp_board = board.clone()
            tmp_board.place(player, c)
            res.append((c, tmp_board))
    return res


def evaluate(player, board):

    adversary = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1

    score = [0]*5
    adv_score = [0]*5

    weights = [0, 1, 4, 16, 1000]

    seg = []
    invalid_slot = -1
    left_revolved = [
        [invalid_slot]*r + board.row(r) + \
        [invalid_slot]*(board.rows-1-r) for r in range(board.rows)
    ]
    right_revolved = [
        [invalid_slot]*(board.rows-1-r) + board.row(r) + \
        [invalid_slot]*r for r in range(board.rows)
    ]
    for r in range(board.rows):

        row = board.row(r) 
        for c in range(board.cols-3):
            seg.append(row[c:c+4])
    for c in range(board.cols):
        col = board.col(c) 
        for r in range(board.rows-3):
            seg.append(col[r:r+4])
    for c in zip(*left_revolved):
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    for c in zip(*right_revolved):
        for r in range(board.rows-3):
            seg.append(c[r:r+4])

    for s in seg:
        if invalid_slot in s:
            continue
        if adversary not in s:
            score[s.count(player)] += 1
        if player not in s:
            adv_score[s.count(adversary)] += 1
    reward = sum([s*w for s, w in zip(score, weights)])
    penalty = sum([s*w for s, w in zip(adv_score, weights)])
    value = reward - penalty
###############################################################################
    return value


def minimax(player, board, depth_limit, maxing_player=True):

    adversary = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    placement = None


       
    if depth_limit==0 or board.terminal() :
        if maxing_player==True:
            score=evaluate(player,board)
        else:
            score=evaluate(adversary,board)
    else: 
        if maxing_player==True:
            score=float("-inf")
            x=get_child_boards(player,board)
            for i in x:
                col,new_board=i
                current_placement,current_score=minimax(adversary, new_board, depth_limit-1, maxing_player=False)
                if current_score>score:
                    score=current_score
                    placement=col
               
        else:
            score=float("+inf")
            x=get_child_boards(player,board)
            for i in x:
                col,new_board=i
                current_placement,current_score=minimax(adversary, new_board, depth_limit-1, maxing_player=True)
                if current_score<score:
                    score=current_score
                    placement=col
                
            
    ##if player==board.PLAYER2:
        
        
        
###############################################################################
    return placement, score


def alphabeta(
        player, board, depth_limit,
        alpha=-math.inf, beta=math.inf, maxing_player=True):

    adversary = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    placement = None
    

    
    if depth_limit==0 or board.terminal() :
        if maxing_player==True:
            score=evaluate(player,board)
        else:
            score=evaluate(adversary,board)

    else:
        if maxing_player == True:
            score = float("-inf")
            x = get_child_boards(player, board)
            for i in x:
                col,new_board=i
                current_placement,current_score = alphabeta(adversary, new_board, depth_limit-1, alpha, beta, maxing_player=False)
                if current_score>score :
                    score=current_score
                    placement=col
                alpha=max(score,alpha)
                if alpha >= beta:
                    break
        

        else:
            score = float("+inf")
            x = get_child_boards(player, board)
            for i in x:
                col, new_board = i
                current_placement, current_score = alphabeta(adversary, new_board, depth_limit-1, alpha, beta, maxing_player=True)
                if current_score<score:
                    score=current_score
                    placement=col
                beta=min(score,beta)
                if alpha >= beta:
                    break
            
    
###############################################################################
    return placement, score


def expectimax(player, board, depth_limit, maxing_player=True):
    

    adversary = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    placement = None


    score = float("-inf")
    if depth_limit==0 or board.terminal() :
        if maxing_player==True:
            score=evaluate(player,board)
        else:
            score=evaluate(adversary,board)
    else:
        score = float("-inf")
        if maxing_player==True:
            x=get_child_boards(player,board)
            for i in x:
                col,new_board=i
                current_placement,current_score=expectimax(adversary, new_board, depth_limit-1, maxing_player=False)
                print('cs',current_score)
                
                if current_score > score:
                    score=current_score
                    placement=col


        else:
            score = 0
            print("chance nodes")
            x=get_child_boards(player,board)
            #este es el lenght de los nodos child 
            length = len(x)
            for i in x:
                col,new_board=i
                current_placement,current_score=expectimax(adversary, new_board, depth_limit-1, maxing_player=True)
                
                chance = length**-1 * current_score
                score += chance
            
###############################################################################
    return placement, score


if __name__ == "__main__":
    from utils.app import App
    import tkinter

    algs = {
        "Minimax": minimax,
        "Alpha-beta pruning": alphabeta,
        "Expectimax": expectimax
    }

    root = tkinter.Tk()
    App(algs, root)
    root.mainloop()
