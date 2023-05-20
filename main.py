"""
Author: Hardeep Kaur Takhar
Contact: hktakhar@sfu.ca
Date: 2023-05-18
Description: This code retrieves date of birth, date of death, and first paragraph from webpages.
"""

from robotics import Robot
import datetime
import re

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

robot = Robot("Quandrinaut")


def introduce_yourself():

    '''
    Introduces itself by saying its name
    and defining the steps it will take.
    '''

    robot.say_hello()
    robot.introduce_itself()

def is_a_date(list_):
        
        '''
        Checks if the list element is a date or not.


        Argument:
            list_(list): List of strings

        Returns:
            flag(bool): Identifies if the element of the list is a string (True - if it is a string).
            date_val(str): Returns the date from the list of string elements.

        '''
        
        # Uses re library to check if list element is a date 
        # (if yes, we extract that date element):

        date_pattern = r'\d+\s\w+\s\d+'  #Pattern: date + space word + space date
        
        for element in list_:
            if re.search(date_pattern, element):
                # print(element)
                date_val = element
                flag = True  

        flag = False # this flag may become of use when handling other conditions
        return flag, date_val

def process_dates(text_elem_born, text_elem_died):
        
        '''
        Uses strings of the extracted elements to extract dates of birth and death.

        Attributes:
            text_elem_born(str): String containing information retreived from the 'Born' row of the webpage
            text_elem_died(str): String containing information retreived from the 'Died' row of the webpage

        Returns:
            date_of_birth_list(str): List of strings (contains parsed birth date)
            date_of_death_list(str): List of strings (contains parsed death date)
        '''

        # Split the text using '\n' keyword to find the dates
        list_text_elem_born = text_elem_born.split('\n') 
        list_text_elem_died = text_elem_died.split('\n')

        # Extracted date element:
        flag_born, date_of_birth = is_a_date(list_text_elem_born)
        flag_death, date_of_death = is_a_date(list_text_elem_died)

        # condider removing flags
        # Split the extracted dates to obtain a precise date:

        date_of_birth_list = date_of_birth.split(" ")
        date_of_death_list = date_of_death.split(" ")

        return date_of_birth_list, date_of_death_list

def age_calculation(date_of_birth_list, date_of_death_list):
        
        '''
        Uses the list of strings to calculate the age

        Attributes:
            date_of_birth_list(list): List of the strings in the birth date element
            date_of_death_list(list): List of the strings in the birth date element

            Example: ['19', 'March', '1820']

        Returns:
            age(int): Age of the scientist        
        '''

        # Join three date strings to form a single date string
        birth_date = ' '.join(date_of_birth_list[0:3])
        death_date = ' '.join(date_of_death_list[0:3])

        print("Birth date: ",birth_date)
        print("Death date: ", death_date)

        # Convert the birth and death dates to datetime objects
        birth_date = datetime.datetime.strptime(birth_date, '%d %B %Y')
        death_date = datetime.datetime.strptime(death_date, '%d %B %Y')

        # Calculate the age
        age = death_date.year - birth_date.year

        # Check if the death month and day are before the birth month and day
        if (death_date.month, death_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        #print("Age: ", age)
        return age

def print_searched_webpage_for_age(scientist_name = SCIENTISTS[0]):

    '''
    Opens the browser, extracts date of birth and date.
    Calculates the age by using the extracted dates.
    
    Argument:
        scientist_name(str): Name of the Scientist
    '''
    
    webpage_url = "https://en.wikipedia.org/wiki/" + scientist_name

    try:
        robot.open_webpage(webpage_url)
        text_elem_born, text_elem_died = robot.search_date_elements()
        date_of_birth_list, date_of_death_list = process_dates(text_elem_born, text_elem_died)
        age = age_calculation(date_of_birth_list, date_of_death_list)
        print("Age: ", age)
    
    except Exception as e:
        print("An error occurred:", e)
    
def print_first_paragraph(name, flag=True):

    '''
    Print the first paragraph of each Scientist's webpage

    Arguments:
        name(str): Name of the scientist
        flag(bool): Set the flag True if you wish to output the first paragraph    
    '''

    try:
        if flag:
            robot.retrieve_first_paragraph(name)
        else:
            print('Set flag to retrieve first paragraph')
    except Exception as e:
        print("An error occurred:", e)

def print_name_age_for_all(SCIENTISTS):

    '''
    Prints the summary for each scientist iteratively.
    Information about a single scientist may be obtained by 
    modifying the input list SCIENTISTS.
    Closes all the previously opened webpages and says goodbye!


    Argument:
        SCIENTISTS(list): list of strings (Name of the scientists)    
    '''

    for name in SCIENTISTS:
        print("Scientist: ", name)
        print_searched_webpage_for_age(name)
        print("Summary: ")
        print_first_paragraph(name, True)
        print("\n")
    robot.close_webpage()
    robot.say_goodbye()

def main():
    '''
    The robot introduces its name and then sequentially prints information
    (Birth date, death date, and first paragraph from their webpage)
    about the pre-defined names in the list "SCIENTISTS".
    '''

    introduce_yourself()
    print_name_age_for_all(SCIENTISTS)
    #print_searched_webpage_for_age()
    #print_first_paragraph(True)
    
    

if __name__ == "__main__":
    main()
