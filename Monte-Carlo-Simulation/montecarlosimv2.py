import numpy as np

def Expectation(sampleset):
  """Calculates the Expectation of the PD named SampleSet"""
  division = sampleset/len(sampleset)
  return(np.sum(division))
def get_value(card_type):
  try:
    if(int(card_type[0])==1):
      return (11)
    else:
      return(int(card_type[0]))
  except ValueError:
    return(10)
class Player:
  def __init__(self,name):
    self.name = name
    self.finished = False
    self.hand = np.zeros(10)
    self.total = 0
    self.c_to_win = 21 
    self.lastcard = 0
    self.win = 2
    self.shown_total = 0
    self.strategy = "Naive"
  def addcard(self,crd,index=0):
    if(index == 0):
      self.hand[self.lastcard] = crd
    else:
      self.hand[index] = crd
    self.shown_total = np.sum(self.hand[1:])
    self.total = np.sum(self.shown_total+self.hand[0])
    self.c_to_win = 21-self.total
    self.lastcard +=1
    self.checkwin()
  def checkwin(self):
    if(self.total == 21):
      self.win = 1
      self.finished = True
    elif(self.total >= 21):
      self.finished = True
      self.win = 3
    else:
      self.finsihed = False
class Deck:
  def __init__(self):
    self.cards = np.array([])
    self.head = 0
    self.used = np.array([])
    self.exhausted = False

  def build_deck_with_array(self,values):
    self.cards = values

  def build_deck(self):
    cards = np.array(['1','2','3','4','5','6','7','8','9','T','J','Q','K'])
    suites = np.array(['H','C','S','D'])
    deck = list()
    for i in suites:
      for j in cards:
        deck.append([j+i])
      deck.append(["1"+i])
    deck = np.repeat(deck,4)
    deck_vals = np.array([])
    for i in deck:
      deck_vals = np.append(deck_vals,get_value(i))
    self.cards = deck_vals
  def draw_card(self):
    np.random.seed()
    ind = np.random.choice(len(self.cards))
    chosen = self.cards[ind]
    np.append(self.used,chosen)
    self.cards = np.delete(self.cards,ind)
    try:
      check = np.random.choice(len(self.cards))
    except ValueError:
      self.exhausted = True
    return(chosen)

  def draw_card_seq(self,delete=True):
    chosen = self.cards[0]
    if(delete):
      self.cards = np.delete(self.cards,0)
def match(p1,p2,deck,seq,ip1,ip2):
  players = list([p1,p2])
  turn = 1
  players[seq].addcard(deck.draw_card())
  players[1-seq].addcard(deck.draw_card())
  while(not(players[seq].finished) or not(players[1-seq].finished) or deck.exhausted==True):
      if(not(players[1-seq].finished) and (np.count_nonzero(deck.cards[players[seq].total+deck.cards<=21])>ip1)):
        if(not(deck.exhausted)):
          players[seq].addcard(deck.draw_card())
      elif(players[1-seq].finsihed and (Expectation(deck.cards[deck.cards+players[1-seq].shown_total<21])+players[1-seq].shown_total)>players[seq].total):
        if(deck.exhausted == False):
          players[seq].addcard(deck.draw_card())
      elif(players[1-seq].finished and (np.count_nonzero(deck.cards[players[seq].total+deck.cards<=21])>=ip2)):
        if(deck.exhausted == False):
          players[seq].addcard(deck.draw_card())
      if(players[seq].win!=2):
        if(players[seq].finished == False and (np.count_nonzero(deck.cards[players[1-seq].total+deck.cards<=21])>ip1)):
          if(deck.exhausted == False):
            players[1-seq].addcard(deck.draw_card())
        elif(players[seq].finsihed and (Expectation(deck.cards[deck.cards+players[seq].shown_total<21])+players[seq].shown_total)>players[1-seq].total):
          if(deck.exhausted==False):
            players[1-seq].addcard(deck.draw_card())
        elif(players[seq].finished and (np.count_nonzero(deck.cards[players[1-seq].total+deck.cards<=21])>=ip2)):
          if(deck.exhausted==False):
            players[1-seq].addcard(deck.draw_card())
  if(players[seq].win == 1):
    winner = players[seq].name
  elif(players[1-seq].win == 1):
    winner = players[seq].name
  elif(players[seq].total>players[1-seq].total and players[seq].win!=2):
    winner = players[seq].name
  elif(players[seq].total<players[1-seq].total and players[1-seq].win!= 2):
    winner = players[1-seq].name
  else:
    winner = "Draw"

  return(winner,players[seq],players[1-seq])
def play(dk,list_of_winners,ips):
  list_of_winners=list()
  sequence = 0
  while(dk.exhausted == False):
    pl1,pl2=Player("Molly"),Player("Polly")
    winner,pl1,pl2 = match(pl1,pl2,dk,sequence,ips[0],ips[1])
    sequence = 1-sequence
    list_of_winners.append(winner)
  return(list_of_winners)
low=list()
inputs=list([0.5,0.7])
for i in range(1):
  dck = Deck()
  dck.build_deck()
  low = play(dck,low,inputs)
print(low)