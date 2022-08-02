from calendar import c
from bs4 import BeautifulSoup
import requests
import random
from time import sleep

all_quotes = []
base_url = "http://quotes.toscrape.com"
url = "/page/1"
game_state = True

while game_state:

    while url:
        
        page = requests.get(base_url + url)
        print("Now Scraping {}{}....".format(base_url, url))
        soup = BeautifulSoup(page.content, 'html.parser')
        quotes = soup.find_all('div', {'class': 'quote'})

        for quote in quotes:
            all_quotes.append({
                "text":quote.find(class_="text").get_text(),
                "author":quote.find(class_="author").get_text(),
                "link":quote.find("a")["href"]
            })
        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        #sleep(1) # waits 1 second before scraping

    random_quote = random.choice(all_quotes)
    bio = BeautifulSoup(requests.get(base_url + random_quote.get("link")).content, 'html.parser')
    hints = [
        "They were born {} on {}.".format(bio.find(class_="author-born-location").get_text(), bio.find(class_="author-born-date").get_text()),
        "Their initals are {}. {}.".format(random_quote.get("author").split(" ")[0][0], random_quote.get("author").split(" ")[1][0]),
        "Their first name is {} characters long.".format(len(random_quote.get("author").split(" ")[0]))
    ]

    print("{}".format("-"*len(random_quote["text"])))
    print("Who said the following:")
    print("{}".format("-"*len(random_quote["text"])))
    print(random_quote.get("text"))
    print("{}".format("-"*len(random_quote["text"])))

    guesses_left = 4
    user_response = input("Answer: ")
    result = "Loser!"

    while guesses_left > 1:

        guesses_left -= 1

        if user_response == random_quote.get("author"):
            result = "Winner!"
        else:
            print("Nope. Here's a hint:")
            print(hints.pop())
            print("Chances left: {}".format(guesses_left))
            user_response = input("Next Guess: ")

    print("{} The answer is {}.".format(result, random_quote["author"]))

    play_again = input("Would you like to play again? (Y/N)")

    if play_again == "N":
        game_state = False
