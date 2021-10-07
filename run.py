# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import os
import random
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('pontoon_data')


def main_manu():
    """
    The main menu of the game. Displays a list showing options for the user to
    choose from: Play Game, See Rules, See High Scores.
    """
    print("Welcome! You've managed to stumble upon this terminal based")
    print("version of the classic card game Pontoon.")

    while True:
        try:
            print("\n---------")
            print("MAIN MENU")
            print("---------\n")
            print("Play Pontoon:    1")
            print("Rules:           2")
            print("High Scores:     3\n")
            print("Quit:            0\n")
            menu_choice = input("Please enter your choice using the "
                                "numbers shown: ")

            if int(menu_choice) == 1:
                play_pontoon()
                break
            elif int(menu_choice) == 2:
                # rules()
                print("Rules")
                break
            elif int(menu_choice) == 3:
                # high_scores()
                print("High Scores")
                break
            elif int(menu_choice) == 0:
                print("You have quit the game, Goodbye.")
                break
            else:
                raise ValueError()

        except ValueError:
            print(f"{menu_choice} is not valid, please try again.")
            input("Press 'Enter' to return to the game.")
            clear()


def clear():
    """
    Clears the terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')


class PackOfCards:
    """
    Pack of cards class
    """
    def __init__(self):
        self.size = 52
        self.pack = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
                     5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8,
                     9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11,
                     12, 12, 12, 12, 13, 13, 13, 13]

    def random_card(self):
        """
        Returns a random card value from the pack
        """
        rand = random.randrange(self.size)
        card = self.pack[rand]
        self.size -= 1
        self.pack[rand] = self.pack[self.size]
        return card

    def reset_pack(self):
        """
        Resets the attributes of the pack
        """
        self.size = 52
        self.pack = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
                     5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8,
                     9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11,
                     12, 12, 12, 12, 13, 13, 13, 13]


class Hand:
    """
    Player's hand class
    """
    def __init__(self):
        self.pack = PackOfCards()
        self.hand = [self.pack.random_card(), self.pack.random_card()]
        self.picture_cards = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}

    def show_hand(self):
        """
        Returns a string containing the player's hand
        """
        display = ""
        for card in self.hand:
            if card == 1 or card > 10:
                display = display + "    " + self.picture_cards[card]
            else:
                display = display + "    " + str(card)

        return display

    def add_card(self):
        """
        Adds a card to the player's hand
        """
        self.hand.append(self.pack.random_card())

    def get_value(self):
        """
        Returns the current value of the player's hand
        """
        value = 0
        aces = 0
        for card in self.hand:
            if card > 10:
                value = value + 10
            elif card == 1:
                value = value + 1
                aces += 1
            else:
                value = value + card

        if aces > 0 and value + 10 <= 21:
            return value + 10
        else:
            return value

    def get_size(self):
        """
        Returns the current size of the player's hand
        """
        return len(self.hand)


class Pontoon:
    """
    Pontoon Class
    """
    def __init__(self):
        self.round_number = 0
        self.round_score = 0

    def play(self):
        while self.round_number < 5:
            self.round_number = self.round_number + 1
            hand = Hand()
            round_end = False
            bust = False
            while True:
                try:
                    clear()
                    print(f"Round {self.round_number} of 5\n")
                    print(f"Your hand is:{hand.show_hand()}\n")

                    if not round_end:
                        print(f"Current value: {hand.get_value()}\n")
                        print("Another card:    1")
                        print("Stick:           2\n")
                        print("Quit:            0\n")
                        choice = input("Please enter your choice using the "
                                       "numbers shown: ")

                        if int(choice) == 1:
                            hand.add_card()
                            if hand.get_value() > 21:
                                round_end = True
                                bust = True
                        elif int(choice) == 2:
                            round_end = True
                        elif int(choice) == 0:
                            print("You have quit the game, Goodbye.")
                            break
                        else:
                            raise ValueError()
                    else:
                        self.end_round(bust, hand.get_value(), hand.get_size())
                        break

                except ValueError:
                    print(f"{choice} is not valid, please try again.")
                    input("Press 'Enter' to return to the game.")

    def end_round(self, bust, value, size):
        if bust:
            print(f"You've bust with a score of {value}.")
            print("That's -100 points...")
            self.round_score = self.round_score - 100
        elif size == 2 and value == 21:
            print(f"You've got a pontoon with a score of {value}.")
            print("That's +100 points! Well done!")
            self.round_score = self.round_score + 100
        elif size == 5:
            print(f"You've got a five card trick with a score of {value}.")
            print("That's +50 points! Nice one!")
            self.round_score = self.round_score + 50
        else:
            print(f"You've got a score of {value}.")
            print(f"That's an extra {value} points for you.")
            self.round_score = self.round_score + value

        print(f"\nAt the end of round {self.round_number}"
              f" your total score is {self.round_score}.")
        input("Press 'Enter' to return to the game.")


# main_manu()
pontoon = Pontoon()
pontoon.play()
