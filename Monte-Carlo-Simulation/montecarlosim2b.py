import numpy as np
import statistics as sc
# import csv
import progressBarPrinter as pb
# HANDS_p1 = list()
# HANDS_p2 = list()
# RESULTS = list()
##To do list:
##1. Players should loose as soon as they get a bust.
##2. The Match should last as long as the deck lasts.
##3. Strat should be alternated with the person who plays first. 
##4. 
class Player:
  def __init__(self,name):
    self.name = name
    self.finished = False
    self.hand = np.zeros(10)
    self.total = 0
    self.c_to_win = 21 
    self.lastcard = 0
    self.win = 2
    self.act_total = 0
    self.strategy = "Naive"
  def addcard(self,crd,index=0):
    if(index == 0):
      self.hand[self.lastcard] = crd
    else:
      self.hand[index] = crd
    self.total = np.sum(self.hand[1:])
    self.act_total = np.sum(self.total+self.hand[0])
    self.c_to_win = 21-self.total
    self.lastcard +=1
  def checkwin(self):
    if(self.act_total == 21):
      self.win = 1
      self.finished = True
      decision = "Winner 21"
    elif(self.act_total >= 21):
      self.finished = True
      self.win = 3
      decision = "Lost Greater than 21"
    else:
      self.finsihed = False
      decision = "Haven't Decided"
    print("I am ",self.name," and decision is ",decision,"\nmy current hand: ",self.hand)

class Deck:
  def __init__(self):
    self.cards = np.array([])
    self.head = 0

  def build_deck_with_array(self,values):
    self.cards = values

  def build_deck(self):
    cards = np.array(['11','1','2','3','4','5','6','7','8','9','T','J','Q','K'])
    #suites = np.array(['H','C','S','D'])
    deck = list()
    for i in range(4):
      for j in cards:
        deck.append([j])
    deck = np.repeat(deck,4)
    deck_vals = np.array([])
    for i in deck:
      deck_vals = np.append(deck_vals,get_value(i))
    self.cards = deck_vals

  def draw_card(self):
    np.random.seed()
    try:
      ind = np.random.choice(len(self.cards))
    except ValueError:
      return(404)
    chosen = self.cards[ind]
    self.cards = np.delete(self.cards,ind)
    return(chosen)

  def draw_card_seq(self,delete=True):
    chosen = self.cards[0]
    if(delete):
      self.cards = np.delete(self.cards,0)

def Expectation(sampleset):
  """Calculates the Expectation of the PD named SampleSet"""
  probablities = sampleset/len(sampleset)
  return(np.sum(probablities))

def std_dev(probablity,sampleset):
  return(((probablity*(1-probablity))/len(sampleset))**(0.5))

def get_value(card_type):
  try:
    val = int(card_type)
    return(val)
  except ValueError:
    return(10)

def start_match(dk,list_of_winners,in1,in2,in3,in4,cnt=True):
  count = 0
  while(dk.cards.size>0):
    polly,molly = Player("Polly"),Player("Molly")
    if(count%2==0):
      winner = start_game(dk,polly,molly,in1,in2,in3,in4,cnt)
    else:
      winner = start_game(dk,molly,polly,in3,in4,in1,in2,cnt)
    count+=1
    list_of_winners.append(winner)
  return(list_of_winners)

