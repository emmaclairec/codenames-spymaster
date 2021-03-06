#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
import wikipedia as wiki
import json
#from cards import CODENAMES_DICT
#import time
#from random import randint


def get_wiki_degrees(page_links):
    print("Getting link paths...")
    result_link_chains = []
    pathcount = 0
    for frst_deg_link in page_links:
        for scnd_deg_link in wiki.page(frst_deg_link).links:
            for thrd_deg_link in wiki.page(scnd_deg_link).links:
                result_link_chains.append([frst_deg_link, scnd_deg_link, thrd_deg_link])
                pathcount += 1
                print("Path " + str(pathcount) + "established")
    return result_link_chains


def parse_wiki_content(content):
    newstr = ""
    for w in word_tokenize(content):
        if w not in set(stopwords.words('english')):
            newstr += str(w)
    return newstr


def for_wiki_page(result, c_dict, l_dict):
    cont = parse_wiki_content(wiki.page(result).content)
    # links = get_wiki_degrees(wiki.page(result).links)
    c_dict.update({result: cont})
    # l_dict.update({result: links})


def get_wiki_data(words):
    content_dict = {}
    links_dict = {}
    for word in words:
        print("Searching for: " + word)
        search_results = wiki.search(word, results=5)
        print("Search results: " + str(search_results))
        result_cont_dict = {}
        result_link_dict = {}
        for result in search_results:
            try:
                print("Getting info for: " + result)
                for_wiki_page(result, result_cont_dict, result_link_dict)
                time.sleep(randint(5, 15))
            except wiki.DisambiguationError as e:
                print("DisambiguationError for: " + result)
                for option in e.options:
                    try:
                        time.sleep(randint(5, 15))
                        print("Getting info for: " + option)
                        for_wiki_page(option, result_cont_dict, result_link_dict)
                    except wiki.DisambiguationError:
                        pass
        content_dict.update({word: result_cont_dict})
        # links_dict.update({word: result_link_dict})
    return [content_dict, links_dict]


def export_wiki_data(content_xport, content, links_xport, links):
    with open(content_xport, 'a') as file1:
        file1.write(json.dumps(content))
        file1.close()
    # with open(links_xport, 'a') as file2:
        # file2.write(json.dumps(links))
        # file2.close()


