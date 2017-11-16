import requests, json, time
from time import sleep

def main():

    listOfUserLogins = []
    listOfUserIDs = []
    followerCounter = 0
    twitchIDCounter = 0
    MYOUTPUTFILE = open("ListOfFollowers.txt", "w")
    CIDFILE = open("config.ini", "r")
    HEADERS = {'Client-ID': CIDFILE.read()}
    SECONDS = 2
    
    print("To test to see if this program works, try following me on Twitch.tv/Catastrio and then using 'Catastrio' as a test!\n")
    getLoginName = input("What user would you like to grab the followers of?: ")
    loginURL = 'https://api.twitch.tv/helix/users?login=' + getLoginName

    loginURLResponse = requests.get(url=loginURL, data={}, headers=HEADERS).json()
    userLoginID = loginURLResponse['data'][0]['id']

    loginURL = 'https://api.twitch.tv/helix/users/follows?to_id=' + userLoginID + '&first=100'
    loginResponse = requests.get(url=loginURL, data={}, headers=HEADERS).json()

    followersOnPage = len(loginResponse['data'])
    print("Followers on page: " + str(followersOnPage))

    while (followerCounter < followersOnPage):
        listOfUserIDs = listOfUserIDs + [loginResponse['data'][followerCounter]['from_id']]
        followerCounter += 1

    print("This process will take some time depending on how many followers a user has...")
    for twitchID in listOfUserIDs:
        userIdUrl = 'https://api.twitch.tv/helix/users?id=' + twitchID
        userLoginGet = requests.get(url=userIdUrl, data={}, headers=HEADERS).json()
        listOfUserLogins = listOfUserLogins + [userLoginGet['data'][0]['login']]
        twitchIDCounter += 1
        print(str(twitchIDCounter) + " out of " + str(len(listOfUserIDs)))
        time.sleep(SECONDS)

    for loginName in listOfUserLogins:
        MYOUTPUTFILE.write(str(loginName) + "\n")

    print("All done! Your list contains " + str(twitchIDCounter) + " followers!")

main()
