import json
import cfg

#Procedure to add data to the Data.json file
def AppendToData(contentID, content):
    with open("data.json", "r+") as f:
        #Load the json file in read mode
        jsonData = json.load(f)
        #Create a temporary list of items from the relevant part of the json file and add the content passed to the
        #procedure
        if contentID =="UserAccounts":
            # Create a temporary list of items from the relevant part of the json file and add the content passed to the
            # procedure
            temp = jsonData["UserAccounts"]
        elif contentID =="ShootingProfiles":
            for user in jsonData["UserAccounts"]:
                # Find the user currently logged in and create a temporary list of items from the relevant part of the
                # json file
                if user["Username"] == cfg.CurrentUserDetails[0] and user["Password"] == cfg.CurrentUserDetails[1]:
                    user_index = jsonData["UserAccounts"].index(user)
                    temp = jsonData["UserAccounts"][user_index]["ShootingProfiles"]
        #Add the content passed to the procedure to the relevant section
        temp.append(content)
    #Write the new content list to json in the correct format
    with open("data.json", "w") as f:
        json.dump(jsonData, f, indent=2)

#Function to return data from the Data.json file
def ReadData():
    with open("data.json", "r") as f:
        return json.load(f)

#A list of valid contentIDs for future reference
valid_contentIDs = ["UserAccounts","ShootingProfiles"]