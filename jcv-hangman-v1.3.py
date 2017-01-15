##################
# Very basic hangman game inspired by TechHire interview with Mined Minds
#  - Developed for Python 3.5.2 on Windows
##################
# John C. Verbosky
# jverbosk@gmail.com
##################
# Change log
##################
# 2016/12/08
#  V1.0
#  - MVP version of hangman game
#  - Works for words without repeated letters
##################
# 2016/12/12
#  V1.1
#  - Updated to work for words with repeated letters
#  - Updated words list
##################
# 2016/12/13
#  V1.2
#  - Added animations for winning and losing
#  - Consolidated repetitive print blocks into functions
#  - Added ability to start a new game after winning/losing
#  - Added cumulative score keeping for multiple games
#  - Updated words list
##################
# 2016/12/15
#  v1.3
#  - Consolidated keypress and animation functions
##################

# Import os to use Windows cls command to clear screen after each letter guess
import msvcrt

# Import random to use random.choice to pull random word from list
import os

# Import msvcrt for user input polling during winner animations
import random

# Import time for winner animations
import time

# List of mystery words
words = ["research", "persistence", "dedication", "curiosity", "troubleshoot", "energetic", "organization",
         "communication", "development", "loyalty", "adaptable", "creativity", "improvement", "dependable", "teamwork",
         "collaboration", "optimistic", "focused", "meticulous", "effective", "inspired"]

# Statement to select random word from the words list
word = random.choice(words)

# List to hold all letters that have been entered to guess
bucket = []

# List to hold guessed letters that are found in mystery word
build_word = []

# List to hold guessed letters that are not found in mystery word
wrong_count = []

# Variables to hold cumulative score (games won and lost)
games_won = 0
games_lost = 0


# Function to print margins
def margin(num):
    # Using "for x in range()" so it's faster to adjust margins
    for x in range(num):
        print(" ")


# Function to display the cumulative score of games won and lost
def score():
    print(" ")
    print("  Score")
    print("  -----")
    print("  Won: " + str(games_won) + "    Lost: " + str(games_lost))


# Function to display guessed and total letters
def letters():
    # Display the correctly guessed letters and placeholders
    print("  Word:     " + " ".join(build_word))
    print(" ")
    # Display all of the guessed letters
    print("  Letters:  " + " ".join(bucket))
    margin(2)


# Function to start the game
def start_game(word):
    # Clear the screen
    os.system("cls")
    # Populate the build_word list with an underscore for each letter in the mystery word
    for abc in word:
        build_word.append("_")
    # Run the user_input function to display the main "UI"
    user_input()


# Function that acts as primary starting/return point for other functions
def user_input():
    # Display the cumulative score
    score()
    # Display the current progressive hangman "image" based on wrong guesses
    hangman(len(wrong_count))
    print(" ")
    # Display guessed/total letters
    letters()
    # Prompt for collecting a letter from the user
    letter = input("  Please enter a letter:")
    # Pass the user-specified letter to the good_letter function
    good_letter(letter)


# Function that checks the user-specified letter for a few things
def good_letter(a):
    # Start by clearing the screen
    os.system("cls")
    # Check to see if letter has already been guessed and reprompt if so
    if a in bucket:
        print("  You already guessed that one - TRY AGAIN!")
        user_input()
    # Check if a single -letter- has been entered and if so, add it to the bucket list, then pass it to the letter_test function
    elif a.isalpha() and len(a) == 1:
        bucket.append(a)
        letter_test(a)
    # If multiple letters, non-alpha characters or nothing has been entered, reprompt user to try again
    else:
        print("  Enter a single letter - TRY AGAIN!")
        user_input()


# Function that receives letter from good_letter function and checks to see if letter is in the mystery word
def letter_test(b):
    # If it is in the word, pass it to the location_test function
    if b in word:
        find_location(word, b)
    # If it is not in the word, pass it to the wrong_letter function
    else:
        wrong_letter(b)


