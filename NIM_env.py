import random
class NIM_env:

    #CHECKED
    #later we can add cash and stuff
    def __init__(self):
        self.seed()
        self.action_space = gen_action_space()
        self.state_space = gen_state_space()
        self.current_stones = len(self.state_space) - 1
        self.intial_stones = len(self.state_space) - 1

        
    #given an action, how does the enviornment react?
    #param action: action the agent wishes to take      
    #returns a tuple (state, reward, done, info)
    #   state - the agent's next observation of the current environment
    #   reward - the reward from doing that action
    #   done - has the game ended yet
    #   info - diagnostic information helped for debugging - opponent's move
    def step(self,action_order,human = False):

        #game has not finished yet
        done = False
        info = "no" #default state of info -- will be changed soon
        
        action_remove = self.action_space[action_order]

        #if the move the Machine chose was illegal
        #return -1 reward b/c machine made illegal move
        if self.isIllegalMove(action_remove):
            reward = -1
            info = -1
            
            
        else:
            #agent will do the action to the environment AKA
            #will remove stones
            self.current_stones = self.current_stones - action_remove

            #opponent will calculate their move
            #will return the number of stones it wishes to remove
            #(no need for indexes)
            oppoMove = self.opponentMove(human)

            #if game has ended
            reward = reward_function(oppoMove)
            
        if (reward == 1 or reward == -1):
            done = True

        #Opponent moves
        #I don't think this (not done) part matters for Q-learning
        if(not done):
            self.current_stones = self.current_stones - oppoMove
            info = oppoMove
        
        tupleStep = (self.current_stones,reward,done,info)
        
        return tupleStep

    #CHECKED
    #resets the state of the environment and returns intial state
    def reset(self):
        self.current_stones = self.intial_stones
        return self.current_stones
        #return - the intial state

    #CHECKED
    #display the environment's current state
    def render(self):
        print("\n")
        print ("There are", self.current_stones, "stones on the board!")
        #just prints the current game's state...

    #CHECKED - this method is useless!
    #gotta remember to delete the env when you are done
    def close(self):
        print("Remember to del youself!")
        
        
    #sets the seed for the enviornment's random number generators
    #return the seed you will use
    #will use seed 300 for the random opponent
    #will use seed 310 for random selection of the agent's moves
    def seed(self,seed = None):
        self.seed = (300,310,320)

    #random opponent
    #Will return 0 if machine has won (b/c oppo cannot make a move)
    #Will return -1 if machine has made an illegal move
    #Will return (amount of stones opponent wishes to remove) otherwise
    def opponentMove(self,human):
        if human:
    
            self.render()

            #if you cannot make a legal move
            #return 0 b/c Machine has won, and end the game
            if not self.movePossible():
                return 0
   
            #asks for the number of stones you wish to remove
            #input protection ensures a valid response
            illegalMove = True
            removeStonesPhrase = "How many stones do you want to remove?: "

            while(illegalMove):
                removeStones = intInputProtection(removeStonesPhrase, min(self.action_space))
                illegalMove = self.isIllegalMove(removeStones)
                
                if illegalMove:
                    print("Illegal move!")

            return removeStones
        
        else:
            #if you make cannot make legal move
            if not self.movePossible():
                return 0
            #if Machine has already lot/the computer made an illegal move
            elif self.current_stones < 0:
                return -1
            #return a random move
            else:
                illegal_Move = True
                while(illegal_Move):
                    #get a random action
                    action_order = rand_action(self.action_space)
                    action_remove = self.action_space[action_order]

                    illegal_Move = self.isIllegalMove(action_remove)

                return action_remove

    #return boolean - if a move is possible  
    def movePossible(self):
        if self.current_stones > -1 and self.current_stones >= min(self.action_space):
            return True
        else:
            return False
        
    def isIllegalMove(self,remove_stones):
        #if move is illegal - return True
        if remove_stones > self.current_stones or remove_stones not in self.action_space:
            return True
        #if move is valid - return False
        else:
            return False
        
        


#CHECKED
#EXPERIMENTABLE
#Param s: state of the game
#Param a: the action taken
def reward_function(opponentMove):
        
    #if the computer removed stones leading to no stones left,
    #opponent cannot remove any more stones - meaning computer won
    if (opponentMove == 0):
        return 1
    #if the computer removed stones leading to a negative amount of stones left,
    #then computer loses
    elif (opponentMove < 0):
        return -1
    else:
        return 0

#generates a random action
#returns a tuple: (action_order)
    #action_order - the index of stones we wish to remove
def rand_action(action_space):
    action_order = random.randint(0,len(action_space)-1)
    return action_order

#CHECKED
#Will generate the action space
#We are playing 1,2,3 NIM
#so only actions are 1,2,3
#obviously right now it's pretty simple, but when cash comes this will be useful
def gen_action_space():
    #ensure an input of a list of integers - protects against strings and floats
    #need to ensure that numbers greater than 0 are entered
    validIntList = False
    greaterZero = False
    while(not validIntList or greaterZero):
        validIntList = False
        greaterZero = False
        try:
            #Splits the user input into a list of strings,
            #Then converts the that list of strings into a list of integers
            print("Enter a1,a2,a3...n with each number seperated by a comma.")
            print("Example:1,3,4 ")
            userStringList = input().split(",")
            userIntList = []
            for x in userStringList:
                userIntList.append(int(x))
                if(int(x) < 1):
                    print("Enter numbers greater than 0!")
                    greaterZero = True
        except:
            print("Invalid input! Enter the numbers and commas properly!\n")
        else:
            validIntList = True

    return userIntList

#CHECKED
#Will generate the state space
#this is pretty simple too
def gen_state_space():
    #later will be input from user but whatever
    n = intInputProtection("Enter number of stones:", 0)
    stateSpace = []
    for x in range (n + 1):
        stateSpace.append(x)
    return stateSpace


#CHECKED
#Function Purpose - protects input for integers
#phrase - (String): line that will be printed to ask for variable
#lessThan - (int): entered integer will not be less than this number
def intInputProtection(phrase,lessThan):
    #ensure an integer is entered - protects against strings and floats
    #ensures no negative numbers are entered
    validInt = False
    negative = False
    while(not validInt or negative):
        validInt = False
        negative = False
        try:
            #Splits the user input into a list of strings,
            #Then converts the that list of strings into a list of integers
            print(phrase)
            entered = int(input())
            if(entered < lessThan):
                    print("Don't enter invalid numbers!!")
                    negative = True
        except:
            print("Invalid input! Enter an integer!\n")
        else:
            validInt = True
    return entered



