import random
import time

def reset_deck():
    global draw_pile
    global cards_remain
    global player_cards
    global dealer_cards
    cards_remain = 52
    player_cards = []
    dealer_cards = []
    draw_pile = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 
           10, 10, 10, 10, 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A']

def deal():
    global card
    global cards_remain
    global player_cards
    global dealer_cards
    global player_total   
    for index in range(1,5):
        card = random.randint(0,cards_remain-1)
        if index < 3:
            player_cards.append((draw_pile[card]))
        elif index > 2:
            dealer_cards.append((draw_pile[card]))
        cards_remain -= 1
        del draw_pile[card]
    player_total_math()
    dealer_total_math()
    print("Your cards: " + str(player_cards) + " = " + str(player_total))
    print("Dealer's cards: " + "[X, " + str(dealer_cards[1]) + "]")

def player_total_math():
    global player_total
    player_total = (sum([x for x in player_cards if isinstance(x, int)]))
    for index in range(len(player_cards)):
        if isinstance(player_cards[index], str) and ('J' in player_cards[index] or 'Q' in player_cards[index] or 'K' in player_cards[index]):
            player_total += 10
        elif isinstance(player_cards[index], str) and 'A' in player_cards[index]:
            player_total += 11
    if 'A' in player_cards and player_total > 21:
        player_total -= 10

def dealer_total_math():
    global dealer_total
    dealer_total = (sum([x for x in dealer_cards if isinstance(x, int)]))
    for index in range(len(dealer_cards)):
        if isinstance(dealer_cards[index], str) and ('J' in dealer_cards[index] or 'Q' in dealer_cards[index] or 'K' in dealer_cards[index]):
            dealer_total += 10
        elif isinstance(dealer_cards[index], str) and 'A' in dealer_cards[index]:
            dealer_total += 11
    if 'A' in dealer_cards and dealer_total > 21:
        dealer_total -= 10 

def check_win():
    global win
    global standing
    global money
    win = 4
    player_total_math()
    dealer_total_math()
    if 'A' in player_cards:
        if 10 in player_cards or 'J' in player_cards or 'Q' in player_cards or 'K' in player_cards:
            win +=2
    if 'A' in dealer_cards:
        if 10 in dealer_cards or 'J' in dealer_cards or 'Q' in dealer_cards or 'K' in dealer_cards:
            win /= 2
    if win == 6:
        print("You got a blackjack!")
        stand()
    elif win == 2:        
        print("Dealer's cards: " + str(dealer_cards) + " = " + str(dealer_total))
        print("The dealer got a blackjack.")
        standing = True
        money -= bet
    elif win == 3:
        print("Dealer's cards: " + str(dealer_cards))
        print("Both you and the dealer got blackjack. That's a push!")

def hit_or_stand():
    global decision
    decision = 0
    while decision != 'hit' and decision != 'stand':
        decision = input("hit or stand: ")
        if decision == 'hit':
            hit()
        elif decision == 'stand':
            stand()
        else:
            print("Make sure to only type 'hit' or 'stand'")

def hit():
    global card
    global cards_remain
    card = random.randint(0,cards_remain-1)
    player_cards.append((draw_pile[card]))
    del draw_pile[card]
    cards_remain -= 1
    player_total_math()
    print("Your cards: " + str(player_cards) + " = " + str(player_total))
    if player_total == 21:
        stand()

def stand():
    global card
    global cards_remain
    global standing
    standing = True    
    dealer_total_math()
    print("Dealer's cards: " + str(dealer_cards) + " = " + str(dealer_total))
    while dealer_total < 17:
        time.sleep(1)
        card = random.randint(0,cards_remain-1)
        dealer_cards.append((draw_pile[card]))
        del draw_pile[card]
        cards_remain -= 1
        dealer_total_math()
        print("Dealer's cards: " + str(dealer_cards) + " = " + str(dealer_total))

def declare_winner():
    global money
    if player_total > 21:
        print("You busted!")
        money -= bet
    elif dealer_total > 21:
        print("You win! The dealer busted!")
        money += bet
    elif player_total < dealer_total:
        print("The dealer beat you!")
        money -= bet
    elif player_total == dealer_total:
        print("That's a push!")
    else:
        print("You beat the dealer!")
        money += bet

def game_loop():
    global money
    global plays
    global bet
    global player_total
    global dealer_total
    global standing
    while plays < 17:
        money = int(100000/2 ** plays)
        plays += 1
        while money > 0:
            print("Balance: $" + str(money))
            try:
                bet = int(input("How much do you want to bet? $"))
                if bet <= money:
                    player_total = 0
                    dealer_total = 0
                    standing = False
                    reset_deck()
                    deal()
                    time.sleep(1)
                    check_win()
                    while player_total < 21 and standing == False:
                        hit_or_stand()
                    declare_winner()
                    time.sleep(1)
                else:
                    print("You have exceeded your maximum bet. Please try again.")
                    time.sleep(2)
            except ValueError:
                print("You can't bet letters or special characters. Please try again.")
                time.sleep(2) 
        if plays < 17:
            print("You lost all your money.")
            time.sleep(2)
            if input("Enter 'try again' for redemption: ") == 'try again':
                game_loop()

plays = 0 
game_loop()