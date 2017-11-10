import requests, json, time
from time import sleep

def main():

    listOfUserLogins = []
    followerCounter = 0
    twitchIDCounter = 0
    myOutputFile = open("ListOfFollowers.txt", "w")
    HEADERS = {'Client-ID': 'bmf0qyjn3nerqr67cjukjbh2pa4eyn'}
    
    getLoginName = input("What user would you like to grab the followers of?: ")
    print("This process will take some time depending on how many followers a user has...")
    loginURL = 'https://api.twitch.tv/helix/users?login=' + getLoginName

    loginURLResponse = requests.get(url=loginURL, data={}, headers=HEADERS).json()
    userLoginID = loginURLResponse['data'][0]['id']

    loginURL = 'https://api.twitch.tv/helix/users/follows?to_id=' + userLoginID + '&first=100'
    loginResponse = requests.get(url=loginURL, data={}, headers=HEADERS).json()

    followersOnPage = len(loginResponse['data'])

    while (followersOnPage != 101):
        if (followerCounter == 0):
            listOfUserIds = [loginResponse['data'][followerCounter]['from_id']]
            followerCounter = followerCounter + 1
        if (followerCounter < followersOnPage):
            listOfUserIds = listOfUserIds + [loginResponse['data'][followerCounter]['from_id']]
            followerCounter = followerCounter + 1
        elif (followerCounter == followersOnPage):
            followersOnPage = 101

    for twitchID in listOfUserIds:
        userIdUrl = 'https://api.twitch.tv/helix/users?id=' + twitchID
        userLoginGet = requests.get(url=userIdUrl, data={}, headers=HEADERS).json()
        listOfUserLogins = listOfUserLogins + [userLoginGet['data'][0]['login']]
        twitchIDCounter = twitchIDCounter + 1
        time.sleep(2)

    for loginName in listOfUserLogins:
        myOutputFile.write(str(loginName) + "\n")

    print("All done! Your list contains " + str(twitchIDCounter) + " followers!")

main()
