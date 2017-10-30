import numpy as np
import progressBarPrinter as pb
# HANDS_p1 = list()
# HANDS_p2 = list()
# RESULTS = list()
##To do list:
##1. Players should loose as soon as they get a bust.
##2. The Match should last as long as the deck lasts.
##3. Strat should be alternated with the person who plays first. 
##4. 
RESULTS = list()
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
    if(crd==404):
      self.win = 2
      self.finished = True
      return
    if(index == 0):
      self.hand[self.lastcard] = crd
    else:
      self.hand[index] = crd
    self.total = np.sum(self.hand[1:])
    self.act_total = np.sum(self.total+self.hand[0])
    self.c_to_win = 21-self.total
    self.lastcard +=1
    self.checkwin()

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
    #print("I am ",self.name," and decision is ",decision,"\nmy current hand: ",self.hand)

class Deck:
  def __init__(self):
    self.cards = np.array([])
    self.scards = np.array([])
    self.head = 0
    self.shead = 0
    self.cflag = False
    self.samplecount = 224

  # def build_deck_with_array(self,values):
  #   self.cards = values

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
    self.scards = deck_vals

  def draw_card(self):
    np.random.seed()
    try:
      ind = np.random.choice(len(self.scards))
      chosen = self.scards[ind]
      if(self.cflag):
        self.scards = np.delete(self.scards,ind)
        return(chosen)
      else:
        self.scards = np.delete(self.scards,ind)
        self.cards = np.delete(self.cards,ind)
        return(chosen)
    except ValueError:
      return(404)

  def set_counting(self,attb):    
    self.cflag = not(attb)
    return

  # def draw_card_seq(self,delete=True):
  #   chosen = self.cards[0]
  #   if(delete):
  #     self.cards = np.delete(self.cards,0)

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
  while(dk.scards.size>0):
    if(count%2==0):
      winner = start_game(dk,"Polly","Molly",in1,in2,in3,in4,cnt,count%2)
    else:
      winner = start_game(dk,"Molly","Polly",in3,in4,in1,in2,cnt,count%2)
    count+=1
    list_of_winners.append(winner)
  return(list_of_winners)

