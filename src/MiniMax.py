# Algoritmo de MiniMax:
#
# Este arquivo foi implementado a partir do código de MARCEL CARACIOLO do blog:
# http://aimotion.blogspot.com.br
#
# link do algoritmo original: http://aimotion.blogspot.com.br/2009/01/aprenda-aplicar-inteligencia-artificial.html
#
######################################################################################################################

# MiniMax Algorithm:
#
# This file was implemented from the code MARCEL CARACIOLO of the blog:
# http://aimotion.blogspot.com.br
#
# Link of the original algorithm: http://aimotion.blogspot.com.br/2009/01/aprenda-aplicar-inteligencia-artificial.html


class MiniMax:

    def __init__(self, game):
        self.game = game

    def getValidMoves(self, board):
        possible_moves = list()
        for i in range(9):
            if board[i] == 0:
                possible_moves.append(i)
        return possible_moves

    def hasEnded(self, board):
        winning_rows = self.game.win
        gameover = True

        if 0 in board:
            gameover = False

        for row in winning_rows:
            row_winner = [board[x] for x in row]
            if row_winner == [1, 1, 1] or row_winner == [2, 2, 2]:
                gameover = True
                break

        return gameover

    def judge(self, board):
        winning_rows = self.game.win
        winner = None
        # (+1 Vitoria da IA, -1 Vitoria do humano, 0 Empate)
        for row in winning_rows:
            row_win = [board[x] for x in row]
            if row_win == [1, 1, 1]:
                winner = 1
                break
            elif row_win == [2, 2, 2]:
                winner = 2
                break

        if winner == 2:
            return 1
        if winner is None:
            return 0
        return -1

    def maxValue(self, board):
        if self.hasEnded(board):
            return self.judge(board)

        bestScore = -100

        for possible_move in self.getValidMoves(board):
            new_game_state = list(board)
            # CPU joga
            new_game_state[possible_move] = 2
            # Obtém o mínimo do próximo nível (MIN).
            score = self.minValue(new_game_state)
            # Pega o maior score dos piores analisados.
            if score >= bestScore:
                bestScore = score

        return bestScore

    def minValue(self, board):
        if self.hasEnded(board):
            return self.judge(board)

        bestScore = 100

        for possible_move in self.getValidMoves(board):
            new_game_state = list(board)
            # Jogador joga.
            new_game_state[possible_move] = 1
            # Obtém o máximo do proximo nivel (MAX).
            score = self.maxValue(new_game_state)
            # Pega o menor score dos melhores analisados.
            if score <= bestScore:
                bestScore = score

        return bestScore

    def decisionMinMax(self):
        move = None
        # Testa todas jogadas possiveis.
        possible_moves = self.getValidMoves(self.game.gameState)
        # Armazena a jogada que tem o melhor score.
        bestScore = -100
        # Se possui mais de uma jogada disponivel.
        if len(possible_moves) > 1:
            for possible_move in possible_moves:
                new_game_state = eval(repr(self.game.gameState))
                # Joga a IA.
                new_game_state[possible_move] = 2
                # Obtem o minimo do proximo nivel (MIN).
                score = self.minValue(new_game_state)
                # Pega o maior score dos piores analisados.
                if score >= bestScore:
                    move = possible_move
                    bestScore = score
        else:
            # Apenas uma única jogada, esta será a jogada pela IA.
            move = possible_moves[0]

        return move