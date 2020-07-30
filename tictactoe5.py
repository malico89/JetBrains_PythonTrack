"""Tic-tac-toe program, phase 5: Computer can be Easy or Medium or Hard"""
"""Hard = Minimaxi algorithm"""
import random

class TicTacToe:
    # possible moves, list of tuples
    POSSIBLE_MOVES = [(1, 3), (2, 3), (3, 3), (1, 2), (2, 2), (3, 2), (1, 1), (2, 1), (3, 1)]

    def __init__(self, x, o):
        # initialize the board. _ = empty
        # indices line up with POSSIBLE_MOVES[index]
        self.board_state = list("_" * 9)

        # gameState means game is going on, not ended
        self.gameState = True

        # xPlaying is True is first player's turn, false for O's turn
        self.xPlaying = True
        # update this depending on who the user wants to play
        self.Xplayer = x
        self.Oplayer = o
    
    def board(self):
        # prints current board based on current board_state
        print("---------")
        print("|", self.board_state[0].replace("_", " "), self.board_state[1].replace("_", " "), self.board_state[2].replace("_", " "), "|")
        print("|", self.board_state[3].replace("_", " "), self.board_state[4].replace("_", " "), self.board_state[5].replace("_", " "), "|")
        print("|", self.board_state[6].replace("_", " "), self.board_state[7].replace("_", " "), self.board_state[8].replace("_", " "), "|")
        print("---------")
        return

    # this function to route the game depending on who is X and O
    def nextPlayer(self):
        # print board
        self.board()
        # assign letter
        if self.xPlaying:
            letter = "X"
            if self.Xplayer == "user":
                self.humanMove(letter)
            elif self.Xplayer == "easy":
                self.AImoveEasy(letter)
            elif self.Xplayer == "medium":
                self.AImoveMed(letter) 
            elif self.Xplayer == "hard":
                self.AImoveHard(letter)
        else:
            letter = "O"
            if self.Oplayer == "user":
                self.humanMove(letter)
            elif self.Oplayer == "easy":
                self.AImoveEasy(letter)
            elif self.Oplayer == "medium":
                self.AImoveMed(letter) 
            elif self.Oplayer == "hard":
                self.AImoveHard(letter)           

    # this method returns indices of possible moves as a list
    # making this for any board that is passed to it, not just current board
    def openMoves(self, board):
        return [i for i in range(len(board)) if board[i] == "_"]

    # prompt the user until valid coordinates entered
    def humanMove(self, letter):
        # ask input from user until valid move
        while True:
            # get input from user
            play = input("Enter the coordinates: ")
            # check if input is numeric
            if play.replace(" ", "").isnumeric() == False:
                print("You should enter numbers!")
            # all ints, convert to tuple
            else:
                play = tuple(int(x.strip()) for x in play.split(' '))
                # not a valid coordinate
                if play not in self.POSSIBLE_MOVES:
                    print("Coordinates should be from 1 to 3!")
                # valid coordinate, check if valid move
                # check if index of coordinate is _ in board_state
                elif self.POSSIBLE_MOVES.index(play) not in self.openMoves(self.board_state):
                    print("This cell is occupied! Choose another one!")
                # valid move, empty square
                else:
                    break
        # make a move. update board state depending on player move
        self.board_state[self.POSSIBLE_MOVES.index(play)] = letter

        # check if won
        self.win(letter)           

    # Easy AI: returns a random move out of available moves
    def AImoveEasy(self, letter):
        print('Making move level "easy"')
        # possible PC moves, as indices in board_state
        PCmoves = self.openMoves(self.board_state)
        # index of play is now randomly generated
        self.board_state[random.choice(PCmoves)] = letter
        
        # check if won
        self.win(letter)

    # medium difficulty. Will win or block if it can.
    def AImoveMed(self, letter):
        print('Making move level "medium"')
        
        # possible PC moves, as indices in board_state
        PCmoves = self.openMoves(self.board_state)

        # opponent letter
        if letter == "X":
            otherletter = "O"
        else:
            otherletter = "X"
    
        # check if AI can win/block in next move. Pass each possible move to a canwin method
        for i in range(len(PCmoves)):
            # canwin returns True if passed move wins the game
            if self.canwin(PCmoves[i], letter):
                # if found a winning move, commit
                move = PCmoves[i]
                break
        # if no winning move, check if can block
        else:
            for i in range(len(PCmoves)):    
                if self.canwin(PCmoves[i], otherletter):
                    # if found a blocking move, commit
                    move = PCmoves[i]
                    break
            else:
                # if we made it here (no breaks), no winning or blocking move found. Do a random move.
                move = random.choice(PCmoves) 

        self.board_state[move] = letter

        # check if won. For updating X/O state
        self.win(letter)

    # hard AI: optimized for winning
    def AImoveHard(self, letter):
        # create a AImove object, which inherits from class TicTacToe
        # constructor arguments: current board state, AI letter
        print('Making move level "hard"')
        AImove = AI(self.board_state, letter)
        
        # call bestMove to get minimax output
        move = AImove.bestMove()

        # update board
        self.board_state[move] = letter

        # check if won. For updating X/O state
        self.win(letter)
     

    # for a given move and letter (X/O), return True if that move wins for that letter. False if it doesn't.
    def canwin(self, move, letter):
        # create a temp board with test move 
        temp_board = self.board_state[:]
        temp_board[move] = letter

        # check if tempboard wins
        # 8 win conditions
        if (temp_board[0] == letter and temp_board[1] == letter and temp_board[2] == letter) or (temp_board[3] == letter and temp_board[4] == letter and temp_board[5] == letter) or (temp_board[6] == letter and temp_board[7] == letter and temp_board[8] == letter) or (temp_board[0] == letter and temp_board[3] == letter and temp_board[6] == letter) or (temp_board[1] == letter and temp_board[4] == letter and temp_board[7] == letter) or (temp_board[2] == letter and temp_board[5] == letter and temp_board[8] == letter) or (temp_board[0] == letter and temp_board[4] == letter and temp_board[8] == letter) or (temp_board[2] == letter and temp_board[4] == letter and temp_board[6] == letter):
            return True
        else:
            return False
    
    # depending on current board state, prints whether someone won or not
    # checks for terminal state
    def win(self, letter):
        # 8 win conditions
        if (self.board_state[0] == letter and self.board_state[1] == letter and self.board_state[2] == letter) or (self.board_state[3] == letter and self.board_state[4] == letter and self.board_state[5] == letter) or (self.board_state[6] == letter and self.board_state[7] == letter and self.board_state[8] == letter) or (self.board_state[0] == letter and self.board_state[3] == letter and self.board_state[6] == letter) or (self.board_state[1] == letter and self.board_state[4] == letter and self.board_state[7] == letter) or (self.board_state[2] == letter and self.board_state[5] == letter and self.board_state[8] == letter) or (self.board_state[0] == letter and self.board_state[4] == letter and self.board_state[8] == letter) or (self.board_state[2] == letter and self.board_state[4] == letter and self.board_state[6] == letter):
            # print board one last time
            self.board()
            print(letter, "wins\n")
            # toggle game state to end game
            self.gameState = False
        # if letter didn't win, check for empty cells
        elif self.board_state.count("_") == 0:
            print("Draw\n")
            # toggle game state to end game
            self.gameState = False
        # else no win, empty cells, toggle player
        else:
            self.xPlaying = not self.xPlaying

