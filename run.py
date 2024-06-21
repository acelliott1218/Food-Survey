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
        while True:
            try:
                print("On a scale of 1-10, rate: Apples, Bananas, and Mangoes")
                question1 = input(
                    "Please separate your answers by commas, for example \n 5,3,10\n")
                # cleaner1, cleaner2, and cleaner3 all serve
                #  to prepare the inputted data for int-conversion
                cleaner1 = question1.split(",")
                # iterates through the list provided from question1, without commas,
                #  and converts to integers for the final answer
                self.answer1 = [int(i) for i in cleaner1]
                # refresher from senderle:
                # https://stackoverflow.com/questions/6009589/how-to-test-if-every-item-in-a-list-of-type-int
                if len(self.answer1) != 3:
                    raise ValueError("You should only put in 3 numbers!")
                for i in self.answer1:
                    if i > 10 or i < 1:
                        raise ValueError(
                            "Please keep your answer between 1 and 10!")
                    if not (int or float):
                        raise ValueError("Please only put in numbers!")
                break
            except ValueError as e:
                print(
                    f"Error! {e} Try again, just numbers this time, and 3 of 'em!")
                continue
        while True:
            try:
                # this entire section works the exact same as the previous one
                print("On a scale of 1-10, rate: Cucumbers, tomatoes, and potatoes.")
                print("Tomatoes aren't technically fruits, but you know what we mean!")
                question2 = input(
                    "Please separate your answers by commas, for example:\n5,3,10\n")
                cleaner2 = question2.split(",")
                self.answer2 = [int(x) for x in cleaner2]
                if len(self.answer2) > 3:
                    raise ValueError("You put in too many numbers!")
                for i in self.answer2:
                    if i > 10 or i < 1:
                        raise ValueError(
                            "Please keep your answer between 1 and 10!")
                    if not (int or float):
                        raise ValueError("Please only put in numbers!")
                break
            except ValueError as e:
                print(
                    f"Error! {e} Try again, just numbers this time, and 3 of 'em!")
                continue
        while True:
            try:
                # section to separate data from non-vegetarians
                if diet in ['no', 'n']:
                    question3 = input(
                        "Beef, chicken, and pork? Please separate your answers by commas, for example \n 5,3,10\n")
                    cleaner3 = question3.split(",")
                    self.answer3 = [int(x) for x in cleaner3]
                    if len(self.answer3) != 3:
                        raise ValueError(
                            "You should only put in 3 numbers!")
                    for i in self.answer3:
                        if i > 10 or i < 1:
                            raise ValueError(
                                "Please keep your answer between 1 and 10!")
                        if not (int or float):
                            raise ValueError("Please only put in numbers!")
                    break
            except ValueError as e:
                print(
                    f"Error! {e} Try again, just numbers this time, and 3 of 'em!")
                continue
            if diet == "no" or "n":
                return self.answer1, self.answer2, self.answer3

    def appender(self, diet, vegetarian, non_vegetarian):
        """
        adds the relevant data from the survey to the vegetarian or non-vegetarian tabs
        converts the answers from survey() to integers (again) so they can be appended
        this method does not touch the statistics page, in the interests of keeping the code
        short
        """
        print("Adding results to spreadsheet...")
        self.answer1 = [int(i) for i in self.answer1]
        self.answer2 = [int(i) for i in self.answer2]

        if diet in ['no', 'n']:
            self.answer3 = [int(i) for i in self.answer3]
            answers = self.answer1 + self.answer2 + self.answer3
            non_vegetarian.append_row(answers)
            print("Results uploaded!")
        if diet in ['yes', 'y']:
            answers = self.answer1 + self.answer2
            vegetarian.append_row(answers)
            print("Results uploaded!")


