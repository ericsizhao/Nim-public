import numpy as np
from NIM_env import *
import random
import time
from IPython.display import clear_output

env = NIM_env()
print(env.reward_matrix)
input()

#modified these to len
action_space_size = len(env.action_space)
state_space_size= len(env.state_space)

q_table = np.zeros((state_space_size, action_space_size))
print(q_table)

num_episodes = 10000
max_steps_per_episode = 100

learning_rate = 0.3
discount_rate = 0.7

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

rewards_all_episodes = []

#Q-learning algorithm

#everything that happens each episode
for episode in range(num_episodes):
    #reset the env to inital state
    state = env.reset()

    #keeps track of whether or not the episode is finished
    done = False

    #keeps track of rewards in each episode
    rewards_current_episode = 0

    for step in range(max_steps_per_episode):

        #exploration-exploitation trade-off
        exploration_rate_threshold = random.uniform(0,1)
        if exploration_rate_threshold > exploration_rate:
            action_order = np.argmax(q_table[state,:])
        else:
            #pick a random action
            action_order = rand_action(env.action_space)
            
        new_state,reward, done, info = env.step(action_order)

        #Update Q-table for Q(s,a)
        q_table[state,action_order] = q_table[state,action_order] * (1 - learning_rate) + \
                                learning_rate * (reward + discount_rate * np.max(q_table[new_state,:]))
        state = new_state
        rewards_current_episode += reward

        if done == True:
            break

    #Exploration rate decay
    exploration_rate = min_exploration_rate +\
                           (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

    rewards_all_episodes.append(rewards_current_episode)


#Calculate and print the average reward per thousand episodes
print("done!")
rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), num_episodes/1000)
count = 1000
print("************Average reward per thousand episodes *************\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r/1000)))
    count +=1000
    
#Print updated Q-table
print("\n\n*********Q-table************")
print(q_table)


print("\n\n********************************")
print(" Time to play the Machine!")

#Get who plays first
playFirstPhrase = "Enter (1) to play first, Enter (2) to play second:"
playFirst = intInputProtection(playFirstPhrase,1)
if playFirst == 1:
    print("You are Player One!")
    computerTurn = False
    playFirst = True
elif playFirst == 2:
    print("You are Player Two!")
    computerTurn = True
    playFirst = False
else:
    print("Bad input! You just lost your right to choose!")
    print("You will be Player Two!")

#after the program is trained, we, as a human, want to play!
state = env.reset()
done = False

if playFirst:
    #check for a winner - trivial case
    if not env.movePossible():
        done = True
        print("Machine Wins.. but honestly was that fun?")
        
    #asks for the number of stones you wish to remove
    #input protection ensures a valid response
    else:
        illegalMove = True
        removeStonesPhrase = "How many stones do you want to remove?: "

        while(illegalMove):
            removeStones = intInputProtection(removeStonesPhrase, min(env.action_space))
            illegalMove = env.isIllegalMove(removeStones)
            
            if illegalMove:
                print("Illegal move!")
                
        env.current_stones -= removeStones

        #check for another winner
        if not env.movePossible():
            done = True
            print("You Win! but honestly was that fun?")

while(not done):
    env.render()

    #Computer has decided on an action to make
    action_order = np.argmax(q_table[state,:])

    action_remove = env.action_space[action_order]
    #if the move the machine makes is illegal, just end the game!
    if (env.isIllegalMove(action_remove)):
        print("Machine wants to remove", action_remove, "stones.")
        print("Obviously not allowed!")
        print("You win!")
        done = True
        
    else:
        print("Machine wants to remove", action_remove, "stone(s)")
        #Your turn now
        new_state,reward, done, info = env.step(action_order, True)
        
       
        #If you cannot make a move, end the game
        if(info == 0 or info == "no"):
            print("You cannot make a move :(")
        else:
            print("You have removed" , info, "stone(s)")
        
        if reward == 1:
            print("Machine wins!")
            
        state = new_state





