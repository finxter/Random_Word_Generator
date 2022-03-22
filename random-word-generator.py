import random
import requests
import re
import os
from difflib import SequenceMatcher
from pathlib import Path

#GAME SETTINGS
MINIMUM_WORD_LENGTH = 5
MAXIMUM_WORD_LENGTH = 7
WORDS_FROM_FILE = False
WORD_LIST_TO_USE = 'THIRD_GRADE_WORDS'

WORD_LIST_WEB = {
  "MIT_WORDS": "https://www.mit.edu/~ecprice/wordlist.10000",
  "NORVIG_WORDS": "http://norvig.com/ngrams/count_1w.txt",
  "THIRD_GRADE_WORDS": "http://www.ideal-group.org/dictionary/p-3_ok.txt"
}

WORD_LIST_FILE = {
  "MIT_WORDS": "mit_wordlist.10000",
  "NORVIG_WORDS": "norvig_count_1w.txt",
  "THIRD_GRADE_WORDS": "p-3_ok.txt",
 
}

def get_word_list_from_web(word_site):
    response = requests.get(word_site)
    words = response.content.splitlines()
    
    return words

def format_words(words):
    if len(words) > 1:
        words_pattern = '[a-z]+'
        if type(words[0]) is bytes:
            words = [re.findall(words_pattern, word.decode('utf-8'), flags=re.IGNORECASE)[0] for word in words]
        else:
            words = [re.findall(words_pattern, word, flags=re.IGNORECASE)[0] for word in words]
    words = [word for word in words if len(word) >= MINIMUM_WORD_LENGTH and len(word) <= MAXIMUM_WORD_LENGTH]
    
    return words

def get_words_from_file(word_path):
    file_directory =  Path().absolute()
  
    word_file_path =  os.path.join(file_directory, WORD_LIST_FILE[WORD_LIST_TO_USE])
    words = open(word_file_path).readlines()
    
    return words

def shuffle_word(word):
    jumble = ""
    
    while word:
        position = random.randrange(len(word))
        jumble += word[position]
        word = word[:position] + word[(position + 1):]
    
    return jumble


def generate_unique_shuffled_word(word):
    while True:
        shuffled_word = shuffle_word(word)
        simliar_percent = SequenceMatcher(None, shuffled_word, word).ratio()

        if MINIMUM_WORD_LENGTH >= 5 and simliar_percent <= 0.5:
            break

    return shuffled_word

def main():
    print(
        """
    	Welcome to WORD JUMBLE!!!

    	Unscramble the leters to make a word.
    	(press the enter key at prompt to quit)
    	"""
    )

    if WORDS_FROM_FILE:
        words = get_words_from_file(WORD_LIST_FILE[WORD_LIST_TO_USE])
    else:
        words = get_word_list_from_web(WORD_LIST_WEB[WORD_LIST_TO_USE])
    words = format_words(words)
    
    word = random.choice(words).lower()
    shuffle_word = generate_unique_shuffled_word(word)

    correct_word = word
    print(shuffle_word)

    guess = input("Your guess: ")
    while (guess != correct_word and guess != "" ) :
        print("Sorry, that's not it")
        guess = input("Your guess: ")
    
    if guess == correct_word:
        print("That's it, you guessed it!\n")
        print("Thanks for playing")
  
    input("\n\nPress the enter key to exit")

main()