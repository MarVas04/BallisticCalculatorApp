from kivymd.app import MDApp
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRectangleFlatButton
import cfg
import LoginModule #Imports file that contains the code for the log in system
import Calculator #Imports file that contains the calculator and environmental value fetcher
import FileHandler #Imports the file handler

#Defind the MyToggleButton class that has to inherit from the button that will be made toggleable
#(in this case MDRectangleFlatButton)
class MyToggleButton(MDRectangleFlatButton, MDToggleButton):
    pass

#Creates the screen manager class under which some object properties are defined. These object properties allow
#referencing of things in the kv file from the py file and vise versa. They have to be initialised with the 'None'
#parameter
class MyScreenManager(ScreenManager):
    username_input_box = ObjectProperty(None)
    password_input_box = ObjectProperty(None)
    username_register_box = ObjectProperty(None)
    password_register_box = ObjectProperty(None)

#Creates a class for a screen manager that will change the section displayed on the main screen with respect to
#the appropriate button being pressed (e.g pressing 'Settings' will display the settings subscreen on main
class SubscreenManager(ScreenManager):
    pass

#Create a class for the shooting profiles subscreen
class ShootingProfilesSubscreen(Screen):

    # Initialise IDs as object properties so that they can be referenced from the .py file
    dropdownMenu = ObjectProperty(None)
    profileSaveName = ObjectProperty(None)

    #A procedure to save a new profile. The new profile is saved as a list and is added under the currently logged in
    #user's 'Shooting Profiles' list in the data.json file
    def SaveNewProfile(self):
        referenceToAVI = self.parent.get_screen('AVISubscreen')
        SaveName = self.profileSaveName.text
        if SaveName == "":
            print ("Please enter a name for the save")
        else:
            #These variables are taken from the Adjustments/Value input subscreen so that's the screen that needs to be
            #referenced to get their IDs and from that, their values.
            SaveMass = referenceToAVI.massInput.text
            SaveCalibre = referenceToAVI.calibreInput.text
            SaveBC = referenceToAVI.bcInput.text
            SaveVelocity = referenceToAVI.velocityInput.text
            SaveClickIncrement = str(cfg.ClickIncrementsValue)
            #Puts all the saved data into a list and adds it to the currently logged in user's shooting profiles
            SaveData = [SaveName,SaveMass,SaveCalibre,SaveBC,SaveVelocity,SaveClickIncrement]
            FileHandler.AppendToData("ShootingProfiles", SaveData)
            #Clears the text input field after saving
            self.profileSaveName.text = ""

    # The 'on_enter' function name is reserved by kivy's screen manager as a function that is run every time the parent
    # screen is entered
    def on_enter(self):
        #Initialise a list of saved profile names
        SavedProfileNames = []
        #Initialise a count variable. The variable tracks whether the on_enter procedure is being accessed for the first
        #time. This is to prevent a bug that is caused by on_enter being called when screens are first being initialised
        #and have no values which then causes the statements that set values to not work.
        count = cfg.ProfilesScreenEntryCount
        #If the function is being accessed for the first time, add 1 to count so that the next time it is run the rest
        # of the code will be executed
        if count == 0:
            cfg.ProfilesScreenEntryCount += 1
        # This block of code accesses the current user's shooting profiles and extracts their names (the first item
        # in the array of a saved profile's data) and adds them to a separate list
        else:
            for user in FileHandler.ReadData()["UserAccounts"]:
                if user["Username"] == cfg.CurrentUserDetails[0] and user["Password"] == cfg.CurrentUserDetails[1]:
                    userIndex = FileHandler.ReadData()["UserAccounts"].index(user)
                    SavedProfiles = FileHandler.ReadData()["UserAccounts"][userIndex]["ShootingProfiles"]
                    try:
                        for i in SavedProfiles:
                            SavedProfileNames.append(i[0])
                    #If there are no items in the user's shooting profiles array then an index error will be raised.
                    # When this happens, a message about the error is provided.
                    except IndexError:
                        print ("No saved profiles")
            #Adds the names of the user's saved profiles to the drop down menu
            self.dropdownMenu.values = SavedProfileNames

    #Procedure to populate the text boxes in the Adjustments/Value input menu with items saved under the selected
    #profile
    def LoadProfileContent(self, profile):
        #Creates a reference to the Adjustments/Value input screen
        referenceToAVI = self.parent.get_screen('AVISubscreen')
        # Creates a reference to the Settings input screen
        referenceToSS = self.parent.get_screen('SSubscreen')
        #Loads the current user's shooting profiles, selects the one that the user chose in the dropdown menu, and sets
        #the values of in the Adjustments/Value input menu as well as the click increment in the settings menu
        for user in FileHandler.ReadData()["UserAccounts"]:
            if user["Username"] == cfg.CurrentUserDetails[0] and user["Password"] == cfg.CurrentUserDetails[1]:
                userIndex = FileHandler.ReadData()["UserAccounts"].index(user)
                temp = FileHandler.ReadData()["UserAccounts"][userIndex]["ShootingProfiles"]
                for Profile_Content in temp:
                    if Profile_Content[0] == profile:
                        referenceToAVI.massInput.text = Profile_Content[1]
                        referenceToAVI.calibreInput.text = Profile_Content[2]
                        referenceToAVI.bcInput.text = Profile_Content[3]
                        referenceToAVI.velocityInput.text = Profile_Content[4]
                        cfg.ClickIncrementsValue = Profile_Content[5]


