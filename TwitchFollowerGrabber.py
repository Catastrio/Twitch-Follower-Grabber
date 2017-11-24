import requests, json, time, configparser, string
from time import sleep

def get_user_by_id(user_id):

    config = configparser.ConfigParser()
    CONFIG_FILE = "config.ini"
    CLIENT_ID = 'Client_id'
    DATA_INDEX = 0
    
    with open(CONFIG_FILE) as f_obj:
        config.read(CONFIG_FILE)
        HEADERS = {'Client-ID': config['DEFAULT'][CLIENT_ID]}

    user_by_id_endpoint = 'https://api.twitch.tv/helix/users?id=' + user_id
    user_id_response = requests.get(url = user_by_id_endpoint, data={}, headers=HEADERS).json()['data'][DATA_INDEX]['login']
    return user_id_response

def get_user_by_username(username):

    config = configparser.ConfigParser()
    CONFIG_FILE = "config.ini"
    CLIENT_ID = 'Client_id'
    DATA_INDEX = 0
    
    with open(CONFIG_FILE) as f_obj:
        config.read(CONFIG_FILE)
        HEADERS = {'Client-ID': config['DEFAULT'][CLIENT_ID]}
    
    user_by_username_endpoint = 'https://api.twitch.tv/helix/users?login=' + username

    user_response = requests.get(url=user_by_username_endpoint, data={}, headers=HEADERS).json()
    data = user_response['data'][DATA_INDEX]
    user_id = data['id']
    return user_id

def get_followers_for_username(username):

    SECONDS_TO_SLEEP = 2
    config = configparser.ConfigParser()
    CONFIG_FILE = "config.ini"
    CLIENT_ID = 'Client_id'
    DATA_INDEX = 0
    
    with open(CONFIG_FILE) as f_obj:
        config.read(CONFIG_FILE)
        HEADERS = {'Client-ID': config['DEFAULT'][CLIENT_ID]}
    
    user_id = get_user_by_username(username)
    user_follows_endpoint = 'https://api.twitch.tv/helix/users/follows?to_id=' + user_id + '&first=100'
    user_follows_response = requests.get(url=user_follows_endpoint, data={}, headers=HEADERS).json()['data']

    followers_on_page = len(user_follows_response)
    print("Followers on page: " + str(followers_on_page))

    list_of_user_ids = [follower_edge['from_id'] for follower_edge in user_follows_response]
    return list_of_user_ids

def convert_id_to_username(idList):
    
    MY_OUTPUT_FILE = open("ListOfFollowers.txt", "w")
    config = configparser.ConfigParser()
    CONFIG_FILE = "config.ini"
    CLIENT_ID = 'Client_id'
    DATA_INDEX = 0
    twitch_id_counter = 0
    list_of_user_logins = []
    SECONDS_TO_SLEEP = 2
    
    with open(CONFIG_FILE) as f_obj:
        config.read(CONFIG_FILE)
        HEADERS = {'Client-ID': config['DEFAULT'][CLIENT_ID]}

    print("This process will take some time depending on how many followers a user has...")
    for twitch_id in idList:
        user_id_response = get_user_by_id(twitch_id)
        list_of_user_logins.append(user_id_response)
        twitch_id_counter += 1
        print(str(twitch_id_counter) + " out of " + str(len(idList)))
        time.sleep(SECONDS_TO_SLEEP)

    for login_name in list_of_user_logins:
        MY_OUTPUT_FILE.write(str(login_name) + "\n")

    print("All done! Your list contains " + str(twitch_id_counter) + " followers!") 

def main():

    print("Follow me at Twitch.tv/Catastrio then try 'Catastrio' and see if you show up!")
    username = input("What user would you like to get the name of?: ")
    follow_list = get_followers_for_username(username)
    convert_id_to_username(follow_list)

if __name__ == '__main__':
    main()