# Function that receives mystery word and user letter from letter_test function, checks to find all locations of letter
# in word, and writes location index to found list and passes to add_letter function
def find_location(string, letter):
    # List to hold the index (position) for all instances of the letter in the word
    location = []
    # Assign the index to -1 so it will become 0 when evaluated in the try clause
    # When set at 0, the index() function will miss the letter if it is the first character in the word
    last_index = -1
    while True:
        try:
            # string.index(letter_to_find, place_to_start_looking)
            # Increment the value of last_index (from -1 to 0 on first pass) and then
            # assign last_index to to the index (position) of the letter
            last_index = string.index(letter, last_index + 1)
        except ValueError:
            # If the letter is not found in the word, it will return ValueError and this loop
            # should end without writing anything to the location list
            # Note that letter_test should preclude this
            break
        else:
            # Append the index (position) of the letter to the location list on each pass
            # If the letter occurs multiple times, this list will have multiple indexes listed
            location.append(last_index)
    # Pass the user's letter and the location list to the add_letter function
    add_letter(letter, location)


# Receives letter and location list from find_location function and adds letter to the corresponding location(s)
# in the build_word list
# Finishes by calling the word_test function with the mystery word
def add_letter(letter, location_list):
    # For each instance of a letter, add that letter to the correct location in the build_word list
    for position in location_list:
        build_word[position] = letter
    # Next run the word_test function
    word_test(word)


# Function to compare the current build_word list against the mystery word
def word_test(compare):
    # Use list() to turn the mystery word into a list and if it matches the build_word list, increase
    # the games_won score by 1 and initiate the winner function with an animation count of 1
    if build_word == list(compare):
        global games_won
        games_won += 1
        winner(1)
    # If they don't match, return to user_input() for another letter
    else:
        user_input()


# Function that receives non-mystery word letter from the letter_test function and adds it to the wrong_count list
def wrong_letter(d):
    # If the wrong_count list has less than 9 letters then add the letter to the list
    if len(wrong_count) < 9:
        wrong_count.append(d)
        user_input()
    # If this is the tenth wrong letter, it's game over so increase the games_lost score by 1 and initiate
    # the loser function with an animation count of 5
    else:
        global games_lost
        games_lost += 1
        loser(5)


# Function to progressively draw the hangman stages as incorrect letters are guessed
def hangman(count):
    if count == 0:
        margin(11)
    elif count == 1:
        margin(8)
        print("   _________     ")
        margin(2)
    elif count == 2:
        margin(2)
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("   ____|____     ")
        margin(2)
    elif count == 3:
        margin(1)
        print("        ______   ")
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("   ____|____     ")
        margin(2)
    elif count == 4:
        margin(1)
        print("        ______   ")
        print("       |      |  ")
        print("       |      |  ")
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("   ____|____     ")
        margin(2)
    elif count == 5:
        margin(1)
        print("        ______   ")
        print("       |      |  ")
        print("       |      |  ")
        print("       |      O  ")
        print("       |         ")
        print("       |         ")
        print("       |         ")
        print("   ____|____     ")
        margin(2)
    elif count == 6:
        margin(1)
        print("        ______   ")
        print("       |      |  ")
        print("       |      |  ")
        print("       |      O  ")
        print("       |      |  ")
        print("       |         ")
        print("       |         ")
        print("   ____|____     ")
        margin(2)
    elif count == 7:
        margin(1)
        print("        ______   ")
        print("       |      |  ")
        print("       |      |  ")
        print("       |      O  ")
        print("       |     /|  ")
        print("       |         ")
        print("       |         ")
        print("   ____|____     ")
        margin(2)
    elif count == 8:
        margin(1)
        print("        ______   ")
        print("       |      |  ")
        print("       |      |  ")
        print("       |      O  ")
        print("       |     /|\ ")
        print("       |         ")
        print("       |         ")
        print("   ____|____     ")
        margin(2)
    elif count == 9:
        margin(1)
        print("        ______   ")
        print("       |      |  ")
        print("       |      |  ")
        print("       |      O  ")
        print("       |     /|\ ")
        print("       |     /   ")
        print("       |         ")
        print("   ____|____     ")
        margin(2)


# Function to handle endgame items
# Check to see if user has pressed a key to start a new game or exit the game between each animation frame
# Function runs after each animation frame iteration
def game_over(ani_count):
    # Check if the user is pressing a key after winning/losing
    if msvcrt.kbhit():
        # Get a single character on Windows
        key = ord(msvcrt.getch())
        # If the user presses any key except Esc, select a new word, clear all lists, and start a new game
        if key != 27:
            global word
            word = random.choice(words)
            bucket[:] = []
            build_word[:] = []
            wrong_count[:] = []
            start_game(word)
        # If the user presses the Esc key, exit the game
        elif key == 27:
            os.system("cls")
            print("Exiting game...")
    # If the user didn't press a key and the animation count is less than 5, run the winner() animation sequence
    elif ani_count < 5:
        os.system("cls")
        winner(ani_count)
    # If the user didn't press a key and the animation count is 5 or higher, run the loser() animation sequence
    else:
        os.system("cls")
        loser(ani_count)