def stat_calculator(stats, a, b, c, diet):
    """
    Increases the number of responses 
    Uses the number of responses to calculate the average for each column
    Average score depends on if the user is a vegetarian or not
    """
    # figured out how to do all this from gspread documentation
    # https://docs.gspread.org/en/v6.0.0/user-guide.html#finding-a-cell
    stats.update_cell(a, b, c)
    nveg_responses = int(stats.cell(12, 2).value)
    veg_responses = int(stats.cell(12, 3).value)

    if diet in ['yes', 'y']:
        tnumbers_raw = SHEET.worksheet('Vegetarian').get_all_values()[1:]
        tnumbers_int = [[int(i) for i in j] for j in tnumbers_raw]
        # credit: Max Shawabkeh
        # https://stackoverflow.com/questions/2166577/casting-from-a-list-of-lists-of-strings-to-list-of-lists-of-ints-in-python
        tnumbers_list = [0] * 6
        # credit: ninjagecko
        # https://stackoverflow.com/questions/10617045/how-to-create-a-fix-size-list-in-python
        # connects the elements of each list to each other by their corresponding element
        for inner_list in tnumbers_int:
            tnumbers_list = [sum(i) for i in zip(tnumbers_list, inner_list)]
            # this took a ton of trial and erroring, but this ended up being the key
        # gets the average response by dividing
        # each element in tnumbers_list by the number of responses
        tnumbers = [i/veg_responses for i in tnumbers_list]
        # credit https://www.geeksforgeeks.org/divide-all-elements-of-a-list-by-a-number-in-python/

        # converts the list to a list of floats to 2 decimal places
        tnumbers_float = [round(float(i), 2) for i in tnumbers]
        # https://stackoverflow.com/questions/1614236/how-do-i-convert-all-of-the-items-in-a-list-to-floats
        rows = [
            [tnumbers_float[0]],
            [tnumbers_float[1]],
            [tnumbers_float[2]],
            [tnumbers_float[3]],
            [tnumbers_float[4]],
            [tnumbers_float[5]],
        ]
        stats.batch_update(
            [
                {'range': 'C2:C7', 'values': rows}
            ]
        )
        # credit: https://github.com/burnash/gspread/issues/792
    else:
        # everything else in here works the same, just changed to make extra room for meat opinions
        # uses values from the non-vegetarian worksheet, obviously
        tnumbers_raw = SHEET.worksheet('Standard').get_all_values()[1:]
        tnumbers_int = [[int(i) for i in j] for j in tnumbers_raw]
        tnumbers_list = [0] * 9
        for inner_list in tnumbers_int:
            tnumbers_list = [sum(i) for i in zip(tnumbers_list, inner_list)]
        tnumbers = [i/nveg_responses for i in tnumbers_list]
        tnumbers_float = [float(i) for i in tnumbers]
        rows = [
            [tnumbers_float[0]],
            [tnumbers_float[1]],
            [tnumbers_float[2]],
            [tnumbers_float[3]],
            [tnumbers_float[4]],
            [tnumbers_float[5]],
            [tnumbers_float[6]],
            [tnumbers_float[7]],
            [tnumbers_float[8]],
        ]

        stats.batch_update(
            [
                {'range': 'B2:B10', 'values': rows}
            ]
        )


def most_popular(stats, diet):
    """
    Analyzes the statistics page after the averages are updated, and finds the
    most popular food overall
    """
    print("Thank you for completing the survey!")
    if diet in ['yes', 'y']:
        numbers = stats.get('C2:C7')  # gets the values of the relevant columns
        names = stats.get('A2:A7')  # gets the names of the relevant columns
        dct = {name[0]: float(number[0])
               for name, number in zip(names, numbers)}
        # creates a dictionary by alternating between names and numbers
        # structure from:
        # https://www.geeksforgeeks.org/python-dictionary-comprehension/
        favorite = max(dct, key=dct.get)
        # gets the item in dct with the highest value, meaning it's the most popular
        # refresh from A. Coady
        # https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
        # adds the favorite item to the relevant cell
        stats.update_cell(11, 3, favorite)
        print("Here are the average scores for vegetarians:")
        print(dct)
        print(f'The most popular food is...\n{favorite}!')
    elif diet in ['no', 'n']:
        # all of this works the same way, just targets different columns
        numbers = stats.get('B2:B10')
        names = stats.get('A2:A10')
        dct = {name[0]: float(number[0])
               for name, number in zip(names, numbers)}
        favorite = max(dct, key=dct.get)
        stats.update_cell(11, 2, favorite)
        print("Here are the average scores for non-vegetarians:")
        print(dct)
        print(f'The most popular food is...\n{favorite}!')


def main():
    """
    Runs all program functions
    """
    print("Welcome to the Food Survey! You will be asked your opinions on various food groups.\n")
    name = input("What is your name?\n").title()
    # code to restrict this to strings at certain character limits
    while True:  # this isn't in try/except form for simplicity's sake
        diet = input(
            "Are you vegetarian? Please enter 'yes' or 'no'.\n").lower()
        if diet in ['yes', 'y', 'no', 'n']:
            break
        else:
            print('Oops! You can only answer yes or no to this question, try again!')

    print(f'Welcome {name}! Since you answered "{diet}", your survey will be tailored with this in mind!')
    non_vegetarian = SHEET.worksheet('Standard')
    vegetarian = SHEET.worksheet('Vegetarian')
    stats = SHEET.worksheet('Statistics')
    nveg_responses = int(stats.cell(12, 2).value)
    veg_responses = int(stats.cell(12, 3).value)

    b = Big()
    b.survey(diet, name)
    b.appender(diet, vegetarian, non_vegetarian)

    # this allows the actual stat_calculator function to be smaller
    # while doing the background work in (main)
    if diet in ['yes', 'y']:
        stat_calculator(stats, 12, 3, veg_responses + 1, diet)
    else:
        stat_calculator(stats, 12, 2, nveg_responses + 1, diet)
    most_popular(stats, diet)


if __name__ == "__main__":
    main()
