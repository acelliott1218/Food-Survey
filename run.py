import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Food Survey')


def inputer(prompt):
    """
    easy function to call for feedback
    """ 
    return input(prompt)


def talker(words):
    """
    easy function to communicate with survey-takers
    """ 
    print(words)

def survey(diet, name):
    """
    The main survey function, which will collect the data inputted by survey takers
    Meat questions are reserved for non-vegetarians as to not skew the data
    """
    talker("Let's get started! What do you think of...")
    question1 = inputer("Apples, Bananas, and Mangoes? Please separate your answers by commas, for example \n 5,3,10\n")
    #code to raise exception if the value isn't an integer
    talker("Very good! Moving onto vegetables, what do you think of...")
    question2 = inputer("Cucumbers, tomatoes, and potatoes?\n Tomatoes aren't technically fruits, but you know what we mean! Please separate your answers by commas, for example \n 5,3,10\n ")
    #code to raise exception if the value isn't an integer
    answer1 = question1.split(",")
    answer2 = question2.split(",")
    if diet == "no" or "n":
        talker(f"Very good! So, {name}, let's talk meat: what do you think about...")
        question3 = inputer("Beef, chicken, and pork? Please separate your answers by commas, for example \n 5,3,10\n")
        answer3 = question3.split(",")
        #code to add numeric value to the spreadsheet
        #code to raise exception if the value isn't an integer
        print(answer3)
        return answer3
        #code to add numeric value to the spreadsheet
    print(answer1,answer2)
    return answer1, answer2
    #code to add numeric value to the spreadsheet

# function to add survey results to relevant spreadsheet

# function to calculate average responses

# function to calculate most popular food

def main():
    info = talker("Welcome to the Food Survey! You will be asked your opinions on various food groups.\n")
    name = inputer("What is your name?\n").title() #code to restrict this to strings at certain character limits
    diet = inputer("Are you vegetarian? Please enter 'yes' or 'no'.\n").lower() #this needs to be strictly yes/no, will figure that out
    review = talker(f'Welcome {name}! Since you answered "{diet}", your survey will be tailored with this in mind!')
    survey(diet, name)
    non_vegetarian = SHEET.worksheet('Standard')
    vegetarian = SHEET.worksheet('Vegetarian')
    standard_data = non_vegetarian.get_all_values()
    veg_data = vegetarian.get_all_values()

if __name__ == "__main__":
    main()


# To be added:
# Test-taker's overall results from survey page, average value for each section, and how many times the survey has been taken
# Favorite food from each category (fruits, vegetables, meat) for vegetarians and non-vegetarians