def start_game(dk,p1,p2,i1,i2,i3,i4,counting):
  if(not(counting)):
    sample_deck = Deck()
    sample_deck.build_deck()
    card = dk.draw_card()
    p1.addcard(card)
    card = dk.draw_card()
    if(card == 404):
      return("Tie")
    p2.addcard(card)
    while(p1.finished == False and p2.finished == False and dk.cards.size!=0):
      #print("P1's total",p1.act_total)
      if(p1.act_total>=21):
        p1.finished = True
        p1.checkwin()
        # print("Polly Holds")
      elif(np.count_nonzero(sample_deck.cards[sample_deck.cards+p1.act_total<=21])>=i1 and p2.finished == False):
        # print("Polly Draws and Molly hasn't finsihed")
        card = dk.draw_card()
        p1.addcard(card)
        p1.checkwin()
      elif(p2.finished == True and (((Expectation(sample_deck.cards[sample_deck.cards+p2.total<=21])+p2.total)>p1.act_total) or len(sample_deck.cards[sample_deck.cards+p2.total<=21]) >= i2)):
        # print("Polly Draws and Molly has finished")
        card = dk.draw_card()
        p1.addcard(card)
        p1.finished = False
        p1.checkwin()
      else:
        p1.finished = True
        p1.checkwin()
      #print("P2's Total",p2.act_total)
      if(p1.finsihed==False):
        if(p2.act_total>=21):
          p2.finished = True
          p2.checkwin()
          # print("Polly Holds")
        elif(np.count_nonzero(sample_deck.cards[sample_deck.cards+p2.act_total<=21])>=i3 and p1.finished == False):
          # print("Polly Draws and Molly hasn't finsihed")
          card = dk.draw_card()
          p2.addcard(card)
          p2.checkwin()
        elif(p1.finished == True and (((Expectation(sample_deck.cards[sample_deck.cards+p1.total<=21])+p1.total)>p2.act_total) or len(sample_deck.cards[sample_deck.cards+p1.total<=21]) >= i4)):
          # print("Polly Draws and Molly has finished")
          card = dk.draw_card()
          p2.addcard(card)
          p2.finished = False
          p2.checkwin()
        else:
          # print("Polly Holds")
          p2.finished=True
          p2.checkwin()
    HANDS_p1.append(p1.hand.tolist())
    HANDS_p2.append(p2.hand.tolist())
    if(p1.win == 1 or p2.win == 3):
     # print("Polly Wins")
      winner = p1.name
    elif(p2.win == 1 or p1.win == 3):
     # print("Molly Wins")
      winner = p2.name
    elif(p1.act_total == p2.act_total):
      #print("It was a tie")
      winner = "Tie"
    elif(p1.act_total>p2.act_total and p1.win == 2):
      #print("Polly Wins")
      winner = p1.name
    elif(p1.act_total<p2.act_total and p2.win == 2):
      #print("Molly Wins")
      winner = p2.name 
    else:
      winner = "Tie"
    RESULTS.append(winner)
    return(winner)
  else:
    card = dk.draw_card()
    p1.addcard(card)
    card = dk.draw_card()
    if(card == 404):
      return("Tie")
    p2.addcard(card)
    while(p1.finished == False and p2.finished == False and dk.cards.size!=0):
      #print("P1's total",p1.act_total)
      if(p1.act_total>=21):
        p1.checkwin()
        # print("Polly Holds")

      elif(np.count_nonzero(dk.cards[dk.cards+p1.act_total<=21])>=i1 and p2.finished == False):
        # print("Polly Draws and Molly hasn't finsihed")
        print("Condition 1: ",len(dk.cards[dk.cards+p1.act_total<=21]))
        card = dk.draw_card()
        p1.addcard(card)
        p1.checkwin()

      elif(p2.finished == True and (((Expectation(dk.cards[dk.cards+p2.total<=21])+p2.total)>p1.act_total) or len(dk.cards[dk.cards+p2.total<=21]) >= i2)):
        # print("Polly Draws and Molly has finished")
        print("Expectation:",(Expectation(dk.cards[dk.cards+p2.total<=21])+p2.total)>p1.act_total)
        print("Condition 2:",len(dk.cards[dk.cards+p2.total<=21]))
        card = dk.draw_card()
        p1.addcard(card)
        p1.checkwin()

      else:
        p1.finished = True
        print("I'm Holding ",p1.name)
      #print("P2's Total",p2.act_total)
      #if(p1.finished==False):
      if(p2.act_total>=21):
        p2.finished = True
        p2.checkwin()
        # print("Polly Holds")

      elif(np.count_nonzero(dk.cards[dk.cards+p2.act_total<=21])>=i3 and p1.finished == False):
        # print("Polly Draws and Molly hasn't finsihed")
        card = dk.draw_card()
        p2.addcard(card)
        p2.checkwin()

      elif(p1.finished == True and (((Expectation(dk.cards[dk.cards+p1.total<=21])+p1.total)>p2.act_total) or len(dk.cards[dk.cards+p1.total<=21]) >= i4)):
        # print("Polly Draws and Molly has finished")
        print("Expectation:",(Expectation(dk.cards[dk.cards+p1.total<=21])+p1.total)>p2.act_total)
        print("Condition 2:",len(dk.cards[dk.cards+p1.total<=21]))
        card = dk.draw_card()
        p2.addcard(card)
        p2.finished = False
        p2.checkwin()
      else:
        # print("Polly Holds")
        p2.finished=True
        print("I'm holding", p2.name)
    # HANDS_p1.append(p1.hand.tolist())
    # HANDS_p2.append(p2.hand.tolist())
    if(p1.win == 1 or p2.win == 3):
     # print("Polly Wins")
      winner = p1.name
    elif(p2.win == 1 or p1.win == 3):
     # print("Molly Wins")
      winner = p2.name
    elif(p1.act_total == p2.act_total):
      #print("It was a tie")
      winner = "Tie"
    elif(p1.act_total>p2.act_total and p1.win == 2):
      #print("Polly Wins")
      winner = p1.name
    elif(p1.act_total<p2.act_total and p2.win == 2):
      #print("Molly Wins")
      winner = p2.name 
    else:
      winner = "Draw"
    print("The Winner of this game is:",winner)
    #RESULTS.append(winner[0])
    return(winner)

