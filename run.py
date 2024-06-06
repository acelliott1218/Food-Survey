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

class Big():
    """
    This gargantuan class combines the survey logic AND the appending logic
    while allowing easy access to the answer attributes across the class its self
    """
    def __init__(self):
        self.answer1 = None
        self.answer2 = None
        self.answer3 = None
    def survey(self, diet, name):
        """
        The main survey function, which will collect the data inputted by survey takers
        Meat questions are reserved for non-vegetarians as to not skew the data
        """
        try:
            talker("On a scale of 1-10, rate: Apples, Bananas, and Mangoes")
            
            question1 = inputer("Please separate your answers by commas, for example \n 5,3,10\n")
            #cleaner1, cleaner2, and cleaner3 all serve to prepare the inputted data for int-conversion
            cleaner1 = question1.split(",")
            #iterates through the list provided from question1, without commas, and converts to integers for the final answer
            self.answer1 = [int(i) for i in cleaner1]
            # refresher from senderle https://stackoverflow.com/questions/6009589/how-to-test-if-every-item-in-a-list-of-type-int
            
            if len(self.answer1) > 3:
                raise ValueError("You put in too many numbers!")
        except ValueError as e:
            print(f"Error! {e} try again, just numbers this time, and 3 of 'em!")
        
        try:
            #this entire section works the exact same as the previous one
            talker("Very good! Moving onto vegetables...")
            
            talker("On a scale of 1-10, rate: Cucumbers, tomatoes, and potatoes.")
            
            talker("Tomatoes aren't technically fruits, but you know what we mean!")
            
            question2 = inputer("Please separate your answers by commas, for example:\n5,3,10\n")
            
            cleaner2 = question2.split(",")
            
            self.answer2 = [int(x) for x in cleaner2]
            
            if len(self.answer2) > 3:
                raise ValueError("You put in too many numbers!")
                    # refresher from senderle https://stackoverflow.com/questions/6009589/how-to-test-if-every-item-in-a-list-of-type-int 
        except ValueError as e:
                print(f"Error! {e} try again, and just numbers this time!")
        
        try: 
            #section to separate data from non-vegetarians
            if diet == "no" or diet == "n":

                talker(f"Very good! So, {name}, let's talk meat: what do you think about...")
                
                question3 = inputer("Beef, chicken, and pork? Please separate your answers by commas, for example \n 5,3,10\n")
                
                cleaner3 = question3.split(",")
                
                self.answer3 = [int(x) for x in cleaner3]
                
                if len(self.answer2) > 3:
                    raise ValueError("You put in too many numbers!")
            
            elif diet == "yes" or diet == "y":
                return self.answer1, self.answer2
        # this exception is unfortunately not where you'd think it'd be!
        except ValueError as e:
            print(f"Error! {e} try again, just numbers this time, and 3 of 'em!")
        if diet == "no" or diet == "n":
            return self.answer1,self.answer2,self.answer3

    def appender(self, diet, vegetarian, non_vegetarian):
        """
        adds the relevant data from the survey to the vegetarian or non-vegetarian tabs
        converts the answers from survey() to integers (again) so they can be appended
        this method does not touch the statistics page, in the interests of keeping the code
        short
        """
        # however, at least the code actually appends now. so that's progress
        print("Adding results to spreadsheet...")
        #the answers have to be re-stated for the code to work
        #it might not be necessary to keep the return statements or int conversions in survey() bc of this
        self.answer1 = [int(i) for i in self.answer1]
        self.answer2 = [int(i) for i in self.answer2]

        if diet == "no" or diet == "n":
            self.answer3 = [int(i) for i in self.answer3]

            non_vegetarian.append_row(self.answer1)
            non_vegetarian.append_row(self.answer2)
            non_vegetarian.append_row(self.answer3)
            print("Results uploaded!")
        if diet == "yes" or diet == "y":
            vegetarian.append_row(self.answer1)
            vegetarian.append_row(self.answer2)
            print("Results uploaded!")


# function to calculate average responses

# function to calculate most popular food

def main():
    info = talker("Welcome to the Food Survey! You will be asked your opinions on various food groups.\n")
    name = inputer("What is your name?\n").title() #code to restrict this to strings at certain character limits
    diet = inputer("Are you vegetarian? Please enter 'yes' or 'no'.\n").lower()
    review = talker(f'Welcome {name}! Since you answered "{diet}", your survey will be tailored with this in mind!')

    non_vegetarian = SHEET.worksheet('Standard')
    vegetarian = SHEET.worksheet('Vegetarian')
    stats = SHEET.worksheet('Statistics')


    b = Big()
    b.survey(diet, name)
    b.appender(diet, vegetarian, non_vegetarian)
    

if __name__ == "__main__":
    main()


# To be added:
# Test-taker's overall results from survey page, average value for each section, and how many times the survey has been taken
# Favorite food from each category (fruits, vegetables, meat) for vegetarians and non-vegetarians