UNIQUE_WORDS = ({'ACE', 'ACID', 'AFRICA', 'AGENT', 'AIR', 'ALASKA', 'ALCOHOL', 'ALIEN', 'ALPS', 'AMAZON',
                 'AMBULANCE', 'AMERICA', 'ANCHOR', 'ANGEL', 'ANIMAL', 'ANT', 'ANTARCTICA', 'ANTHEM', 'APPLE', 'APPLES',
                 'APRON', 'ARM', 'ARMOR', 'ARMY', 'ASH', 'ASHES', 'ASS', 'ASTRONAUT', 'ATLANTIS', 'ATTIC',
                 'AUSTRALIA', 'AVALANCHE', 'AXE', 'AZTEC', 'BABY', 'BACK', 'BACON', 'BAKED', 'BALL', 'BALLOON',
                 'BALLS', 'BANANA', 'BAND', 'BANG', 'BANK', 'BAR', 'BARBECUE', 'BARK', 'BARTENDER', 'BASS', 'BAT',
                 'BATH', 'BATTERY', 'BATTLE', 'BATTLESHIP', 'BAY', 'BEACH', 'BEAM', 'BEAN', 'BEANS', 'BEAR', 'BEARD',
                 'BEAT', 'BEAVER', 'BED', 'BEE', 'BEEF', 'BEER', 'BEHIND', 'BEIJING', 'BELL', 'BELT', 'BENCH', 'BENDER',
                 'BERLIN', 'BERMUDA', 'BERRY', 'BICYCLE', 'BIG BANG', 'BIG BEN', 'BIKINI', 'BILL', 'BISCUIT',
                 'BISCUITS', 'BISEXUAL', 'BITCH', 'BLACK', 'BLACKSMITH', 'BLADE', 'BLIND', 'BLING', 'BLIZZARD', 'BLOCK',
                 'BLONDE', 'BLOW', 'BLUES', 'BLUSH', 'BOARD', 'BODY', 'BOIL', 'BOLT', 'BOMB', 'BOND', 'BONDAGE', 'BONE',
                 'BONG', 'BONSAI', 'BOOB', 'BOOK', 'BOOM', 'BOOT', 'BOOTY', 'BOOZE', 'BOSS', 'BOTTLE', 'BOTTOM', 'BOW',
                 'BOWL', 'BOWLER', 'BOX', 'BOXER', 'BOXERS', 'BOY', 'BRA', 'BRAIN', 'BRASS', 'BRAZIL', 'BREAD', 'BREAK',
                 'BREAST', 'BRICK', 'BRIDE', 'BRIDGE', 'BRIEFS', 'BROTHER', 'BROWN', 'BROWNIE', 'BRUSH', 'BUBBLE',
                 'BUCK', 'BUCKET', 'BUFFALO', 'BUG', 'BUGLE', 'BULB', 'BUNK', 'BURN', 'BUSH', 'BUST', 'BUTT', 'BUTTER',
                 'BUTTERFLY', 'BUTTON', 'CABLE', 'CABOOSE', 'CAESAR', 'CAKE', 'CALF', 'CAMP', 'CANADA', 'CANDLE',
                 'CANE', 'CANNONS', 'CAP', 'CAPITAL', 'CAPTAIN', 'CAR', 'CARD', 'CARPET', 'CARROT', 'CASINO', 'CAST',
                 'CASTLE', 'CAT', 'CATCHER', 'CAVE', 'CELL', 'CENTAUR', 'CENTER', 'CHAIN', 'CHAINS', 'CHAIR', 'CHALK',
                 'CHAMPAGNE', 'CHANGE', 'CHAPS', 'CHARGE', 'CHECK', 'CHEEK', 'CHEESE', 'CHERRY', 'CHEST', 'CHICK',
                 'CHINA', 'CHIP', 'CHOCOLATE', 'CHOKE', 'CHRISTMAS', 'CHUBBY', 'CHURCH', 'CIGAR', 'CIGARETTE', 'CIRCLE',
                 'CLAM', 'CLAP', 'CLEOPATRA', 'CLIFF', 'CLOAK', 'CLOCK', 'CLOUD', 'CLUB', 'COACH', 'COAST', 'COCK',
                 'COCKTAIL', 'CODE', 'COFFEE', 'COLD', 'COLLAR', 'COLUMBUS', 'COMB', 'COMET', 'COMIC', 'COMMANDO',
                 'COMPOUND', 'COMPUTER', 'CONCERT', 'CONDOM', 'CONDUCTOR', 'CONE', 'CONTRACT', 'COOK', 'COOZIE',
                 'COPPER', 'COTTON', 'COUCH', 'COUGAR', 'COUNTRY', 'COUPLE', 'COURT', 'COVER', 'COW', 'COWBOY',
                 'COWGIRL', 'COYOTE', 'CRAB', 'CRABS', 'CRACK', 'CRAFT', 'CRANE', 'CRAP', 'CRASH', 'CREAM', 'CRICKET',
                 'CROSS', 'CROW', 'CROWN', 'CRUSADER', 'CRYSTAL', 'CUCKOO', 'CUCUMBER', 'CUDDLE', 'CUFFS', 'CURRY',
                 'CYCLE', 'CZECH', 'DADDY', 'DAME', 'DANCE', 'DASH', 'DATE', 'DAY', 'DEATH', 'DECK', 'DEGREE', 'DELTA',
                 'DENTIST', 'DESK', 'DIAMOND', 'DIARRHEA', 'DICE', 'DICK', 'DILDO', 'DINOSAUR', 'DIRECTOR', 'DISEASE',
                 'DISK', 'DOCTOR', 'DOG', 'DOGGY', 'DOLL', 'DOLLAR', 'DOMINATE', 'DONKEY', 'DOOR', 'DOUCHE', 'DOWN',
                 'DRAFT', 'DRAG', 'DRAGON', 'DRAWING', 'DREAM', 'DRESS', 'DRESSING', 'DRILL', 'DRIVER', 'DRONE', 'DROP',
                 'DRUM', 'DRUNK', 'DRYER', 'DUCK', 'DUST', 'DWARF', 'EAGLE', 'EAR', 'EARTH', 'EARTHQUAKE', 'EASTER',
                 'EAT', 'EDEN', 'EGG', 'EGYPT', 'EINSTEIN', 'ELEPHANT', 'EMBASSY', 'EMISSION', 'ENGINE', 'ENGLAND',
                 'ESCORT', 'EUROPE', 'EXPERIMENT', 'EYE', 'EYES', 'FACE', 'FACIAL', 'FAIR', 'FALL', 'FAN', 'FANTASY',
                 'FARM', 'FATTY', 'FEATHER', 'FECAL', 'FENCE', 'FETISH', 'FEVER', 'FIDDLE', 'FIELD', 'FIGHTER',
                 'FIGURE', 'FILE', 'FILM', 'FINGER', 'FIRE', 'FISH', 'FIST', 'FLAG', 'FLASH', 'FLAT', 'FLESH', 'FLOOD',
                 'FLOOR', 'FLOWER', 'FLUFF', 'FLUTE', 'FLY', 'FOAM', 'FOG', 'FOOT', 'FORCE', 'FORESKIN', 'FOREST',
                 'FORK', 'FRANCE', 'FREAK', 'FRECKLES', 'FRENCH', 'FRICTION', 'FROG', 'FROST', 'FUEL', 'FURRY',
                 'G-SPOT', 'GAG', 'GAME', 'GANG', 'GANGBANG', 'GANGSTER', 'GARDEN', 'GAS', 'GASH', 'GAY', 'GEAR',
                 'GENIE', 'GENIUS', 'GERBIL', 'GERMANY', 'GHOST', 'GIANT', 'GIGOLO', 'GIRL', 'GLACIER', 'GLASS',
                 'GLASSES', 'GLOVE', 'GOAT', 'GOLD', 'GOLDILOCKS', 'GOLF', 'GOOSE', 'GOVERNOR', 'GRACE', 'GRANDMA',
                 'GRASS', 'GREECE', 'GREEN', 'GREENHOUSE', 'GROOM', 'GROPE', 'GROUND', 'GROUP', 'GUITAR', 'GUM',
                 'GYMNAST', 'HAIR', 'HALLOWEEN', 'HAM', 'HAMBURGER', 'HAMMER', 'HAMSTER', 'HAND', 'HAWAII', 'HAWK',
                 'HEAD', 'HEADBOARD', 'HEADLIGHTS', 'HEART', 'HELICOPTER', 'HELL', 'HELMET', 'HERB', 'HERCULES', 'HIDE',
                 'HIGH', 'HIMALAYAS', 'HIT', 'HOLE', 'HOLLYWOOD', 'HOMER', 'HOMERUN', 'HONEY', 'HOOD', 'HOOK', 'HOOKER',
                 'HOOTERS', 'HORN', 'HORNY', 'HORSE', 'HORSESHOE', 'HOSE', 'HOSPITAL', 'HOT', 'HOTEL', 'HOUSE', 'HUMP',
                 'HURL', 'ICE', 'ICE AGE', 'ICE CREAM', 'ICELAND', 'IGLOO', 'INCH', 'INDIA', 'INK', 'INTERN', 'IRON',
                 'IVORY', 'JACK', 'JAIL', 'JAM', 'JAZZ', 'JELLYFISH', 'JERK', 'JET', 'JEWELLER', 'JEWELS',
                 'JOAN OF ARC', 'JOB', 'JOCKEY', 'JOHN', 'JOHNSON', 'JOINT', 'JOKER', 'JOYSTICK', 'JUDGE', 'JUGS',
                 'JUICE', 'JUMPER', 'JUPITER', 'KANGAROO', 'KEG', 'KETCHUP', 'KEY', 'KICK', 'KID', 'KILT', 'KING',
                 'KING ARTHUR', 'KINKY', 'KISS', 'KITCHEN', 'KITTY', 'KIWI', 'KNEES', 'KNIFE', 'KNIGHT', 'KNOB',
                 'KNOCKERS', 'KNOT', 'KUNG FU', 'LAB', 'LACE', 'LADDER', 'LAP', 'LASER', 'LATEX', 'LAUNDRY', 'LAWYER',
                 'LEAD', 'LEAF', 'LEATHER', 'LEGEND', 'LEGS', 'LEMON', 'LEMONADE', 'LEPRECHAUN', 'LETTER', 'LICK',
                 'LIFE', 'LIGHT', 'LIGHTER', 'LIGHTNING', 'LIMOUSINE', 'LINE', 'LINGERIE', 'LINK', 'LION', 'LIP',
                 'LIPS', 'LIQUOR', 'LITTER', 'LIZARD', 'LOBSTER', 'LOCH NESS', 'LOCK', 'LOCUST', 'LOG', 'LONDON',
                 'LOOSE', 'LOTION', 'LOVE', 'LUBE', 'LUCK', 'LUMBERJACK', 'LUNCH', 'LUST', 'MAGAZINE', 'MAGICIAN',
                 'MAIL', 'MAKEUP', 'MAMMOTH', 'MANBOOBS', 'MANICURE', 'MAP', 'MAPLE', 'MARACAS', 'MARATHON', 'MARBLE',
                 'MARCH', 'MARK', 'MARTINI', 'MASS', 'MATCH', 'MATTRESS', 'MEAT', 'MEDIC', 'MELONS', 'MEMBER', 'MEMORY',
                 'MERCURY', 'MESH', 'MESS', 'METER', 'MEXICO', 'MICROSCOPE', 'MICROWAVE', 'MILE', 'MILK', 'MILL',
                 'MILLIONAIRE', 'MINE', 'MINOTAUR', 'MINT', 'MINUTE', 'MIRROR', 'MISS', 'MISSILE', 'MISSIONARY',
                 'MIXER', 'MODEL', 'MOHAWK', 'MOIST', 'MOLE', 'MOM', 'MONA LISA', 'MONKEY', 'MOON', 'MOSCOW', 'MOSES',
                 'MOSQUITO', 'MOTEL', 'MOTHER', 'MOTORBOAT', 'MOUNT', 'MOUNTIE', 'MOUSE', 'MOUTH', 'MOVIE', 'MUD',
                 'MUG', 'MUMMY', 'MUSHROOM', 'MUSKETEER', 'MUSTARD', 'NAIL', 'NAKED', 'NAPOLEON', 'NAVEL', 'NECKLACE',
                 'NEEDLE', 'NERVE', 'NET', 'NEW YORK', 'NEWTON', 'NIGHT', 'NINJA', 'NIPPLE', 'NOAH', 'NOODLE', 'NOSE',
                 'NOTE', 'NOTRE DAME', 'NOVEL', 'NUDE', 'NURSE', 'NUT', 'NUTS', 'NYLON', 'OASIS', 'OCTOPUS', 'OIL',
                 'OLIVE', 'OLYMPUS', 'ONION', 'OPERA', 'ORANGE', 'ORGAN', 'ORGASM', 'ORGY', 'OYSTER', 'PACIFIC',
                 'PACKAGE', 'PAD', 'PADDLE', 'PAGE', 'PAINT', 'PALM', 'PAN', 'PANTS', 'PAPER', 'PARACHUTE', 'PARADE',
                 'PARK', 'PARROT', 'PART', 'PASS', 'PASTE', 'PATIENT', 'PEA', 'PEACH', 'PEACHES', 'PEANUT', 'PEARL',
                 'PECKER', 'PEE', 'PEN', 'PENGUIN', 'PENIS', 'PENNY', 'PENTAGON', 'PEPPER', 'PERIOD', 'PEW', 'PHOENIX',
                 'PIANO', 'PICKLE', 'PIE', 'PIG', 'PILLOW', 'PILLOWS', 'PILOT', 'PIMP', 'PIN', 'PINCH', 'PINE', 'PINK',
                 'PIPE', 'PIRATE', 'PISTOL', 'PIT', 'PITCH', 'PITCHER', 'PIZZA', 'PLANE', 'PLASTIC', 'PLATE',
                 'PLATYPUS', 'PLAY', 'PLAYER', 'PLOT', 'POCKET', 'POINT', 'POISON', 'POKER', 'POLE', 'POLICE', 'POLISH',
                 'POLO', 'POOL', 'POOP', 'POP', 'POPCORN', 'PORK', 'PORN', 'PORT', 'POST', 'POT', 'POTATO', 'POTTER',
                 'POUND', 'POWDER', 'PRESS', 'PRICK', 'PRINCESS', 'PRISON', 'PROSTATE', 'PUB', 'PUCKER', 'PUMPKIN',
                 'PUPIL', 'PUPPET', 'PURPLE', 'PURSE', 'PUSSY', 'PYRAMID', 'QUACK', 'QUARTER', 'QUEEF', 'QUEEN',
                 'QUEER', 'RABBIT', 'RACK', 'RACKET', 'RADIO', 'RAIL', 'RAINBOW', 'RAM', 'RANCH', 'RAT', 'RAVE', 'RAY',
                 'RAZOR', 'RECORD', 'RECTUM', 'RED', 'REGRET', 'REINDEER', 'REVOLUTION', 'RICE', 'RIFLE', 'RING', 'RIP',
                 'RIVER', 'ROACH', 'ROAD', 'ROBIN', 'ROBOT', 'ROCK', 'RODEO', 'ROLL', 'ROME', 'ROOF', 'ROOKIE', 'ROOT',
                 'ROPE', 'ROSE', 'ROULETTE', 'ROUND', 'ROW', 'RUBBER', 'RUG', 'RULER', 'RUSSIA', 'RUST', 'SACK',
                 'SADDLE', 'SAFE', 'SAHARA', 'SAIL', 'SALAD', 'SALOON', 'SALSA', 'SALT', 'SAND', 'SANTA', 'SATELLITE',
                 'SATURN', 'SAUNA', 'SAUSAGE', 'SAW', 'SCALE', 'SCARECROW', 'SCHOOL', 'SCIENTIST', 'SCORE', 'SCORPION',
                 'SCRATCH', 'SCREEN', 'SCREW', 'SCROLL', 'SCUBA DIVER', 'SEAL', 'SECOND', 'SECRETARY', 'SEED', 'SEMEN',
                 'SERVER', 'SEX', 'SHADOW', 'SHAFT', 'SHAKESPEARE', 'SHAME', 'SHAMPOO', 'SHARE', 'SHARK', 'SHAVE',
                 'SHED', 'SHEEP', 'SHEET', 'SHELL', 'SHERLOCK', 'SHERWOOD', 'SHIP', 'SHOE', 'SHOOT', 'SHOP', 'SHORTS',
                 'SHOT', 'SHOULDER', 'SHOWER', 'SIGN', 'SILK', 'SIN', 'SINK', 'SISTER', 'SKANK', 'SKATES', 'SKI',
                 'SKID', 'SKIRT', 'SKULL', 'SKYSCRAPER', 'SLED', 'SLEEP', 'SLING', 'SLIP', 'SLIPPER', 'SLOTH', 'SLUG',
                 'SLUT', 'SMEGMA', 'SMELL', 'SMOKE', 'SMOOTHIE', 'SMUGGLER', 'SNAKE', 'SNAP', 'SNATCH', 'SNIFF',
                 'SNORT', 'SNOW', 'SNOWMAN', 'SOAP', 'SOCK', 'SOFTBALLS', 'SOLDIER', 'SOLO', 'SORE', 'SOUL', 'SOUND',
                 'SOUP', 'SPACE', 'SPANK', 'SPEED', 'SPELL', 'SPERM', 'SPHINX', 'SPIDER', 'SPIKE', 'SPINE', 'SPIRIT',
                 'SPOON', 'SPOT', 'SPRAY', 'SPREAD', 'SPRING', 'SPURS', 'SPY', 'SQUARE', 'SQUASH', 'SQUIRREL', 'SQUIRT',
                 'ST.PATRICK', 'STABLE', 'STADIUM', 'STAFF', 'STALKER', 'STAMP', 'STAR', 'STATE', 'STEAM', 'STEAMY',
                 'STEEL', 'STEP', 'STETHOSCOPE', 'STICK', 'STICKER', 'STIFF', 'STILETTO', 'STOCK', 'STONES', 'STOOL',
                 'STORM', 'STORY', 'STRAIGHT', 'STRAP', 'STRAW', 'STREAM', 'STREET', 'STRIKE', 'STRING', 'STRIP',
                 'STRIPPER', 'STROBE', 'STUD', 'SUB', 'SUGAR', 'SUIT', 'SUMO', 'SUN', 'SUPERHERO', 'SWALLOW', 'SWAMP',
                 'SWEAT', 'SWIMMERS', 'SWING', 'SWITCH', 'SWORD', 'TABLE', 'TABLET', 'TABOO', 'TACO', 'TAG', 'TAIL',
                 'TANK', 'TAP', 'TASTE', 'TATTOO', 'TAVERN', 'TEA', 'TEABAG', 'TEACHER', 'TEAM', 'TEAR', 'TEASE',
                 'TELESCOPE', 'TEMPLE', 'TENT', 'TEQUILA', 'TEXAS', 'THEATRE', 'THIEF', 'THREESOME', 'THROAT', 'THUMB',
                 'THUNDER', 'TICK', 'TICKLE', 'TIE', 'TIGER', 'TIME', 'TIN', 'TIP', 'TIPI', 'TIT', 'TOAST', 'TOKYO',
                 'TONGUE', 'TOOL', 'TOOTH', 'TOP', 'TORCH', 'TORNADO', 'TORTURE', 'TOUCH', 'TOUCHDOWN', 'TOWER', 'TOY',
                 'TRACK', 'TRAIN', 'TRAMP', 'TRIANGLE', 'TRICK', 'TRIM', 'TRIP', 'TROLL', 'TROUSERS', 'TRUNK', 'TUBE',
                 'TUBESTEAK', 'TUNA', 'TUNNEL', 'TURD', 'TURKEY', 'TURTLE', 'TUTU', 'TUXEDO', 'TWIG', 'UDDERS',
                 'UNDERTAKER', 'UNICORN', 'UNIVERSITY', 'URANUS', 'VACUUM', 'VALENTINE', 'VAMPIRE', 'VAN', 'VASECTOMY',
                 'VEGAS', 'VEIN', 'VENUS', 'VET', 'VIBRATOR', 'VIDEO', 'VIKING', 'VINYL', 'VIOLET', 'VIRGIN', 'VIRUS',
                 'VODKA', 'VOLCANO', 'VOLUME', 'VOMIT', 'WAD', 'WAGON', 'WAITRESS', 'WAKE', 'WALL', 'WALRUS', 'WANG',
                 'WAR', 'WASHER', 'WASHINGTON', 'WASTE', 'WATCH', 'WATER', 'WAVE', 'WAX', 'WEB', 'WEDDING', 'WEED',
                 'WELL', 'WENCH', 'WEREWOLF', 'WET', 'WHALE', 'WHEEL', 'WHEELCHAIR', 'WHIP', 'WHISKEY', 'WHISTLE',
                 'WHITE', 'WIENER', 'WIND', 'WINDOW', 'WINE', 'WING', 'WISH', 'WITCH', 'WIZARD', 'WONDERLAND', 'WOOD',
                 'WOOL', 'WORM', 'YARD', 'YELLOWSTONE', 'ZOMBIE'})


def get_search_results(uniquewords):
    dictionary = {}
    for word in uniquewords:
        search_results = wiki.search(word, results=5)
        dictionary.update({word: search_results})
        with open('wiki_searches.txt', 'w') as file1:
            file1.write(json.dumps(dictionary))
            file1.close()
    return dictionary


diction = get_search_results(UNIQUE_WORDS)

print(str(diction))




#cont_dict, link_dict = get_wiki_data(word_list)

#export_wiki_data('wiki_text.txt', cont_dict, 'wiki_links.txt', link_dict)

#print('pause')
