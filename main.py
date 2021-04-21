import functools
import os
import random


# TODO
# look into polymorphism / inheritance, idk what it's called but the python equivalent of extends in js.
# because the Dealer and Player classes here share a lot of methods

class Dealer:
  def __init__(self):
    suits = ["spades", "clubs", "diamonds", "hearts"]
    self.deck =[Card(number, suit) 
                for suit in suits 
                  for number in [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 11]]
    self.hand = []
  
  def get_score(self):
    numbers = [card.number for card in self.hand]

    # changes aces from 11s to 1s until the total score drops below 22, if ever.
    if sum(numbers) > 21 and 11 in numbers:
      while 11 in numbers:
        numbers[numbers.index(11)] = 1
        if sum(numbers) <= 21:
          break
    
    return sum(numbers)


  def __str__(self):
    return_string = ""
    for card in self.deck:
      return_string += f"{card.__str__()} \n"
    return return_string
    
  def receive_card(self, card):
    self.hand.append(card)
  
  #This needs to be remade, it's messy
  def shuffle(self):
    for i in range(len(self.deck)):
      ran_card_number = random.randrange(0, len(self.deck))
      self.deck[i], self.deck[ran_card_number] = self.deck[ran_card_number], self.deck[i]

  def deal_card(self, player):
    player.receive_card(self.deck.pop(0))

  
class Player:
  def __init__(self):
    self.hand = []

  def __str__(self):
    return_string = ""
    for card in self.hand:
      return_string += f"{card.__str__()} \n"
    return return_string

  def receive_card(self, card):
    self.hand.append(card)

  def get_score(self):
    numbers = [card.number for card in self.hand]

    # changes aces from 11s to 1s until the total score drops below 22, if ever.
    if sum(numbers) > 21 and 11 in numbers:
      while 11 in numbers:
        numbers[numbers.index(11)] = 1
        print(numbers)
        if sum(numbers) <= 21:
          print(numbers)
          break
    
    return sum(numbers)

class Card:
  def __init__(self, number, suit):
    self.number = number
    self.suit = suit

  def __str__(self):
    return f"{self.number} of {self.suit}"


class Game:
  def __init__(self, player, dealer):
    self.player = player
    self.dealer = dealer
    self.winner = None
  

  #asks the player if they want to hit again and returns boolean
  def another_card(self):
    player_input = None

    # "" allows the player to just press enter to hit again. not sure if this is error prone though
    while player_input not in ["Y", "y", "", "N", "n"]:
      player_input = input("would you like to get another card? (y/n)\n")
    
    return player_input in ["Y", "y", ""]


  def show_hands(self, show_dealer_hand):
    print("Dealer:")
    if show_dealer_hand:
      for card in self.dealer.hand:
        print(card)
    else:
      print(self.dealer.hand[0])
    print("\n")
    print("Player:")
    print(self.player)

  # TODO 
  # use destruring, got a lot of "self." going on
  def play(self):
    self.dealer.shuffle()

    self.dealer.deal_card(self.player)
    self.dealer.deal_card(self.player)
    self.dealer.deal_card(self.dealer)
    self.dealer.deal_card(self.dealer)

    while not self.winner:
      # clear the console
      os.system('clear')
      
      self.show_hands(show_dealer_hand=False)

      if self.player.get_score() > 21:
        self.winner = "dealer" # should this asign self.winner to self.dealer maybe?
        break # not necessary but good for clarity?

      if self.another_card():
        self.dealer.deal_card(self.player)
      else:
        self.winner = "dealer" if self.dealer.get_score() > self.player.get_score() else "player"

    os.system('clear')
    self.show_hands(show_dealer_hand=True)

    print(f"{self.winner} wins!")    


#--------------------------------

player1 = Player()
dealer1 = Dealer()

game1 = Game(player1, dealer1)

dealer1.shuffle()

game1.play()


# Blackjack rules cos I don't actually know them and I just searched them up
#
# Goal is to beat the dealer but not go over 21
#
# Dealer deals 1 card face up to each player and themselves
#
# players are dealt 1 more card face up and the dealer one more face down
#
# players can then ask for as many more cards as they want so long as they don't go over 21 (rememebering the special case of aces)
# 
# when the player stays. the dealer deals his hand.
# 
# if he has less than 17 points, he has to get another card.
#
# then we compare to see who won. 

