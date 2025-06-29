from kivy.uix.screenmanager import Screen
import FileHandler
import cfg


class LoginScreen_LoginModule(Screen):
    # Function to verify login details
    def VerifyLogin(self):
        # Initiates variables
        Username_Verified = False
        Password_Verified = False
        temp_list = []
        # Assigns a variable to the text inside the username and password boxes
        username = self.usernameinput.text
        password = self.passwordinput.text
        # Takes usernames from the UserInfo dictionary in data.json and adds them to a list
        for singleUserData in FileHandler.ReadData()["UserAccounts"]:
            temp_list.append(singleUserData["Username"])
        # Checks each username in the list against the text in the username field
        for username_in_list in temp_list:
            if username_in_list == username:
                Username_Verified = True
                break
            elif username_in_list != username:
                pass
            else:
                print("Error verifying username")
        # Carries out the same process as above for the password
        for singleUserData in FileHandler.ReadData()["UserAccounts"]:
            temp_list.append(singleUserData["Password"])
        for password_in_list in temp_list:
            if password_in_list == password:
                Password_Verified = True
                break
            elif password_in_list != password:
                pass
            else:
                print("Error verifying username")
        # If both the username and password match then save them for future reference and switch the screen to the main
        # area
        if Username_Verified == True and Password_Verified == True:
            cfg.CurrentUserDetails = [username,password]
            self.manager.current = "mainArea"
        else:
            print("login failed")


class RegisterScreen_LoginModule(Screen):
    # Function to register a user
    def RegisterUser(self):
        # Assigns a name to the text in the username and password boxes and initialises variables
        username = self.usernameregister.text
        password = self.passwordregister.text
        if username == "" or password == "":
            print ("Can't register user with blank username or password")
        else:
            Username_Taken = False
            temp_list = []
            # Takes usernames from the UserAccounts dictionary in data.json and adds them to a list
            for singleUserData in FileHandler.ReadData()["UserAccounts"]:
                temp_list.append(singleUserData["Username"])
            # Checks each username in the list against the text in the username field
            for username_in_list in temp_list:
                if username_in_list == username:
                    print("Username taken")
                    Username_Taken = True
                    break
                elif username_in_list != username:
                    pass
                else:
                    print("Error verifying username uniqueness")
                    break
            # If the username is unique then the username and password are added to data.json thereby creating a new
            # account
            if Username_Taken == False:
                dict = {"Username": username, "Password": password, "ShootingProfiles": []}
                FileHandler.AppendToData("UserAccounts",dict)
                print("User registered successfully")
            else:
                print("Unable to register user")