def start_game(dk,player1,player2,i1,i2,i3,i4,counting,first):
  dk.set_counting(counting)
  if(first==0):
    p1 = Player(player1)
    p2 = Player(player2)
  else:
    p1 = Player(player2)
    p2 = Player(player1)
  p1.addcard(dk.draw_card())
  p2.addcard(dk.draw_card())
  if(first==0):
    # print("Alt1")
    while((p1.finished==False or p2.finished==False) and len(dk.scards)!=0 and (p1.win==2 and p2.win==2)):
      if(p1.finished==False):
        if(p2.finished==False and (len(dk.scards[dk.scards+p1.act_total<=21])/len(dk.scards))>i1):
          p1.addcard(dk.draw_card())
        elif(p2.finished==True and (Expectation(dk.scards[dk.scards+p2.total < 21])+ p2.total > p1.act_total)):
          p1.addcard(dk.draw_card())
        elif(p2.finished == True and (len(dk.scards[dk.scards+p1.act_total<=21])/len(dk.scards))>i2):
          p1.addcard(dk.draw_card())
        else:
          p1.finished = True
      if(p2.finished == False and p1.win==2 and len(dk.scards)!=0):
        if(p1.finished==False and (len(dk.cards[dk.cards+p2.act_total<=21])/len(dk.cards))>i3):
          p2.addcard(dk.draw_card())
        elif(p1.finished==True and (Expectation(dk.cards[dk.cards+p1.total < 21])+ p1.total > p2.act_total)):
          p2.addcard(dk.draw_card())
        elif(p1.finished == True and (len(dk.cards[dk.cards+p2.act_total<=21])/len(dk.cards))>i4):
          p2.addcard(dk.draw_card())
        else:
          p2.finished = True
  else:
      # print("Alt2")
      while((p1.finished==False or p2.finished==False) and len(dk.scards)!=0 and (p1.win==2 and p2.win==2)):
        if(p1.finished==False):
          if(p2.finished==False and (len(dk.cards[dk.cards+p1.act_total<=21])/len(dk.cards))>i3):
            p1.addcard(dk.draw_card())
          elif(p2.finished==True and (Expectation(dk.cards[dk.cards+p2.total < 21])+ p2.total > p1.act_total)):
            p1.addcard(dk.draw_card())
          elif(p2.finished == True and (len(dk.cards[dk.cards+p1.act_total<=21])/len(dk.cards))>i4):
            p1.addcard(dk.draw_card())
          else:
            p1.finished = True
        if(p2.finished == False and p1.win==2 and len(dk.scards)!=0):
          if(p1.finished==False and (len(dk.scards[dk.scards+p2.act_total<=21])/len(dk.scards))>i1):
            p2.addcard(dk.draw_card())
          elif(p1.finished==True and (Expectation(dk.scards[dk.scards+p1.total < 21])+ p1.total > p2.act_total)):
            p2.addcard(dk.draw_card())
          elif(p1.finished == True and (len(dk.scards[dk.scards+p2.act_total<=21])/len(dk.scards))>i2):
            p2.addcard(dk.draw_card())
          else:
            p2.finished = True
  if(p1.win==2 and p2.win == 2):
    if(p1.act_total>p2.act_total):
      winner = p1.name
    elif(p1.act_total<p2.act_total):
      winner = p2.name
    else:
      winner = "Tie"
  elif(p1.win==1):
    winner = p1.name
  elif(p2.win==1):
    winner = p2.name
  elif(p1.win==3):
    winner = p2.name
  else:
    winner = p1.name
  if(p1.name=="Polly"):
    RESULTS.append([p1.act_total,p2.act_total,winner[0]])
  else:
    RESULTS.append([p2.act_total,p1.act_total,winner[0]])
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
      input1 = float(input("Enter the value for Player 1(Card Counting), P_1: "))#*224
      input2 = input1 #float(input("Enter the value for Player 1, P_2: "))#*224
      input4 = float(input("Enter the value for Player 2(Card Counting), P_1: "))#*224
      input5 = input4 #float(input("Enter the value for Player 2, P_2: "))#*224
      input3 = int(input("Enter the number of times the game should be simulated: "))
      flag = 1
      #return(main_menu_mc2())
      low = list()
      for i in range(input3):
        deck = Deck()
        deck.build_deck()
        low.append(start_match(deck,low,input1,input2,input4,input5))
        sufString = "Games Played:"+str(len(low))+"."
        pb.printProgressBar(iteration=i,total=input3-1,prefix="Calculating...",suffix = sufString)
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
      input1 = float(input("Enter the value for Player 1(Card Counting), P_1: "))#*224
      #input2 = float(input("Enter the value for Player 1, P_2: "))#*224
      input4 = float(input("Enter the value for Player 2(Not Card Counting), P_1: "))#*224
      #input5 = float(input("Enter the value for Player 2, P_2: "))#*224
      input2 = input1
      input5 = input4
      input3 = int(input("Enter the number of times the game should be simulated: "))
      low = list()
      for i in range(input3):
        deck = Deck()
        deck.build_deck()
        low.append(start_match(deck,low,input1,input2,input4,input5,cnt=False))
        sufString = "Games Played:"+str(len(low))+"."
        pb.printProgressBar(iteration=i,total=input3-1,prefix="Calculating...",suffix = sufString)
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
    # elif(choice == 5):
    #   inters = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    #   for i in inters:
    #     for j in inters:

    elif(choice == 5):
      flag = 0
    else:
      flag = 1
      print("INVALID INPUT")
    #return(main_menu_mc2())
# deck = Deck()
# deck.build_deck()
# P1,P2 = Player("P1"),Player("P2")
# start_game(deck,P1,P2,0.5*224,0.5*224,0.7*224,0.7*224,True)
main_menu_mc2()
#print(RESULTS)