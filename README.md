# Pontoon Game

## Contents

## Overview

This is Python terminal game based on the classic card game Pontoon, which runs in the Code Institute's mock terminal on Heroku. It is simple, easy to use, and is fun. Success is based on chance and judgement, and the player's final score is added to a leaderboard to add a further competative element.

## Game Rules

The following rules can also be seen within the game itself.

- The game starts with the player being dealt 2 random cards.
- These could be any 2 cards from a standard pack of cards.
- Card suits are not needed for this game so are not shown.
- Cards numbered 2 to 10 hold that specific value.
- Aces can have a value of 1 or 11. The optimum value used.
- Jack, Queen and King cards all have a value of 10.
- The player can request more cards, one-at-a-time, up to a total of 5.
- The aim is to get as close as possible to a score of 21 without going higher.
- The hand is considered bust if higher than 21 which results in a round score of -50 points.
- If a score of 21 is achieved with the first 2 cards that's a Pontoon, worth 100 points!
- If 5 cards are held with a total value of 21 or less that's a five card trick, worth 50 points!
- A game consists of 5 rounds with an aim of getting as many points as possible over the 5 rounds.

## User Experience

The five planes of user experience were considered during the design phase of this website, which are all outlined below.

### Strategy Plane

Here, the user goals are considered and outlined to have a clear understanding of what thought process users of the site are likely to go through, and what they might expect from the game. 

The aim is to provide ideas for potential features for the website.

#### User Goals
- __As a user I would like:__
    - to play a game based on chance and judgement.
    - to easily navigate through the game with no ambiguity.
    - to have plenty of relevant feedback.
    - to be able to compare my results with other players.
    - to be able to read the rules of the game.
    - to be able to play against the computer.

### Scope Plane

All of the user goals outlined in the strategy plane all seem to be plausible for the first release of the game. Although for this particular game, playing against the computer would add another layer of complexity which I don't feel would provide enough of a difference to the user's experience to warrant implementing at this stage. For this reason it won't be included.

### Structure Plane

The game will have a welcome message shown only when the game is first loaded. From then on, a main menu is shown with various options for the user to choose from - Play Pontoon, See Rules, See Leaderboard and Quit. They will be notified if they don't select a valid option and asked to try again.

See Rules and See Leaderboard are self explanatory, though it's worth mentioning that the terminal is cleared before either are shown, and then cleared again on returning to the main menu.

Play Pontoon takes the user to the game itself, firstly asking them for their name. This can include any characters but is limited to only 10 in length. The name is used for their score to be added to the leaderboard once a game has been completed. Next, the terminal is cleared and the main game screen is shown. The player's initial hand is shown along with its current value. The player can then choose from some options - Add another card to their hand, Stick with what the currently have, or to Quit.

Once the player has either gone bust, got a five card trick, or has chosen to stick with what they have, they are notified of their score for the round and can then continue to the next round where the process is repeated. Once all 5 rounds have been completed they're shown their final score which is then added to the leaderboard. They are then returned to the main menu.