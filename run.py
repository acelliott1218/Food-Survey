"""
convenient function to call for input prompts
"""
def inputer(prompt):
    return input(prompt)
"""
easy function to call for feedback
""" 
def talker(words):
    print(words)



name = inputer("What is your name?\n").title()
diet = inputer("Are you vegetarian?\n").lower() #this needs to be strictly yes/no, will figure that out

review = talker(f'Welcome {name}! Since you answered "{diet}", your survey will be tailored with this in mind!')

"""
Separates vegetarians from non-vegetarians for data clarity
"""
def survey():
    if diet == "no":
        talker(f"Very good! So, {name}, what do you think about...")
        inputer("Beef, chicken, and pork? Please separate your answers by commas, for example \n 5,3,10\n").int()
        #code to add numeric value to the spreadsheet
        #code to raise exception if the value isn't an integer
    else:
        talker(f"Very good! So, {name}, what do you think about...")
        inputer("Apples?").int()
        #code to add numeric value to the spreadsheet
        #code to raise exception if the value isn't an integer
survey()

"""
To be added:
Test-taker's overall results from survey page, average value for each section, and how many times the survey has been taken
"""