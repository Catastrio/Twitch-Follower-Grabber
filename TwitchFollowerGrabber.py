import requests, json, time, configparser, string
from time import sleep

def main():
    
    config = configparser.ConfigParser()
    listOfUserLogins = []
    listOfUserIDs = []
    followerCounter = 0
    twitchIDCounter = 0
    
    MY_OUTPUT_FILE = open("ListOfFollowers.txt", "w")
    SECONDS_TO_SLEEP = 2
    DATA_INDEX = 0
    CONFIGFILE = "config.ini"

    with open(CONFIGFILE) as f_obj:
        config.read(CONFIGFILE)
        HEADERS = {'Client-ID': config['DEFAULT']['Client_id']}
    
    print("To test to see if this program works, try following me on Twitch.tv/Catastrio and then using 'Catastrio' as a test!\n")
    twitchName = input("What user would you like to grab the followers of?: ")
    userEndpoint = 'https://api.twitch.tv/helix/users?login=' + twitchName

    userResponse = requests.get(url=userEndpoint, data={}, headers=HEADERS).json()
    data = userResponse['data'][DATA_INDEX]
    user_id = data['id']

    userFollowsEndpoint = 'https://api.twitch.tv/helix/users/follows?to_id=' + user_id + '&first=100'
    userFollowsResponse = requests.get(url=userFollowsEndpoint, data={}, headers=HEADERS).json()

    followersOnPage = len(userFollowsResponse['data'])
    print("Followers on page: " + str(followersOnPage))

    listOfUserIDs = [ID['from_id'] for ID in userFollowsResponse['data']]

    print("This process will take some time depending on how many followers a user has...")
    for twitchID in listOfUserIDs:
        userIdEndpoint = 'https://api.twitch.tv/helix/users?id=' + twitchID
        userIdResponse = requests.get(url=userIdEndpoint, data={}, headers=HEADERS).json()
        listOfUserLogins = listOfUserLogins + [userIdResponse['data'][DATA_INDEX]['login']]
        twitchIDCounter += 1
        print(str(twitchIDCounter) + " out of " + str(len(listOfUserIDs)))
        time.sleep(SECONDSTOSLEEP)

    for loginName in listOfUserLogins:
        MY_OUTPUT_FILE.write(str(loginName) + "\n")

    print("All done! Your list contains " + str(twitchIDCounter) + " followers!")

if __name__ == '__main__':
    main()
