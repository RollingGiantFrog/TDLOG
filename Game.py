# -*- coding: utf-8 -*-


from random import randint
from io import *


# Difficultés
# Correspond à la profondeur de l'algorithme du minimax
# Plus la profondeur est grande, plus l'ordinateur est fort (car il voit plus loin dans la partie)
class GameDifficulty:
    EASY    = 1
    MEDIUM  = 3
    HARD    = 5
    INSANE  = 7

class GameRules:
    # Valeurs de pièce possibles
    COINS = [5,10,20,50,100,200]
    # Dictionnaire des directions possibles indexées par leur chaîne de caractère
    MOVES = {"N" : (0,-1), "S" : (0,1), "W" : (-1,0), "E" : (1,0), "NW" : (-1,-1), "NE" : (1,-1), "SW" : (-1,1), "SE" : (1,1)}


# Sert à déterminer si un caractère est un chiffre (c in numbers)
numbers = "0123456789"

# Sert dans l'algorithme du minimax
inf = 1000000000

class Grid:
    def __init__(self,size):
        self.__size = size
        # Initialise la grille avec des valeurs de pièce autorisées
        self.__grid = [[None]*size for j in range(size)]        
        
    # Setters
    @property
    def size(self):
        return self.__size
    
    # Operateurs
    def __contains__(self,coords):
        return coords[0] >= 0 and coords[0] < self.__size and coords[1] >= 0 and coords[1] < self.__size
    
    def __getitem__(self,coords):
        return self.__grid[coords[0]][coords[1]]
        
    def __setitem__(self,coords,value):
        self.__grid[coords[0]][coords[1]] = value
        
    def __str__(self):
        s = "_"*6*self.__size + "\n"
        delimiter = "_"*5 + "|"
        
        for i in range(self.__size):
            
            s = s + "|"            
            
            for j in range(self.__size):
                val = str(self[(j,i)])
                
                # On aligne les colonnes
                nbSpaces = 4-len(val)
                
                s = s + " "*nbSpaces + val + " |"
                
            s = s + "\n" + "|" + delimiter*self.__size + "\n"
        return s
    
class NotSquareGridError(Exception): pass

def LoadGrid(csvFile):
    with open(csvFile,"r") as f:
        # On lit les lignes et on sépare les valeurs de chaque lignes
        lines = [line.split(";") for line in f]
        
        # On teste la taille de la grille (grille carrée)
        size = len(lines)
        for line in lines:
            if len(line) != size:
                raise NotSquareGridError
        
        # On convertit ces valeurs en données entières
        for line in lines:
            line[len(line)-1] = line[len(line)-1].replace("\n","")
        grid = [[int(value) for value in line] for line in lines]
        
        # On créé la grille et on charge les valeurs
        G = Grid(size)
        for i in range(size):
            for j in range(size):
                G[(i,j)] = grid[j][i]
                
        return G
        

class Player:
    def __init__(self,name):
        self.__name = name
        self.__score = 0
    
    # Setters and modifiers
    @property
    def name(self):
        return self.__name
    
    @property
    def score(self):
        return self.__score
        
    def addScore(self,v):
        self.__score += v
        
    def __str__(self):
        return self.__name + " : " + str(self.__score)


class MoveException(Exception):
    def __init__(self,msg):
        self.msg = msg
        
    def __str__(self):
        return "Mouvement non autorisé : " + self.msg


