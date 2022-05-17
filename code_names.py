# Select codenames ver (1. Original 2. Deep Undercover 3. Duet)
# versions available 'codenames', 'undercover', 'duet'
from cards import codenames as card_list
import parse_horsepaste as p

url = 'https://www.horsepaste.com/testingmycode'

blue, red, neutral, black = p.parse(url)

print("Blue cards: "+str(blue)+"\nRed cards: "+str(red)+"\nNeutral cards: "+str(neutral)+"\nBlack card:"+str(black))