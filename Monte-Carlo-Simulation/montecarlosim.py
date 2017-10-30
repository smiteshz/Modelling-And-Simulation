import random as r
#import tkinter as gui
import numpy as np
import montecarlosim2b as mc2
#Progress Bar and other fancy stuff

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


#CLI MAIN MENU STARTS HER
def main_menu ():
  print("Welcome to Smitesh's 552 Programming Assignments Menu:")
  print("Please Choose one of the following options to display.")
  flag = 1
  while(flag==1):
    print("1. The Sychronicity of Lecture and Leisure \n2. What's in the Name?\n3. MonteCarlo Simulation for Playing BlackJack \n4. Exit")
    choice = int(input())
    if (choice==1):
      flag = 0
      prog1()
    elif (choice==2):
      flag = 0
      prog2()
    elif(choice ==3):
      flag = 0
      mc2.main_menu_mc2()
      return
    elif(choice==4):
      flag = 0
      return
    else:
      flag = 1
      print("Invalid Input Please Try again.")

def prog1():
  itns = int(input("Enter the number of times the simulation should be carried out:"))
  hits = 0
  for i in range(itns-1):
    options = ["Lucy","Seinfield"]
    eps = [1,1]

    for t in range(1,255):
      watch = np.random.choice([0,1],p=[0.6,0.4])
      #print("Day ", t, " Watching ", options[watch]," Episode ", eps[watch]," Today")
      eps[watch]= eps[watch]+1
    #print("Final Episode of ",options[0],"Watched is",eps[0])
    if(eps[0]==152):
      hits = hits + 1
    sufString = "Synchronicity achieved "+str(hits)+" times."
    printProgressBar(iteration=i,total=itns-2,prefix="Calculating...",suffix = sufString)
  print("Final Score = ", hits, "\nFraction = ", hits/itns)
  return main_menu()


def prog2():
  itns = int(input("Enter the number of times Tabatha and two girl childs should occur:"))
  name1 = 1
  name2 = 1
  gl = 0
  i = 0
  ctr = 0
  while(i!=itns):
    born1 = 0
    born2 = 0
    name1 = 1
    name2 = 1
    options = ["Boy","Girl"]
    born1 = np.random.choice([0,1],p=[0.5,0.5])
    if (born1==1):
      #print("Relevant Family found!\t Family No.",ctr)
      name1 = np.random.choice([0,1],p=[0.001,0.999])
    born2 = np.random.choice([0,1],p=[0.5,0.5])
    if (born2==1):
      name2 = np.random.choice([0,1],p=[0.001,0.999])
    #family = [options[born1],name1,options[born2],name2]
    #print("Family ", i, "Members: ",born1," ",born2)
    if (name1 == 0 or name2 == 0):
      #print("Relevant Family Found:",ctr)
      if(born1 == 1 and born2 == 1):
        gl = gl + 1
      i = i + 1
    ctr = ctr + 1
    preString = "Families Simulated "+str(ctr)
    printProgressBar(i,itns,prefix ="Finding Relevant Families...",suffix=preString)
  print("The number of families needed to me simulated", ctr)
  print("The total number of Relevant families", i)
  print("The total number of Relevent families where the other child is a girl", gl)
  print("The Probability of that both children are girls and their name is Tabatha is",gl/i)
  print("The reason for getting a value close to 0.5 means that there is an equal possibility of the other child to be a girl or a boy")
  print("This can be imagined as whenever a girl named Tabatha is born, a coin is flipped (as the probability of other child being a girl is independent).")
  return main_menu()

main_menu()

##CLI ENDS HERE

##GUI STARTS HERE
#
# top = gui.Tk()
# def sim1CallBack():
#     prog1()
#     sim1window = gui.Tk()
#     t1 = Text(sim1window)
#     t1.insert(INSERT,"Simulation Completed")
#     tk.mainloop()
#     return
# def sim2CallBack():
#     prog2()
#     return
# def exitcallBack():
#     exit()
#     return
#
# B1 = gui.Button(top, text = "Perform Simulation for 'The Synchronicity of Lecture and Leisure'", command = sim1CallBack)
# B2 = gui.Button(top, text = "Perform Simulation for 'What's in the Name?'", command = sim2CallBack)
# B3 = gui.Button(top, text = "Exit Simulation", command = exitcallBack)
# B1.grid()
# B2.grid()
# B3.grid()
# top.mainloop()