#Create a class for the settings subscreen
class SettingsSubscreen(Screen):
    #Initialise IDs as object properties so that they can be referenced from the .py file
    tenthToggle = ObjectProperty(None)
    eighthToggle = ObjectProperty(None)
    quarterToggle = ObjectProperty(None)
    halfToggle = ObjectProperty(None)

    #A procedure to change the ClickIncrementsValue (contained in the cfg file) in accordance with which button is
    #pressed
    def UpdateClickValue(self):
        if self.tenthToggle.state == "down" :
            cfg.ClickIncrementsValue = float(0.1)
        elif self.eighthToggle.state == "down":
            cfg.ClickIncrementsValue = float(0.125)
        elif self.quarterToggle.state == "down":
            cfg.ClickIncrementsValue = float(0.25)
        elif self.halfToggle.state == "down":
            cfg.ClickIncrementsValue = float(0.5)

#Create a class for the Adjustments/Value input subscreen
class AdjustmentsValueInputSubscreen(Screen):
    #Initialise IDs as object properties so that they can be referenced from the .py file
    massInput = ObjectProperty(None)
    calibreInput = ObjectProperty(None)
    bcInput = ObjectProperty(None)
    velocityInput = ObjectProperty(None)
    distanceInput = ObjectProperty(None)
    temperatureInput = ObjectProperty(None)
    rhInput = ObjectProperty(None)
    moaAdjustment = ObjectProperty(None)
    milradAdjustment = ObjectProperty(None)

    #Procedure to send the input from the relevant boxes to the calculator module to set the value for the necessary
    #variables
    def CalculateAdjustment(self):
        #Set the variables in the calculator module to the input in the relevant box
        Calculator.mass = self.massInput.text
        Calculator.calibre = self.calibreInput.text
        Calculator.BC = self.bcInput.text
        Calculator.velocity = self.velocityInput.text
        Calculator.distance_to_target = self.distanceInput.text
        #Use the values sent in the above chunk of code as well as environmental ones to calculate the adjustment in
        #MOA and MILRAD
        try:
            MOAadjustment = Calculator.MOA_Adjustment(Calculator.distance_to_target,
                            Calculator.bullet_drop(Calculator.mass,float(self.temperatureInput.text), float(self.rhInput.text)))
            MILRADadjustment = Calculator.MILRAD_Adjustment(MOAadjustment)
            #Set the text in the output boxes to the result of the calculation
            self.moaAdjustment.text = str(MOAadjustment/float(cfg.ClickIncrementsValue))
            self.milradAdjustment.text = str(MILRADadjustment/float(cfg.ClickIncrementsValue))
        except:
            print ("Unable to calculate adjustment")

    #Procedure to fetch environmental data if required
    def EnvironmentalValues(self):
        EnvDataDict = Calculator.env_data()
        #Set the value in the relevant boxes to the value acquired from the function to get environmental data
        if self.temperatureInput.text == "":
            self.temperatureInput.text = str(round(EnvDataDict["Temperature"],2))
        if self.rhInput.text == "":
            self.rhInput.text = str(round(EnvDataDict["Relative Humidity"],2))


#Creates the main screen class
class MainScreen(Screen):
    pass

#Creates the login screen class. It inherits from the LoginScreen class within the login module file.
class LoginScreen(LoginModule.LoginScreen_LoginModule):
    pass

#Creates the register screen class. It inherits from the RegisterScreen class within the login module file.
class RegisterScreen(LoginModule.RegisterScreen_LoginModule):
    pass


#Creates the class for the app which inherits functionality from MDApp and
#builds the app from various elements
class MVBC(MDApp):

    #Reset the profile screen entry count to 0 to avoid potential errors
    cfg.ProfilesScreenEntryCount = 0

    #Data dictionary to create the menu button. Defines the text and icon of menu buttons
    data = {
        "Logout": "logout",
        "Shooting profiles": "account",
        "Settings": "cog",
        "Adjustments/Value input": "numeric"
    }
    #This is the callback procedure for the menu button. Depending on what button is pressed in the menu after it's
    #open the relevant procedure will be called
    def callbackMainMenu(self, instance):
        if instance.icon == "logout":
            callback_L(self, instance)
        elif instance.icon == "account":
            callback_SP(self, instance)
        elif instance.icon == "cog":
            callback_S(self, instance)
        elif instance.icon == "numeric":
            callback_AVI(self, instance)


    def build(self):
        # Changes the default colour of all elements to green
        self.theme_cls.primary_palette = "Green"
        # Allows to set the colour of specific elements to red (primarily to highlight certain parts of the program)
        self.theme_cls.accent_palette = "Red"
        #When the app is run initialise the click increment value to 1 in order to avoid  errors. This value can be
        #updated as needed from the settings menu
        cfg.ClickIncrementsValue = 1
        # When the app is run initialise the saved profile names list to blank in order to avoid  errors. This value
        # can be updated as needed from the shooting profiles menu
        cfg.SavedProfileNames = []


#The following 4 procedures can be called depending on what button in the menu is pressed. The letters
#following the underscore are an acronym of the button name (e.g _L means it's the callback for the Logout button)
def callback_L(self, instance):
    self.root.current = "loginArea"

def callback_SP(self, instance):
    #Uses IDs to reference the nested screen manager in the main screen and displays the contents of the shooting
    #profiles subscreen when the relevant button is pressed
    self.root.ids.screen2.ids.SubscreenManagement.current = "SPSubscreen"

def callback_S(self, instance):
    #Uses IDs to reference the nested screen manager in the main screen and displays the contents of the settings
    #subscreen when the relevant button is pressed
    self.root.ids.screen2.ids.SubscreenManagement.current = "SSubscreen"

def callback_AVI(self, instance):
    #Uses IDs to reference the nested screen manager in the main screen and displays the contents of the adjustments/
    #value input subscreen when the relevant button is pressed
    self.root.ids.screen2.ids.SubscreenManagement.current = "AVISubscreen"


#Runs the app
MVBC().run()
