#! /usr/bin/env python

from twython import Twython
import random, requests
from io import BytesIO

APP_KEY = xxxxxxx
APP_SECRET = xxxxxxx
OAUTH_TOKEN = xxxxxxx
OAUTH_TOKEN_SECRET = xxxxxxx

api = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

first_list = ["Appetite For", "Famished For", "Starving For", "Greedy For", "Voracious For", "Aching For", "Driven To", "Sick For", "Thirsty For", "Suffering For",
"Curious About", "Ravenous For", "Living For The", "Out For A", "Born To", "Maximum", "Force Of", "Flight Of", "Executive", "Under Siege 3:", "The Refreshing Taste Of",
"Today It's", "A Good", "A Long Day's", "Lawful", "True", "Mojo"]
second_list = ["Annihilation", "Assassination", "Butchery", "Crucifixion", "Decapitation", "Devastation", "Decimation", "Destruction", "Garroting",
"Guillotining", "Lapidation", "Liquidation", "Massacres", "Murder", "Neutralization", "Ruination", "Slaughter", "Slayings", "Smiting", "Sniping",
"Termination", "Extermination", "Harpooning", "Exsanguination", "Strangulation", "Assaults", "Kill"]
image_list = ['12449792','39253225','25741644','19016174','41706702','53733315','56208839','57905320','58274511']

def create_image(status):
mg_user = 'RyanGoslingsBugle'
    mg_pass = 'memegenerator.net'
    generator_id = random.choice(image_list)
    request_string = 'https://api.imgflip.com/caption_image?template_id=' + generator_id + '&username=' + mg_user + '&password=' + mg_pass + '&text0=' + status + '&text1=starring Steven Seag$
    mg_response = requests.get(request_string)
    response = mg_response.json()
    return requests.get(response['data']['url']).content

def get_followers():
    """
    Automatically follows all new followers
    """
    following = api.get_friends_ids(screen_name='seagalbot')
    followers = api.get_followers_ids(screen_name='seagalbot')

    not_following_back = []
    
    for f in followers['ids']:
        if f not in following['ids']:
                not_following_back.append(f)

    for follower_id in not_following_back:
        try:
            api.create_friendship(user_id=follower_id)
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
