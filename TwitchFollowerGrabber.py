import requests, json, time
from time import sleep

def main():

    # Declaring some variables for later use.
    # ListOfFollowers.txt will be created if it doesn't exist already.
    # It will always overwrite the previous.
    # Twitch's API returns a list of followers in the order they followed you.
    # In other words, your oldest followers are at the bottom.
    # Headers are used any time a request is sent to Twitch.
    listOfUserLogins = []
    followerCounter = 0
    twitchIDCounter = 0
    myOutputFile = open("ListOfFollowers.txt", "w")
    HEADERS = {'Client-ID': 'bmf0qyjn3nerqr67cjukjbh2pa4eyn'}
    
    # The user is asked for the login name of a Twitch streamer.
    # Try using my name, Catastrio!
    # The loginURL appends the user input to the end so that any user's followers can be grabbed.
    # We throw in a print statement to let the user know this process isn't quick.
    getLoginName = input("What user would you like to grab the followers of?: ")
    print("This process will take some time depending on how many followers a user has...")
    loginURL = 'https://api.twitch.tv/helix/users?login=' + getLoginName

    # Here we store the response of the loginURL result.
    # This returns a json containing a bunch of info about the user.
    # In this case, we're converting the login name into an ID that can be used later.
    loginURLResponse = requests.get(url=loginURL, data={}, headers=HEADERS).json()
    userLoginID = loginURLResponse['data'][0]['id']

    # The user's login ID is appended to the url.
    # As of right now, this program will ONLY grab the user's first 100 followers.
    # Feature coming in TFG2.0
    loginURL = 'https://api.twitch.tv/helix/users/follows?to_id=' + userLoginID + '&first=100'
    loginResponse = requests.get(url=loginURL, data={}, headers=HEADERS).json()

    # If using my name, Catastrio, as an example this variable is 40 at the time of writing.
    # This variable will later be used to determine whether or not we paginate
    # This will have to be rewritten. so that followersOnPage changes.
    # Maybe make it so if the followersOnPage = 100, store the pagination number for another round
    # Else if followersOnPage < 100 finish up and close the while loop.
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

    # So what the previous algorithm did is store the IDs of users following a channel.
    # Those are stored in listOfUser Ids.
    # For each ID, we want to grab the login name of the user.
    # We store those login names in listOfUserLogins
    # TwitchIDCounter is used to tell you how many followers you have.
    # This is so you can double check and ensure your output is accurate.
    # time.sleep() is used to prevent the "too many requests" error from Twitch's API.
    for twitchID in listOfUserIds:
        userIdUrl = 'https://api.twitch.tv/helix/users?id=' + twitchID
        userLoginGet = requests.get(url=userIdUrl, data={}, headers=HEADERS).json()
        listOfUserLogins = listOfUserLogins + [userLoginGet['data'][0]['login']]
        twitchIDCounter = twitchIDCounter + 1
        time.sleep(2)

    # Writing to the file. Final print statement to signify completion.
    for loginName in listOfUserLogins:
        myOutputFile.write(str(loginName) + "\n")

    print("All done! Your list contains " + str(twitchIDCounter) + " followers!")

main()
