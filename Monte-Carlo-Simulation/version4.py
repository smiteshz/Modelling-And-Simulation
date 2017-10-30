def start_game_void(dk,p1,p2,i1,i2,i3,i4,counting,first):
  if(not(counting)):
    sample_deck = Deck()
    sample_deck.build_deck()
    card = dk.draw_card()
    if(first%2==0):
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
        elif((len(dk.cards[dk.cards+p1.act_total<=21])/len(dk.cards))>=i1 and p2.finished == False):
          # print("Polly Draws and Molly hasn't finsihed")
          card = dk.draw_card()
          p1.addcard(card)
          p1.checkwin()
        elif(p2.finished == True and (((Expectation(dk.cards[dk.cards+p2.total<=21])+p2.total)>p1.act_total) or (len(dk.cards[dk.cards+p2.total<=21])/len(dk.cards)) >= i2)):
          # print("Polly Draws and Molly has finished")
          card = dk.draw_card()
          p1.addcard(card)
          p1.finished = False
          p1.checkwin()
        else:
          p1.finished = True
        #print("P2's Total",p2.act_total)
        if(len(dk.cards)==0):
          break
        if(p2.act_total>=21):
          p2.finished = True
          p2.checkwin()
          # print("Polly Holds")
        elif(len(sample_deck.cards[sample_deck.cards+p2.act_total<=21])>=i3 and p1.finished == False):
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
        winner = "Tie"
      # RESULTS.append(winner)
      return(winner)
    else:
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
        elif((len(sample_deck.cards[sample_deck.cards+p1.act_total<=21])/len(sample_deck.cards))>=i1 and p2.finished == False):
          # print("Polly Draws and Molly hasn't finsihed")
          card = dk.draw_card()
          p1.addcard(card)
          p1.checkwin()
        elif(p2.finished == True and (((Expectation(sample_deck.cards[sample_deck.cards+p2.total<=21])+p2.total)>p1.act_total) or (len(sample_deck.cards[sample_deck.cards+p2.total<=21])/len(sample_deck.cards)) >= i2)):
          # print("Polly Draws and Molly has finished")
          card = dk.draw_card()
          p1.addcard(card)
          p1.finished = False
          p1.checkwin()
        else:
          p1.finished = True
        #print("P2's Total",p2.act_total)
        if(len(dk.cards)==0):
          break
        if(p2.act_total>=21):
          p2.finished = True
          p2.checkwin()
          # print("Polly Holds")
        elif(len(dk.cards[dk.cards+p2.act_total<=21])>=i3 and p1.finished == False):
          # print("Polly Draws and Molly hasn't finsihed")
          card = dk.draw_card()
          p2.addcard(card)
          p2.checkwin()
        elif(p1.finished == True and (((Expectation(dk.cards[dk.cards+p1.total<=21])+p1.total)>p2.act_total) or len(dk.cards[dk.cards+p1.total<=21]) >= i4)):
          # print("Polly Draws and Molly has finished")
          card = dk.draw_card()
          p2.addcard(card)
          p2.finished = False
          p2.checkwin()
        else:
          # print("Polly Holds")
          p2.finished=True
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
        winner = "Tie"
      # RESULTS.append(winner)
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

      elif((len(dk.cards[dk.cards+p1.act_total<=21])/len(dk.cards))>=i1 and p2.finished == False):
        # print("Polly Draws and Molly hasn't finsihed")
        #print("Condition 1: ",len(dk.cards[dk.cards+p1.act_total<=21]))
        card = dk.draw_card()
        p1.addcard(card)
        p1.checkwin()

      elif(p2.finished == True and (((Expectation(dk.cards[dk.cards+p2.total<=21])+p2.total)>p1.act_total) or (len(dk.cards[dk.cards+p2.total<=21])/len(dk.cards)) >= i2)):
        # print("Polly Draws and Molly has finished")
        # print("Expectation:",(Expectation(dk.cards[dk.cards+p2.total<=21])+p2.total)>p1.act_total)
        # print("Condition 2:",len(dk.cards[dk.cards+p2.total<=21]))
        card = dk.draw_card()
        p1.addcard(card)
        p1.checkwin()

      else:
        p1.finished = True
        # print("I'm Holding ",p1.name)
      #print("P2's Total",p2.act_total)
      #if(p1.finished==False):
      if(len(dk.cards)==0):
        break
      if(p2.act_total>=21):
        p2.finished = True
        p2.checkwin()
        # print("Polly Holds")

      elif((len(dk.cards[dk.cards+p2.act_total<=21])/len(dk.cards))>=i3 and p1.finished == False):
        # print("Polly Draws and Molly hasn't finsihed")
        card = dk.draw_card()
        p2.addcard(card)
        p2.checkwin()

      elif(p1.finished == True and (((Expectation(dk.cards[dk.cards+p1.total<=21])+p1.total)>p2.act_total) or (len(dk.cards[dk.cards+p1.total<=21])/len(dk.cards)) >= i4)):
        # print("Polly Draws and Molly has finished")
        # print("Expectation:",(Expectation(dk.cards[dk.cards+p1.total<=21])+p1.total)>p2.act_total)
        # print("Condition 2:",len(dk.cards[dk.cards+p1.total<=21]))
        card = dk.draw_card()
        p2.addcard(card)
        p2.finished = False
        p2.checkwin()
      else:
        # print("Polly Holds")
        p2.finished=True
        # print("I'm holding", p2.name)
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
    #print("The Winner of this game is:",winner)
    #RESULTS.append(winner[0])
    return(winner)