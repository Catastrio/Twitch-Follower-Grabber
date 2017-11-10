import requests, json, time
from time import sleep

def main():

    listOfUserLogins = []
    followerCounter = 0
    twitchIDCounter = 0
    MYOUTPUTFILE = open("ListOfFollowers.txt", "w")
    CIDFILE = open("config.ini", "r")
    clientID = CIDFILE.read()
    HEADERS = {'Client-ID': clientID}
    
    getLoginName = input("What user would you like to grab the followers of? Try my name, 'Catastrio'!: ")
    print("This process will take some time depending on how many followers a user has...")
    loginURL = 'https://api.twitch.tv/helix/users?login=' + getLoginName

    loginURLResponse = requests.get(url=loginURL, data={}, headers=HEADERS).json()
    userLoginID = loginURLResponse['data'][0]['id']

    loginURL = 'https://api.twitch.tv/helix/users/follows?to_id=' + userLoginID + '&first=100'
    loginResponse = requests.get(url=loginURL, data={}, headers=HEADERS).json()

    listOfUserIds = [userID for userID in [loginResponse['data'][0]['from_id']]]
    
    '''followersOnPage = len(loginResponse['data'])

    while (followerCounter < followersOnPage):
            listOfUserIds = [loginResponse['data'][followerCounter]['from_id']]
            followerCounter += 1'''

    userIdUrl = 'https://api.twitch.tv/helix/users?id=' + twitchID
    userLoginGet = requests.get(url=userIdUrl, data={}, headers=HEADERS).json()
    listOfUserLogins = [twitchID for twitchID in [userLoginGet['data'][0]['login']]]

    for loginName in listOfUserLogins:
        MYOUTPUTFILE.write(str(loginName) + "\n")

    print("All done! Your list contains " + str(twitchIDCounter) + " followers!")

main()
