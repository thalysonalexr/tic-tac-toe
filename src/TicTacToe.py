class TicTacToe:

    def __init__(self):
        self.initAttributes()

    def initAttributes(self):
        self.win = [[0, 1, 2],  # Horizontais
                    [3, 4, 5],  #
                    [6, 7, 8],  #
                    [0, 3, 6],  # Verticais
                    [1, 4, 7],  #
                    [2, 5, 8],  #
                    [0, 4, 8],  # Diagonais
                    [2, 4, 6]]  #
        self.gameState = [0] * 9
        self.turn = 1
        self.playedp1 = list()
        self.playedp2 = list()
        self.pointsp1 = self.pointsp2 = 0
        self.winner = False

    def restart(self):
        self.gameState = [0] * 9
        self.winner = False
        self.turn = 1
        self.playedp1 = list()
        self.playedp2 = list()

    def registerPlay(self, position, player):
        if self.gameState[position] == 0:
            self.gameState[position] = self.turn
            player.append(position)
            return True
        return False

    def changeTurn(self):
        self.turn = 2 if self.turn == 1 else 1

    def checkTurn(self, position):
        if self.turn == 1:
            registered = self.registerPlay(position, self.playedp1)
            self.checkPlayer(self.playedp1)
        else:
            registered = self.registerPlay(position, self.playedp2)
            self.checkPlayer(self.playedp2)

        if not registered:
            return False
        return True

    def checkPlayer(self, player):
        if len(player) >= 3:
            if self.winCheck(player):
                self.winner = True

    def winCheck(self, played):
        for sublist in self.win:
            if all(x in played for x in sublist):
                return True
        return False