# when this gets instantiated, it inherits the current game as it is
# has all the same methods as TicTacToe, plus new methods to handle minimax
class AI(TicTacToe):
    def __init__(self, board_state, AIletter):
        self.board_state = board_state      # initial board state, tree root. Clone, don't update.
        self.AIletter = AIletter
        self.Oppletter = "X" if AIletter == "O" else "O"
        self.AIturn = True                  # toggle between turns
    
    # minimax function. Arguments: a board, the current player, and the move that got you that board
    def minimax(self, board, isAIturn):
        # check if terminal state. 3 terminal cases.
        # can AI win?
        if self.win(board, self.AIletter) == True:
            return 10
        # can opponent win?
        elif self.win(board, self.Oppletter) == True:
            return -10
        # is the board full?
        elif board.count("_") == 0:
            return 0
        # here's the recursive part
        else:
            # array of available moves as of this iteration
            # moves: an int array that contains open indices
            moves = self.openMoves(board)

            # if AI turn, maximize
            if isAIturn == True:
                bestvalue = -100

                for move in moves:
                    temp_board = board[:]       # temp board clone
                    temp_board[move] = self.AIletter
                    val = self.minimax(temp_board, False)
                    bestvalue = max(val, bestvalue)
                return bestvalue

            # if opponent turn, minimize
            else:
                bestvalue = 100
                # update this to make all available moves
                for move in moves:
                    temp_board = board[:]       # temp board clone
                    temp_board[move] = self.Oppletter
                    val = self.minimax(temp_board, True)
                    bestvalue = min(val, bestvalue)
                return bestvalue


    # redefine win method to return T/F depending on if a win state
    def win(self, board, letter):
        # 8 win conditions. Check if with current board, guven letter has won
        if (board[0] == letter and board[1] == letter and board[2] == letter) or (board[3] == letter and board[4] == letter and board[5] == letter) or (board[6] == letter and board[7] == letter and board[8] == letter) or (board[0] == letter and board[3] == letter and board[6] == letter) or (board[1] == letter and board[4] == letter and board[7] == letter) or (board[2] == letter and board[5] == letter and board[8] == letter) or (board[0] == letter and board[4] == letter and board[8] == letter) or (board[2] == letter and board[4] == letter and board[6] == letter):
            return True
        else:
            return False

    # bestMove takes in the given board and returns index of best move based on minimax
    def bestMove(self):
        # this needs to return an index!
        bestmove = -1
        bestvalue = -100
        
        # open moves
        moves = self.openMoves(self.board_state)

        for move in moves:
            temp_board = self.board_state[:]       # temp board clone
            temp_board[move] = self.AIletter
            
            val = self.minimax(temp_board, False)
            if val > bestvalue:
                bestvalue = val
                bestmove = move

        return bestmove

def menu(x, o):
    # instantiate game based on player input. Args are X, O
    game = TicTacToe(x, o)

    while game.gameState == True:
        game.nextPlayer()
    # once game ended, return for user input
    return

def main():
    # prompt user for starting instructions. Will loop until player exits.
    while True:
        choice = input("Input command: ").split()
        # if player
        if choice[0].lower() == "exit":
            break
        # if start, go to menu(), which defines how to instantiate game    
        elif choice[0].lower() == "start":
            # check for correct inputs
            if len(choice) != 3:
                print("Bad parameters!")
            elif choice[1] .lower() not in ["user", "easy", "medium", "hard"] or choice[2].lower() not in ["user", "easy", "medium", "hard"]:
                print("Bad parameters!")
            # good input, proceed to game
            else:    
                menu(choice[1].lower(), choice[2].lower())

main()

