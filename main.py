'''
simple_blackjack
Thomas Gregory
A simple game of blackjack in the terminal
'''


# The imports we will use
import random
import os
import sys


# Two simple functions we will be using throughout the app
def clear(): return os.system('clear')
# def flush(): return sys.stdout.flush()


# Globals
# Two arrays we can loop together and create a list for the deck of cards
suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
values = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six',
          'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']


# Function to Create the Deck from the two arrays above
def create_deck():
    deck = []
    for suit in suits:
        for value in values:
            card = {
                "suit": suit,
                "value": value
            }
            deck.append(card)
    return deck


# Returns the next card off of the deck and pops it from the deck list
def next_card(deck):
    return deck.pop(0)


# this function takes in a deck, returns the shuffled deck
def shuffle_deck(deck):
    shuffled_deck = random.sample(deck, len(deck))
    return shuffled_deck


# This function takes in a card from a list and returns the text string of the card
def get_card_string(card):
    return (f'[{card["value"]}] of {card["suit"]}')


def get_hand_string(hand):
    for card in hand:
        print(get_card_string(card))
    print(
        f'score(high aces): {hand_score_high(hand)} score(low aces): {hand_score_low(hand)}')


def hand_score_high(hand):
    score = 0
    for card in hand:
        score = score + get_high_numeric_value(card['value'])
    return score


def hand_score_low(hand):
    score = 0
    for card in hand:
        score = score + get_low_numeric_value(card['value'])
    return score


# This will return the numeric score of the card it takes in
def get_high_numeric_value(value):
    switcher = {
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
        'Six': 6,
        'Seven': 7,
        'Eight': 8,
        'Nine': 9,
        'Ten': 10,
        'Jack': 10,
        'Queen': 10,
        'King': 10,
        'Ace': 11
    }
    return switcher.get(value)


# This will return the numeric score of the card it takes in
def get_low_numeric_value(value):
    switcher = {
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
        'Six': 6,
        'Seven': 7,
        'Eight': 8,
        'Nine': 9,
        'Ten': 10,
        'Jack': 10,
        'Queen': 10,
        'King': 10,
        'Ace': 1
    }
    return switcher.get(value)


# This will be the function that is called when the app is started or when a game is finished
def new_game_prompt():
    clear()
    command = input('Would you like to [P]lay Blackjack or [E]xit: ')
    if command.lower() == 'p' or command.lower() == 'play':
        start_new_game()
    elif command.lower() == 'e' or command.lower() == 'exit':
        quit()
    else:
        clear()
        print(f' {command} not a recognized choice')
        new_game_prompt()


def conclusion(player_score, dealer_score, player_hand, dealer_hand):
    if dealer_score >= player_score and dealer_score <= 21:
        input(f'House wins with {dealer_score} (enter)')
        clear()
    else:
        input(f'Congratulations, You have won with {player_score} (enter)')
        clear()
    print('Dealer final hand:')
    get_hand_string(dealer_hand)
    print('\nPlayer final hand: ')
    get_hand_string(player_hand)
    input('Please hit enter to continue')


def dealer_logic(player_hand, dealer_hand, deck, player_score):
    dealer_score = 0
    while dealer_score <= player_score and dealer_score < 17:
        if hand_score_high(dealer_hand) > 21:
            dealer_score = hand_score_high(dealer_hand)
        else:
            dealer_score = hand_score_low(dealer_hand)
        clear()
        print(
            f'Score to beat: [{player_score}]   Dealer score: [{dealer_score}]')
        print('Dealer has:')
        get_hand_string(dealer_hand)
        if dealer_score < 17:
            input('Dealer has less than 17, he must hit. (enter)')
            dealer_hand.append(next_card(deck))

        elif dealer_score >= 17:
            input('Dealer has more than 16, he cannot hit. (enter)')
            clear()

    conclusion(player_score, dealer_score, player_hand, dealer_hand)

    new_game_prompt()


def decision_handler(decision, player_hand, deck, dealer_hand):
    print(f'you inputted {decision}')
    if decision.lower() == 'h' or decision.lower() == 'hit':
        player_hand.append(next_card(deck))
        return player_hand, deck
    elif decision.lower() == 's' or decision.lower() == 'stay':
        clear()
        if hand_score_high(player_hand) <= 21:
            final_score = hand_score_high(player_hand)
        else:
            final_score = hand_score_low(player_hand)
        print(f'You have chosen to stay with a score of [{final_score}]')
        print('The Dealer will now try to beat your score.')
        dealer_logic(player_hand, dealer_hand, deck, final_score)
    else:
        print('Wrong command, try again...')


def is_busted(hand):
    if hand_score_low(hand) > 21:
        return True
    else:
        return False


# Main logic of the game - called after the hands are dealt
def game_logic(dealer_hand, player_hand, deck):
    game_over = False

    if hand_score_high(dealer_hand) == 21:
        print('Dealer scored blackjack on first hand. Please try again')
        get_hand_string(dealer_hand)
        game_over = True
        new_game_prompt()

    dealer_string = (
        f'Dealer is showing a {dealer_hand[1]["value"]} of {dealer_hand[1]["suit"]} - [{get_high_numeric_value(dealer_hand[1]["value"])}]')

    while not game_over:
        clear()
        if is_busted(player_hand):
            print('Sorry! You have busted! Please try again')
            get_hand_string(player_hand)
            input('Press enter to continue...')
            game_over = True
            new_game_prompt()
        print(dealer_string)
        get_hand_string(player_hand)
        decision = input('[H]it or [S]tay: ')
        decision_handler(decision, player_hand, deck, dealer_hand)


# This fires off when a user agrees to a new game
# Create deck, shuffle deck, deal hands, send info to the logic function
def start_new_game():
    clear()
    deck = create_deck()
    shuffled_deck = shuffle_deck(deck)
    dealer_hand = [next_card(shuffled_deck), next_card(shuffled_deck)]
    player_hand = [next_card(shuffled_deck), next_card(shuffled_deck)]
    game_logic(dealer_hand, player_hand, shuffled_deck)


# Calling new_game_prompt() to start the app
new_game_prompt()
