import os
import random
import gspread
from google.oauth2.service_account import Credentials

# CREDIT-------------
# This section of code - used to access google sheets - was taken from
# the code insitue's Love Sandwiches walkthrough project.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('pontoon_data')
# END OF CREDIT------


def main_manu():
    """
    The main menu of the game. Displays a list showing options for the user to
    choose from: Play Game, See Rules, See Leaderboard. The user can also quit.
    """
    print("Welcome! You've managed to stumble upon this terminal based")
    print("version of the classic card game Pontoon.\n")
    pontoon = Pontoon()

    while True:
        try:
            print("---------")
            print("MAIN MENU")
            print("---------\n")
            print("Play Pontoon:    1")
            print("Rules:           2")
            print("Leaderboard:     3\n")
            print("Quit:            0\n")
            menu_choice = input("Please enter your choice using the "
                                "numbers shown: ")

            if int(menu_choice) == 1:
                pontoon.play()
            elif int(menu_choice) == 2:
                show_rules(pontoon.BUST_SCORE, pontoon.PONTOON_SCORE,
                           pontoon.FIVE_TRICK)
            elif int(menu_choice) == 3:
                show_leaderboard()
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
     - CREDIT - this code was found on stack overflow:
     - https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def show_rules(bust, pontoon, five):
    """
    Show rules function displays the rules of the game afer clearing
    the terminal. It has 3 parameters which represent the value
    of certain hands of the game.
    """
    clear()
    print("-----")
    print("RULES")
    print("-----")
    print("- The game starts with the player being dealt 2 random cards.")
    print("- These could be any 2 cards from a standard pack of cards.")
    print("- Card suits are not needed for this game so are not shown.")
    print("- Cards numbered 2 to 10 hold that specific value.")
    print("- Aces can have a value of 1 or 11. The optimum value used.")
    print("- Jack, Queen and King cards all have a value of 10.")
    print("- The player can request more cards, one-at-a-time, up to a")
    print("  total of 5.")
    print("- The aim is to get as close as possible to a score of 21")
    print("  without going higher.")
    print("- The hand is considered bust if higher than 21 which results")
    print(f"  in a round score of {bust} points.")
    print("- If a score of 21 is achieved with the first 2 cards that's")
    print(f"  a Pontoon, worth {pontoon} points!")
    print("- If 5 cards are held with a total value of 21 or less that's")
    print(f"  a five card trick, worth {five} points!")
    print("- A game consists of 5 rounds with an aim of getting as many")
    print("  points as possible over the 5 rounds.")
    input("\nPress 'Enter' to return to the Main Menu.")
    clear()


def show_leaderboard():
    """
    Show leaderboard displays the leaderboard of previous players scores
    up to a maximum of the top 10.
    """
    clear()
    worksheet = SHEET.worksheet("scores")
    worksheet.sort((2, 'des'))

    scores = []
    leaderboard_size = 0
    for ind in range(1, 3):
        column = worksheet.col_values(ind)
        scores.append(column)

    if len(scores[0]) < 10:
        leaderboard_size = len(scores[0])
    else:
        leaderboard_size = 10

    print("-----------")
    print("LEADERBOARD")
    print("-----------\n")

    for ind in range(1, leaderboard_size + 1):
        print(f"{str(ind)+'.':<6}{scores[0][ind]:<12}{scores[1][ind]:>4}")

    input("\nPress 'Enter' to return to the Main Menu.")
    clear()


class PackOfCards:
    """
    Pack of cards class represents a pack of 52 cards. Suits not
    included. It can generate a random card from the pack and reset
    its state if needed.
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
    Hand class represents a player's hand of cards, starting with 2.
    It can take a PackOfCards object as an arguement, though this is not
    required as it declares its own if omitted.
    """
    def __init__(self, pack=PackOfCards()):
        self.pack = pack
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
    Pontoon Class represents the game pontoon. It has some constant variables
    declared for all pontoon objects which affect the game's scoring system.
    It contains the main loops of the game and updates the user appropriately
    at the end of each round and game. It also writes players' scores to the
    leaderboard.
    """
    PONTOON_SCORE = 100
    FIVE_TRICK = 50
    BUST_SCORE = -50

    def __init__(self):
        self.round_number = 0
        self.round_score = 0
        self.rounds = {
            "Name": "",
            "Total": 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }

    def play(self):
        """
        Play contains the main loop of the game. It loops through 5 rounds
        unless the player quits.
        """
        self.request_name()
        self.round_number = 0
        self.round_score = 0
        while self.round_number < 5:
            self.round_number = self.round_number + 1
            hand = Hand()
            round_end = False
            bust = False
            quit = False
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
                            elif hand.get_size() == 5:
                                round_end = True
                        elif int(choice) == 2:
                            round_end = True
                        elif int(choice) == 0:
                            quit = True
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

            if quit:
                break

    def end_round(self, bust, value, size):
        """
        End round is called at the end of each round and when all 5 rounds
        have been completed. It takes 3 parameters which determine what
        it outputs to the user.
        """
        if bust:
            print(f"You've bust with a score of {value}. "
                  f"That's {self.BUST_SCORE} points...")
            self.round_score = self.round_score + self.BUST_SCORE
            self.rounds[self.round_number] = self.BUST_SCORE
        elif size == 2 and value == 21:
            print(f"You've got a pontoon with a score of {value}. "
                  f"That's +{self.PONTOON_SCORE} points! Well done!")
            self.round_score = self.round_score + self.PONTOON_SCORE
            self.rounds[self.round_number] = self.PONTOON_SCORE
        elif size == 5:
            print(f"You've got a five card trick with a score of {value}. "
                  f"That's +{self.FIVE_TRICK} points! Nice one!")
            self.round_score = self.round_score + self.FIVE_TRICK
            self.rounds[self.round_number] = self.FIVE_TRICK
        else:
            print(f"You got a score of {value}. "
                  f"That's {value} points added to your total.")
            self.round_score = self.round_score + value
            self.rounds[self.round_number] = value

        if self.round_number == 5:
            print(f"\nThat's all 5 rounds complete! "
                  f"Your total score is {self.round_score}.\n")
            self.rounds["Total"] = self.round_score
            self.update_leaderboard()
            clear()
        else:
            print(f"\nAt the end of round {self.round_number}"
                  f" your total score is {self.round_score}.\n")
            input(f"Press 'Enter' to continue to round "
                  f"{self.round_number + 1}.")

    def request_name(self):
        """
        Request name askes the user for their name.
        A maximum of 10 characters is allowed.
        """
        while True:
            try:
                clear()
                print("You've chosen to play Pontoon!\n")
                name = input("Please tell us your name: ")
                if len(name) <= 10:
                    self.rounds["Name"] = name
                    break
                else:
                    raise ValueError()

            except ValueError:
                print("That has too many characters!")
                print("A maximum of 10 characters is allowed.")
                input("Press 'Enter' to try again.")

    def update_leaderboard(self):
        """
        Update leaderboard uses the current state of the pontoon object
        to update the google sheet which contains the leaderboard
        information.
        """
        worksheet = SHEET.worksheet("scores")
        worksheet.append_row(list(self.rounds.values()))
        worksheet.sort((2, 'des'))
        print("Your score has been added to the leaderboard!\n")
        input("Press 'Enter' to continue.")


main_manu()
