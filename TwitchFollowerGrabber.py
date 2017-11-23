import requests, json, time, configparser, string
from time import sleep

def main():
    
    config = configparser.ConfigParser()
    list_of_user_logins = []
    list_of_usser_ids = []
    follower_counter = 0
    twitch_id_counter = 0
    
    MY_OUTPUT_FILE = open("ListOfFollowers.txt", "w")
    SECONDS_TO_SLEEP = 2
    DATA_INDEX = 0
    CONFIG_FILE = "config.ini"
    CLIENT_ID = 'Client_id'

    with open(CONFIG_FILE) as f_obj:
        config.read(CONFIG_FILE)
        HEADERS = {'Client-ID': config['DEFAULT'][CLIENT_ID]}
    
    print("To test to see if this program works, try following me on Twitch.tv/Catastrio and then using 'Catastrio' as a test!\n")
    twitch_username = input("What user would you like to grab the followers of?: ")
    user_by_username_endpoint = 'https://api.twitch.tv/helix/users?login=' + twitch_username

    user_response = requests.get(url=user_by_username_endpoint, data={}, headers=HEADERS).json()
    data = user_response['data'][DATA_INDEX]
    user_id = data['id']

    user_follows_endpoint = 'https://api.twitch.tv/helix/users/follows?to_id=' + user_id + '&first=100'
    user_follows_response = requests.get(url=user_follows_endpoint, data={}, headers=HEADERS).json()['data']

    followers_on_page = len(user_follows_response)
    print("Followers on page: " + str(followers_on_page))

    list_of_user_ids = [follower_edge['from_id'] for follower_edge in user_follows_response]

    print("This process will take some time depending on how many followers a user has...")
    for twitch_id in list_of_user_ids:
        user_by_user_id_endpoint = 'https://api.twitch.tv/helix/users?id=' + twitch_id
        user_id_response = requests.get(url=user_by_user_id_endpoint, data={}, headers=HEADERS).json()
        list_of_user_logins = list_of_user_logins + [user_id_response['data'][DATA_INDEX]['login']]
        twitch_id_counter += 1
        print(str(twitch_id_counter) + " out of " + str(len(list_of_user_ids)))
        time.sleep(SECONDS_TO_SLEEP)

    for login_name in list_of_user_logins:
        MY_OUTPUT_FILE.write(str(login_name) + "\n")

    print("All done! Your list contains " + str(twitch_id_counter) + " followers!")

if __name__ == '__main__':
    main()
