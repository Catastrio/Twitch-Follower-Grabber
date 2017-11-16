import requests, json, time
from time import sleep

def main():

    listOfUserLogins = []
    listOfUserIDs = []
    followerCounter = 0
    twitchIDCounter = 0
    MYOUTPUTFILE = open("List_of_followers.txt", "w")
    CIDFILE = open("config.ini", "r")
    HEADERS = {'Client-ID': CIDFILE.read()}
    SECONDSTOSLEEP = 2
    
    print("To test to see if this program works, try following me on Twitch.tv/Catastrio and then using 'Catastrio' as a test!\n")
    userLoginName = input("What user would you like to grab the followers of?: ")
    userLoginEndpoint = 'https://api.twitch.tv/helix/users?login=' + userLoginName

    userLoginResponse = requests.get(url=userLoginEndpoint, data={}, headers=HEADERS).json()
    userLoginNameId = userLoginResponse['data'][0]['id']

    userFollowersEndpoint = 'https://api.twitch.tv/helix/users/follows?to_id=' + userLoginNameId + '&first=100'
    userFollowersResponse = requests.get(url=userFollowersEndpoint, data={}, headers=HEADERS).json()

    followersOnPage = len(userFollowersResponse['data'])
    print("Followers on page: " + str(followersOnPage))

    while (followerCounter < followersOnPage):
        listOfUserIDs = listOfUserIDs + [userFollowersResponse['data'][followerCounter]['from_id']]
        followerCounter += 1

    print("This process will take some time depending on how many followers a user has...")
    for twitchID in listOfUserIDs:
        userIdEndpoint = 'https://api.twitch.tv/helix/users?id=' + twitchID
        userIdResponse = requests.get(url=userIdEndpoint, data={}, headers=HEADERS).json()
        listOfUserLogins = listOfUserLogins + [userIdResponse['data'][0]['login']]
        twitchIDCounter += 1
        print(str(twitchIDCounter) + " out of " + str(len(listOfUserIDs)))
        time.sleep(SECONDSTOSLEEP)

    for loginName in listOfUserLogins:
        MYOUTPUTFILE.write(str(loginName) + "\n")

    print("All done! Your list contains " + str(twitchIDCounter) + " followers!")

if __name__ == '__main__':
    main()