def main_menu_mc2():
  print("\n\n\n\t\t\t******BlackJack Simulator v2.0*****\n\n\n")
  flag = 1
  while(flag==1):
    choice = int(input("Please select the program option to be executed:\n1. Find choice parameters for hiting on opponent not holding.\n2. Find choice parameters for hitting on opponent holding.\n3. Simulate N rounds of BlackJack.\n4. Simulate N rounds with card counting\n5. Exit\n"))
    if(choice == 1):
      deck = Deck()
      deck.build_deck()
      sumin = int(input("Enter the Value for S: \t"))
      print("P(X+S<=21) = ",len(deck.cards[deck.cards+sumin<=21])/len(deck.cards))
      flag = 1
      #return(main_menu_mc2())
    elif(choice==2):
      deck = Deck()
      deck.build_deck()
      sumin = int(input("Enter the value of S_v: \t"))
      print("E[X|X+S_v<21] = ",Expectation(deck.cards[deck.cards+sumin<21]))
      flag = 1
      #return(main_menu_mc2())
    elif(choice == 3):
      input1 = float(input("Enter the value for Player 1, P_1: "))*224
      input2 = float(input("Enter the value for Player 1, P_2: "))*224
      input4 = float(input("Enter the value for Player 2, P_1: "))*224
      input5 = float(input("Enter the value for Player 2, P_2: "))*224
      input3 = int(input("Enter the number of times the game should be simulated: "))
      flag = 1
      #return(main_menu_mc2())
      low = list()
      for i in range(input3):
        deck = Deck()
        deck.build_deck()
        low.append(start_match(deck,low,input1,input2,input4,input5))
        # sufString = "Games Played:"+str(len(low))+"."
        # pb.printProgressBar(iteration=i,total=input3-1,prefix="Calculating...",suffix = sufString)
      print("Total Games :",len(low))
      # with open('hands_file.csv','w',newline = '') as csvfile:
      #   cswrite = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
      #   cswrite.writerows(HANDS_p1)
      #   cswrite.writerow("P2")
      #   cswrite.writerows(HANDS_p2)
      #   cswrite.writerows(RESULTS)
      Polly_wins=low.count("Polly")
      Molly_wins=low.count("Molly")
      Ties = low.count("Tie")
      Prob_p1 = Polly_wins/len(low)
      Prob_p2 = Molly_wins/len(low)
      conf_int_p1_h = Prob_p1+std_dev(Prob_p1,low)*1.645             #std_dev(Polly_wins,Molly_wins,Ties,low)*1.645
      conf_int_p1_l = Prob_p1-std_dev(Prob_p1,low)*1.645
      conf_int_p2_h = Prob_p2+std_dev(Prob_p2,low)*1.645
      conf_int_p2_l = Prob_p2-std_dev(Prob_p2,low)*1.645
      print("\n\nPlayer 1 wins:",Polly_wins)
      print("\n\nPlayer 2 wins:",Molly_wins)
      print("\n\nProbability for Player 1's Victory: ",Polly_wins/len(low),"")
      print("\n\nProbability for Player 2's Victory: ",Molly_wins/len(low),"")
      print("\n\nConfidence Intervals\n \tP1: [",conf_int_p1_l," , ",conf_int_p1_h,"]\n\tP2: [",conf_int_p2_l,",",conf_int_p2_h,"]")
      #return(main_menu_mc2())
    elif(choice == 4):
      flag = 1
      input1 = float(input("Enter the value for P_1: "))*224
      input2 = float(input("Enter the value for P_2: "))*224
      input3 = int(input("Enter the number of times the game should be simulated: "))
      low = list()
      for i in range(input3):
        deck = Deck()
        deck.build_deck()
        low.append(start_match(deck,low,input1,input2,cnt=False))
        # sufString = "Games Played:"+str(len(low))+"."
        # pb.printProgressBar(iteration=i,total=input3-1,prefix="Calculating...",suffix = sufString)
      print("Total Games = ",len(low))
      Polly_wins=low.count("Polly")
      Molly_wins=low.count("Molly")
      Ties = low.count("Tie")
      Prob_p1 = Polly_wins/len(low)
      Prob_p2 = Molly_wins/len(low)
      conf_int_p1_h = Prob_p1+std_dev(Prob_p1,low)*1.645             #std_dev(Polly_wins,Molly_wins,Ties,low)*1.645
      conf_int_p1_l = Prob_p1-std_dev(Prob_p1,low)*1.645
      conf_int_p2_h = Prob_p2+std_dev(Prob_p2,low)*1.645
      conf_int_p2_l = Prob_p2-std_dev(Prob_p2,low)*1.645
      print("\n\nPlayer 1 wins:",Polly_wins)
      print("\n\nPlayer 2 wins:",Molly_wins)
      print("\n\nProbability for Player 1's Victory: ",Polly_wins/len(low),"")
      print("\n\nProbability for Player 2's Victory: ",Molly_wins/len(low),"")
      print("\n\nConfidence Intervals\n \tP1: [",conf_int_p1_l," , ",conf_int_p1_h,"]\n\tP2: [",conf_int_p2_l,",",conf_int_p2_h,"]")
      # with open('hands_file.csv','w',newline = '') as csvfile:
      #   cswrite = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
      #   cswrite.writerows(HANDS_p1)
      #   cswrite.writerows(HANDS_p2)
      #   cswrite.writerow(RESULTS)
      #return(main_menu_mc2())
    elif(choice == 5):
      flag = 0
    else:
      flag = 1
      print("INVALID INPUT")
    #return(main_menu_mc2())
deck = Deck()
deck.build_deck()
P1,P2 = Player("P1"),Player("P2")
start_game(deck,P1,P2,0.5*224,0.5*224,0.7*224,0.7*224,True)