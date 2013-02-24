"""
File: Player.py

Defines a simple artificially intelligent player agent
You will define the alpha-beta pruning search algorithm
You will also define the score function in the MancalaPlayer class,
a subclass of the Player class.
"""


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):    
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        return str(self.num)
        
    def minimaxMove( self, board, ply ):
        """ Choose the best minimax move.  Returns (move, val) """
        move = -1
        score = -INFINITY
        turn = self
        
        for m in board.legalMoves( self ):
            if ply == 0:
                return (self.score(board), m)
            
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            
            nb = deepcopy(board)
            nb.makeMove(self, m)
            opp = Player(self.opp, self.type, self.ply)
            s, oppMove = opp.minValue(nb, ply-1, turn)
            
            if s > score:
                move = m
                score = s
        
        return score, move

    def maxValue( self, board, ply, turn):
        """ 
        Find the minimax value for the next move for this player
        at a given board configuation Returns (score, oppMove)
        """
        if board.gameOver():
            return (turn.score( board ), -1)
        
        score = -INFINITY
        move = -1
        
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board ), m)
            
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove( self, m )
            s, oppMove = opponent.minValue(nextBoard, ply-1, turn)
            
            if s > score:
                move = m
                score = s
        
        return (score, move)
    
    def minValue( self, board, ply, turn ):
        """
        Find the minimax value for the next move for this player
        at a given board configuation
        """
        
        if board.gameOver():
            return turn.score( board ), -1
        
        score = INFINITY
        move = -1
        
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board ), m)
            
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove( self, m )
            s, oppMove = opponent.maxValue(nextBoard, ply-1, turn)
            
            if s < score:
                score = s
                move = m
        
        return (score, move)


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        score = 0.0
        if board.hasWon( self.num ):
            score = score + 100.0
        elif board.hasWon( self.opp ):
            score = score +100.0
        for n in range(6):
            score -= board.p2Cups[n]
            score += board.p1Cups[n]
        score += board.scoreCups[0]
        score -= board.scoreCups[1]
        return score

    ###########################################################
    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.
    ###########################################################

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    # 
    # Do NOT change the number of parameters, function name, etc.
    def alphaBetaMove( self, board, ply):
        """ Choose a move with alpha beta pruning """
        move = -1
        alpha = -INFINITY
        beta = INFINITY
        score = -INFINITY
        turn = self
        
        for m in board.legalMoves( self ):
            nb = deepcopy(board)
            nb.makeMove(self, m)
            #opp = Player(self.opp, self.type, self.ply)
            s, bestMove = self.alphaBetaMaxValue(nb, ply-1, turn, alpha, beta)#****#  
            if s > score:
                move = m
                score = s
        #print "Alpha Beta Move in progress"
        #return -1
        return (score, move)

    def alphaBetaMaxValue(self, board, ply, turn, alpha, beta):
        """ 
        Find the alpha-betaMax value for the next move for this player
        at a given board configuation Returns (score, oppMove)
        """
     
        if board.gameOver():#terminal test
            return turn.score( board ), -1
        
        score = -INFINITY
        move = -1
        
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board ), m)  
            
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove( self, m )
            someScore, someMove = opponent.alphaBetaMaxValue(nextBoard, ply-1, turn, alpha, beta)

            if someScore > score:
                score = someScore
                move = m
            if score >= beta:
                return (score, move)
            alpha = max(alpha, score)

        return (score, move)
    
    def alphaBetaMinValue( self, board, ply, turn, alpha, beta):
        """
        Find the minimax value for the next move for this player
        at a given board configuation
        """
        
        if board.gameOver():#terminal test
            return turn.score( board ), -1
        
        score = -INFINITY
        move = -1
        
        for m in board.legalMoves( self ):
            if ply == 0:
                return (turn.score( board ), m)  
            
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove( self, m )
            someScore, someMove = opponent.alphaBetaMaxValue(nextBoard, ply-1, turn, alpha, beta)

            if someScore < score:
                score = someScore
                move = m
            if score <= alpha:
                return (score, move)
            beta = min(beta, score)

        return (score, move)
                
    def chooseMove( self, board ):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove( board, self.ply )
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove( board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            print "Custom player not yet implemented"
            return -1
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be a custom name
# that identifies you or your team.
class MancalaPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        print "Calling score in MancalaPlayer"
        return Player.score( self, board )
        
