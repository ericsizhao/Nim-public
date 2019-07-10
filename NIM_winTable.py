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

#get the number of stones
n = intInputProtection("Enter the number of stones:",0)


winMatrix = []
winMoveMatrix = []
winActionOrder = []

#for loop that will iterate through until the table is complete
#each iteration will add one to the solution table
for currentStone in range(n+1):

    if currentStone == 0:
        winMatrix.append(2)
        winMoveMatrix.append(-1)
        winActionOrder.append(-1)

    else:
        moveFound = False
        action_order = 0
        for pMove in userIntList:
            #the move must be legal
            if currentStone >= pMove and winMatrix[currentStone-pMove] == 2:
                winMatrix.append(1)
                winMoveMatrix.append(pMove)
                winActionOrder.append(action_order)
                moveFound = True
                break
            action_order +=1

        if(not moveFound):
            winMatrix.append(2)
            winMoveMatrix.append(-1)
            winActionOrder.append(-1)

print(winMatrix)
print(winMoveMatrix)
print(winActionOrder)
