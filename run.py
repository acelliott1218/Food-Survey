#need to connect to spreadsheet


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
    Separates vegetarians from non-vegetarians for data clarity
    """
    talker("Let's get started! What do you think of...")
    question1 = inputer("Apples, Bananas, and Mangoes? Please separate your answers by commas, for example \n 5,3,10\n")
    talker("Very good! Moving onto vegetables, what do you think of...")
    question2 = inputer("Cucumbers, tomatoes, and potatoes?\n Tomatoes aren't technically fruits, but you know what we mean! Please separate your answers by commas, for example \n 5,3,10\n ")
    #code to add +1 to survey respondents
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
    print(answer1,answer2)
    return answer1, answer2

# function to add survey results to relevant spreadsheet

# function to calculate average responses

# function to calculate most popular food

def main():
    info = talker("Welcome to the Food Survey! You will be asked your opinions on various food groups.\n")
    name = inputer("What is your name?\n").title()
    diet = inputer("Are you vegetarian?\n").lower() #this needs to be strictly yes/no, will figure that out
    review = talker(f'Welcome {name}! Since you answered "{diet}", your survey will be tailored with this in mind!')
    survey(diet, name)

if __name__ == "__main__":
    main()


# To be added:
# Test-taker's overall results from survey page, average value for each section, and how many times the survey has been taken
# Favorite food from each category (fruits, vegetables, meat) for vegetarians and non-vegetarians
