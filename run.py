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
    try:
        talker("On a scale of 1-10, rate: Apples, Bananas, and Mangoes")
        
        question1 = inputer("Please separate your answers by commas, for example \n 5,3,10\n")
        
        cleaner1 = question1.split(",")
        
        answer1 = [int(i) for i in cleaner1]
        # refresher from senderle https://stackoverflow.com/questions/6009589/how-to-test-if-every-item-in-a-list-of-type-int
        
        if len(answer1) > 3:
            raise ValueError("You put in too many numbers!")
    except ValueError as e:
        print(f"Error! {e} try again, just numbers this time, and 3 of 'em!")
    
    try:
        talker("Very good! Moving onto vegetables...")
        
        talker("On a scale of 1-10, rate: Cucumbers, tomatoes, and potatoes.")
        
        talker("Tomatoes aren't technically fruits, but you know what we mean!")
        
        question2 = inputer("Please separate your answers by commas, for example:\n5,3,10\n")
        
        cleaner2 = question2.split(",")
        
        answer2 = [int(x) for x in cleaner2]
        
        if len(answer2) > 3:
            raise ValueError("You put in too many numbers!")
                # refresher from senderle https://stackoverflow.com/questions/6009589/how-to-test-if-every-item-in-a-list-of-type-int 
    except ValueError as e:
            rint(f"Error! {e} try again, and just numbers this time!")
    
    try: 
        if diet == "no" or diet == "n":
            talker(f"Very good! So, {name}, let's talk meat: what do you think about...")
            question3 = inputer("Beef, chicken, and pork? Please separate your answers by commas, for example \n 5,3,10\n")
            cleaner3 = question3.split(",")
            answer3 = [int(x) for x in cleaner3]
            if len(answer2) > 3:
                raise ValueError("You put in too many numbers!")
        elif diet == "yes" or diet == "y":
            return answer1, answer2
    except ValueError as e:
        print(f"Error! {e} try again, just numbers this time, and 3 of 'em!")
    else:
        return answer1,answer2,answer3



# code to add numeric value to the spreadsheet

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
