#! /usr/bin/env python

from twython import Twython
import random, requests
from io import BytesIO

APP_KEY = xxxxxx
APP_SECRET = xxxxxx
OAUTH_TOKEN = xxxxxx
OAUTH_TOKEN_SECRET = xxxxxx

api = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

first_list = ["Appetite For", "Famished For", "Starving For", "Greedy For", "Voracious For", "Aching For", "Driven To", "Sick For", "Thirsty For", "Suffering For",
"Curious About", "Ravenous For", "Living For The", "Out For A", "Born To", "Maximum", "Force Of", "Flight Of", "Executive", "Under Siege 3:", "The Refreshing Taste Of",
"Today It's", "A Good", "A Long Day's", "Lawful", "True", "Mojo"]
second_list = ["Annihilation", "Assassination", "Butchery", "Crucifixion", "Decapitation", "Devastation", "Decimation", "Destruction", "Garroting",
"Guillotining", "Lapidation", "Liquidation", "Massacres", "Murder", "Neutralization", "Ruination", "Slaughter", "Slayings", "Smiting", "Sniping",
"Termination", "Extermination", "Harpooning", "Exsanguination", "Strangulation", "Assaults", "Kill"]
image_list = {'1403':'456808', '2991012':'10922955', '343038':'2062154', '2601831':'10169828', '3540388':'11691205', '3305675':'11370388',
'4305945':'12736851', '4340170':'12780021', '3650000':'11847041', '3961906':'12284159', '3502536':'11644415'}

def create_image(status):
    """
    Picks a random phrase from first_list and second_list, combines with a random generator ID
    then runs it through Memegenerator API to get poster image 
    """
    mg_user = 'RyanGoslingsBugle'
    mg_pass = 'memegenerator.net'
    generator_id = random.choice(list(image_list.keys())) 
    image_id = image_list[generator_id]
    request_string = 'http://version1.api.memegenerator.net/Instance_Create?username=' + mg_user + '&password=' + mg_pass + '&languageCode=en&generatorID=' + generator_id  + '&imageID=' + image_id  + '&text0=' + status + '&text1=starring Steven Seagal'
    mg_response = requests.get(request_string)
    response_dict = mg_response.json()
    inner_dict = response_dict['result']
    return requests.get(url=inner_dict['instanceImageUrl']).content

def get_followers():
    """
    Automatically follows all new followers
    """
    following = api.get_friends_ids()
    followers = api.get_followers_ids()

    not_following_back = []
    
    for f in followers:
        if f not in following:
                not_following_back.append(f)

    for user_id in not_following_back:
        try:
            api.create_friendship(user_id)
        except Exception as e:
            print("error: %s" % (str(e)))

    
def post_update():
    """
    Posts status message to Twitter.
    """
    status = create_status()
    image = create_image(status)
    try:
        api.update_status_with_media(status=status, media=BytesIO(image))
    except Exception as e:
        print("error: %s" % (str(e)))
    
def create_status():
    """
    Creates a status message based on random choices from word lists.
    """
    status = random.choice(first_list) + ' ' +  random.choice(second_list)
    return status

def start():
    """
    Starts the program.
    """
    post_update()
    get_followers()

start()