class Game:
    # gridData contient les données de la grille
    # Il peut prendre la forme d'une taille de grille ou directement d'une grille
    def __init__(self,gridData,playersData):
        # On teste si gridData correspond à une taille
        if type(gridData) == int:
            size = gridData
            assert (size % 2 == 1)
            self.__size = size
            self.__grid = Grid(size)
            nbCoins = len(GameRules.COINS)
            for i in range(size):
                for j in range(size):
                    self.__grid[(i,j)] = GameRules.COINS[randint(0,nbCoins-1)]
        else:
            size = gridData.size            
            assert (size % 2 == 1)
            self.__size = size
            
            # On vérifie que les valeurs de la grille sont autorisées
            for i in range(size):
                for j in range(size):
                    assert(gridData[(i,j)] in GameRules.COINS or gridData[(i,j)] == 0)

            self.__grid = gridData
        
        # players contient la liste des joueurs
        # botValue contient la liste des difficultés (0 pour un joueur humain)
        self.__players = []
        self.__botValue = []
        k = 1
        for playerData in playersData:
            if type(playerData) == str or type(playerData) == unicode:
                self.__players += [Player(playerData)]
                self.__botValue += [0]
            elif type(playerData) == int:
                self.__players += [Player(self.computerName(k))]
                self.__botValue += [playerData]
                k += 1
                
        self.__currentPlayerIndex = 0
        # moves contiendra la pile des coups joués
        self.__moves = []
            
        # Initialisation du personnage au centre de la grille
        self.__currentPos = (size/2,size/2)
        self.__grid[self.__currentPos] = self.characterValue
            
    
    @property
    def players(self):
        return self.__players[:]
    
    @property
    def currentPlayer(self):
        return self.__players[self.__currentPlayerIndex]
    
    @property
    def characterValue(self):
        return "###"
    
    @property
    def currentPos(self):
        return self.__currentPos    
    
    @property
    def size(self):
        return self.__size
    
    def __getitem__(self,coords):
        return self.__grid[coords]
        
        
    def playerRanks(self):
        listPlayers = [[p.score,p] for p in self.__players]
        listPlayers.sort(reverse=True)
        
        # Variable qui compte l'ordre du joueur
        k = 1
            
        # On renvoit les joueurs dans l'ordre de victoire
        # On gère le cas où des joueurs ont le même score
        listPlayers[0] += [k]
        prevScore = listPlayers[0][0]
        for p in listPlayers[1:]:
            if p[0] < prevScore:
                k += 1
            prevScore = p[0]
            p += [k]
            
        return listPlayers
                
    # Teste si la partie est finie (on regarde si chaque voisin est supérieur à 0)
    def isOver(self):
        for i in range(-1,2):
            for j in range(-1,2):
                coords = (self.__currentPos[0]+i,self.__currentPos[1]+j)
                if coords in self.__grid and self.__grid[coords] != self.characterValue and self.__grid[coords] > 0:
                    return False
        return True

    def __str__(self):
        # On distingue les cas où la partie est finie ou ne l'est pas
        if not self.isOver():
            # On affiche la grille
            s = str(self.__grid)
            
            # On affiche les joueurs
            for p in self.__players:
                s = s + "\n\n" + str(p)
                if self.currentPlayer == p:
                    s = s + "\n" + "(Joueur actuel)"
        else:
            s = str(self.__grid)
            s = s + "\nLa partie est terminée"
            
            # On trie les joueurs par ordre de score décroissant (ordre de victoire)
            listPlayers = [(p.score,p) for p in self.__players]
            listPlayers.sort(reverse=True)
            
            highestScore = listPlayers[0][0]
            listWinners = [player[1].name for player in listPlayers if player[0] == highestScore]
            if len(listWinners) == 1:            
                s = s + "\n\n" + "Le vainqueur est " + listPlayers[0][1].name 
            else:
                s += "\n\n" + "Les vainqueurs sont "
                s += ", ".join(listWinners)
            
            # Variable qui compte l'ordre du joueur
            k = 1
            
            # On affiche les joueurs dans l'ordre de victoire
            # On gère le cas où des joueurs ont le même score
            s = s + "\n\n" + str(listPlayers[0][1]) + " ({}e)".format(k)
            prevScore = listPlayers[0][0]
            for p in listPlayers[1:]:
                if p[0] < prevScore:
                    k += 1
                prevScore = p[0]
                s = s + "\n\n" + str(p[1]) + " ({}e)".format(k)
                
        return s + "\n"
    
    def isComputerTurn(self):
        return self.__botValue[self.__currentPlayerIndex] > 0
    
    def nextPlayerIndex(self,index):
        return (index + 1) % (len(self.__players))
        
    # Prend en paramètre la position absolue où l'on veut aller
    # On teste si la nouvelle position est valide
    # Pour chaque type d'erreur on affiche un message correspondant
    # Renvoit True si le mouvement est autorisé et False sinon
    def isMoveValid(self,newPos):
        """if type(newPos) != tuple or len(newPos) != 2:
            raise MoveException("L'information entrée n'est pas correcte")
        elif not newPos in self.__grid:
            raise MoveException("La position demandée est en dehors de la grille")
        elif abs(newPos[0]-self.__currentPos[0]) > 1 or abs(newPos[1]-self.__currentPos[1]) > 1:
            raise MoveException("La position demandée est trop loin du personnage")
        elif self.__grid[newPos] == self.characterValue:
            raise MoveException("Vous êtes actuellement sur cette case")
        elif self.__grid[newPos] <= 0:
            raise MoveException("Vous êtes déjà passé sur cette case")
        else:
            return True
        """
        if type(newPos) != tuple or len(newPos) != 2:
            return False
        elif not newPos in self.__grid:
            return False
        elif abs(newPos[0]-self.__currentPos[0]) > 1 or abs(newPos[1]-self.__currentPos[1]) > 1:
            return False
        elif self.__grid[newPos] == self.characterValue:
            return False
        elif self.__grid[newPos] <= 0:
            return False
        else:
            return True
        
        
    # Permet de faire un mouvement sans vérification au préalable
    def move(self,newPos):
        self.currentPlayer.addScore(self.__grid[newPos])
                            
        # On empile le mouvement à la "pile" des mouvements
        self.__moves.append((self.__grid[newPos],self.__currentPos))
        self.__grid[newPos] = self.characterValue
        self.__grid[self.__currentPos] = 0
        self.__currentPos = newPos
        self.__currentPlayerIndex = self.nextPlayerIndex(self.__currentPlayerIndex)
    
    
    # Vérifie si un mouvement est valide et s'il l'est, il l'applique
    # Sinon affiche un message et renvoit Faux
    def validMove(self,newPos):
        try:
            if self.isMoveValid(newPos):
                self.move(newPos)
                return True
        except MoveException as err:
            print(err)
            return False
            
        
    
    # Annule la dernière action effectuée, peut être répété jusqu'à l'initialisation du jeu
    def undo(self):
        if len(self.__moves) > 0:
            move = self.__moves.pop()
            self.__currentPlayerIndex = (self.__currentPlayerIndex - 1) % (len(self.__players))
            score = move[0]
            self.__grid[self.__currentPos] = score
            self.currentPlayer.addScore(-score)
            self.__currentPos = move[1]
            self.__grid[self.__currentPos] = self.characterValue
            return move
        else:
            return None
    
    # On convertit une chaîne de texte entrée par l'utilisateur en information de commande
    # L'utilisateur peut entrer une direction (N,S,W,E...) ou une position qui correspond à la position
    # d'arrivée du personnage
    # Exemple : pour aller de (3,3) à (2,2) on peut écrire soit NW (North West) soit 2,2
    def inputToCmd(self,s):
        # Si la commande est une direction (N,S,...) on la transforme en couple d'entiers (vecteur de direction)
        if GameRules.MOVES.has_key(s):
            cmd = (self.__currentPos[0] + GameRules.MOVES[s][0],self.__currentPos[1] + GameRules.MOVES[s][1])
        
        # Sinon, on regarde si c'est une entrée de la forme "x,y" et dans ce cas on la convertit en couple (x,y)
        # On ne peut pas utiliser la méthode split de s car on vérifie également 
        # qu'il n'y a que des nombres à part la virgule dans la chaîne        
        else:
            sx = ""
            sy = ""
            k = 0
            
            #On stocke tout ce qu'il y a avant une virgule dans sx
            while k < len(s) and s[k] != ",":
                if not s[k] in numbers:
                    return ""
                else:
                    sx = sx + s[k]
                    k += 1
                    
            k += 1
            
            # On stocke tout ce qu'il y a après une virgule dans sy
            while k < len(s) :
                if not s[k] in numbers:
                    return ""
                else:
                    sy = sy + s[k]
                    k += 1
            
            # On convertit en couple
            cmd = (int(sx),int(sy))
            
        return cmd
    
    
    def askCmd(self):
        print("Entrez la position où vous souhaitez aller : ")
            
        s = raw_input()
        newPos = None        
            
        if s == "undo":
            self.undo()
            print(self)
        elif s != "exit":
            newPos = self.inputToCmd(s)
        
        return s,newPos

    # Fonction de gestion d'une partie
    # Gère les commandes undo et exit
    def play(self):
        while not self.isOver():
            print(self)
            
            botValue = self.__botValue[self.__currentPlayerIndex]
            if botValue > 0:            
                optMove = self.bestMove(botValue)
                self.move(optMove)
                print "L'ordinateur a joué " + str(optMove)
            else:
                s,newPos = self.askCmd()              
                if s == "exit":
                    return
                
                print ""
                
                while s == "undo" or not self.validMove(newPos):
                    s,newPos = self.askCmd()              
                    if s == "exit":
                        return
            
            print ""
    
        print(self)
        
    # Génère les coups possibles de la grille actuelle
    def possibleMoves(self):
        listMoves = []
        for i in range(-1,2):
            for j in range(-1,2):
                coords = (self.__currentPos[0]+i,self.__currentPos[1]+j)
                if coords in self.__grid and self.__grid[coords] != self.characterValue and self.__grid[coords] > 0:
                    listMoves += [coords]
        return listMoves
    
    # Renvoit le signe d'un entier (0 si 0)
    def sign(self,score):
        if score > 0:
            return 1
        elif score == 0:
            return 0
        else:
            return -1
    
    # Généralisation de l'algorithme :
    # L'évaluation est un vecteur d'évaluations pour chaque joueur
    # La composante i du vecteur correspond au score du joueur par rapport à la partie, c'est-à-dire au min de la différence des scores avec les autres joueurs
    # En somme son score consiste à son pire résultat vis-à-vis des autres joueurs
    # C'est ce pire résultat qu'il veut maximiser pour gagner contre tous les joueurs
    def evaluationScore(self,playerIndex,depth,isOver):
        scores = []
        for p in self.__players:
            diffScores = [p.score - player.score for player in self.__players if not p is player] 
            scores += [min(diffScores)]
            
        # Si la partie est terminée et que le score de l'ordinateur
        # est plus élevé que celui des autres joueurs, on renvoit
        # un score très élevé (10000) en rajoutant un terme depth
        # afin de privilégier une victoire le plus rapidement possible
        # (s'il a le choix entre deux configurations où la partie se termine sur sa victoire
        # on préfèrera qu'il choisisse celle qui termine le plus rapidement)
        if isOver:
            scores = [(10000 + depth)*self.sign(score) for score in scores]

        return scores
    
    # Implémente l'algorithme du minimax
    # Généralisation du minimax à deux joueurs
    # Chaque joueur essaie de maximiser son évaluation de score (c'est-à-dire de maximiser la composante correspondant au joueur)
    # Ceci est un test : l'algorithme n'est peut-être pas optimal
    # En revanche on remarque qu'à deux joueurs, l'algorithme est égal au minimax classique à deux joueurs,
    # en effet l'évaluation du minimax classique correspond à la composante de l'évaluation correspondant à l'ordinateur
    # Maximiser cette évaluation correspond à maximiser cette composante
    # l'opposé de l'évaluation du minimax classique correspond à l'autre composante de l'évaluation (c-a-d à la composante de l'autre joueur)
    # Donc minimiser l'évaluation correspond à maximiser cette composante (car elles sont opposées)
    # Les algorithmes sont donc complètement équivalents à deux joueurs
    def minimax(self,playerIndex,depth,index):
        isOver = self.isOver()
        if isOver or depth <= 0:
            return self.evaluationScore(playerIndex,depth,isOver),(-1,-1)
        else:
            allowedMoves = self.possibleMoves()
            optMove = allowedMoves[0]
            val = -inf
            scores = None
            for mv in allowedMoves:
                self.move(mv)
                newVal = self.minimax(playerIndex,depth-1,self.nextPlayerIndex(index))[0]
                if val < newVal[index]:
                    val = newVal[index]
                    scores = newVal
                    optMove = mv
                self.undo()
            return scores,optMove
    
    # Renvoit le meilleur coup de la grille actuelle lorsqu'on voit depth coups à l'avance
    def bestMove(self,depth):
        return self.minimax(self.__currentPlayerIndex,depth,self.__currentPlayerIndex)[1]
    
    # Renvoit le nom du n-ième ordinateur
    def computerName(self,n):
        return "Computer " + str(n)
        
        
# Exemple d'utilisation :
# G = Game(7,["Pierre",GameDifficulty.HARD])
# G.play()

# On peut également faire jouer plusieurs ordinateurs ou même des ordinateurs entre eux
# G = Game(7,[GameDifficulty.HARD,GameDifficulty.MEDIUM,GameDifficulty.HARD])
# G.play()