# Function to print repetitive congratulations text in winner() animations
def congratulations():
    margin(2)
    print("       ---CONGRATULATIONS---")
    margin(1)
    print("        YOU WON THE GAME!!!")
    margin(2)


# Function that is called from the word_test function when the build_word list and the mystery word are matching
# (i.e. the user correctly guessed the word)
def winner(ani_count):
    if ani_count == 1:
        # winner animation 1
        score()
        congratulations()
        print("   \O/    \O_  \O/  _O/    \O/ ")
        print("    |    _/     |     \_    |  ")
        print("   / \    |    / \    |    / \ ")
        margin(2)
        letters()
        print(" - Press any key to play again or Esc to quit - ")
        # Wait 1/2 second for smooth animation
        time.sleep(.5)
        # Run the game_over function to see if user has pressed a key
        game_over(2)
    elif ani_count == 2:
        # winner animation 2
        score()
        congratulations()
        print("    \O_  \O/  _O/    \O/    \O_ ")
        print("   _/     |     \_    |    _/   ")
        print("    |    / \    |    / \    |   ")
        margin(2)
        letters()
        print(" \ Press any key to play again or Esc to quit \ ")
        time.sleep(.5)
        game_over(3)
    elif ani_count == 3:
        # winner animation 3
        score()
        congratulations()
        print("   \O/  _O/    \O/    \O_  \O/ ")
        print("    |     \_    |    _/     |  ")
        print("   / \    |    / \    |    / \ ")
        margin(2)
        letters()
        print(" | Press any key to play again or Esc to quit | ")
        time.sleep(.5)
        game_over(4)
    else:
        # winner animation 4
        score()
        congratulations()
        print("  _O/    \O/    \O_  \O/  _O/  ")
        print("    \_    |    _/     |     \_ ")
        print("    |    / \    |    / \    |  ")
        margin(2)
        letters()
        print(" / Press any key to play again or Esc to quit / ")
        time.sleep(.5)
        game_over(1)


# Function to print repetitive game over text in loser() animations
def sorry():
    margin(1)
    print("  SORRY - GAME OVER!")
    margin(1)


# Function that is called from the wrong_letter function
def loser(ani_count):
    if ani_count == 5:
        # loser animation 1
        score()
        margin(1)
        print("        ______      ")
        print("       |      |     ")
        print("       |      |     ")
        print("       |      O     ")
        print("       |     /|\    ")
        print("       |     / \    ")
        print("       |            ")
        print("   ____|____        ")
        sorry()
        letters()
        print(" - Press any key to play again or Esc to quit - ")
        time.sleep(.5)
        game_over(6)
    elif ani_count == 6:
        # loser animation 2
        score()
        margin(1)
        print("        ______      ")
        print("       |      |     ")
        print("       |      |     ")
        print("       |     _O_    ")
        print("       |      |     ")
        print("       |     / \    ")
        print("       |            ")
        print("   ____|____        ")
        sorry()
        letters()
        print(" \ Press any key to play again or Esc to quit \ ")
        time.sleep(.5)
        game_over(7)
    elif ani_count == 7:
        # loser animation 3
        score()
        margin(1)
        print("        ______      ")
        print("       |      |     ")
        print("       |      |     ")
        print("       |     \O/    ")
        print("       |      |     ")
        print("       |     / \    ")
        print("       |            ")
        print("   ____|____        ")
        sorry()
        letters()
        print(" | Press any key to play again or Esc to quit | ")
        time.sleep(.5)
        game_over(8)
    else:
        # loser animation 4
        score()
        margin(1)
        print("        ______      ")
        print("       |      |     ")
        print("       |      |     ")
        print("       |     _O_    ")
        print("       |      |     ")
        print("       |     / \    ")
        print("       |            ")
        print("   ____|____        ")
        sorry()
        letters()
        print(" / Press any key to play again or Esc to quit / ")
        time.sleep(.5)
        game_over(5)


# Call start_game(word) to begin the game - have fun! ^_^ /
start_game(word)
