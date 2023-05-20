"""
Author: Hardeep Kaur Takhar
Contact: hktakhar@sfu.ca
Date: 2023-05-18
Description: This code retrieves date of birth, date of death, and first paragraph from webpages.
"""

from RPA.Browser.Selenium import Selenium

import sys

br = Selenium()

class Robot:
    '''
    The Robot class represents a robot that scrapes wikipedia webpages
    to obtain birth date and death date of the inquired scientists
    and then calculates their age at the time of their death.
    It also extracts first paragraph of their respective webpages.

    Attributes:
        name(str): Name of the robot

    Methods:
        say_hello(): Introduces its name.
        say_goodbye(): Says goodbye during the closing session.
        introduce_itself(): Summarizes the steps it will take to calculate the age.
        open_webpage(): Opens the webpage automaticall using a available browser.
        close_webpage(): Closes all the previously opened browsers.
        retrieve_first_paragraph(): Extracts the first paragraph from the opened webpage and is presented as summary to the user.
        search_date_elements(): Searches the tabular data in the opened webpage to return column data for rows with labels "Born" and "Died".
    '''

    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("Hello, my name is " + self.name)

    def say_goodbye(self):
        print("Goodbye, my name is " + self.name)

    def introduce_itself(self):
        '''
        Summarizes the steps it will take to calculate the age
        and the information it will present to the user.    
        '''
        print("I will be exploring wikipedia page to identify the age lived by the respective scientists.")
        print("First I will identify their date of birth")
        print("Then I will identify their date of death")
        print("I will also share summary about them.")
        print("Let's get started!\n")

    def open_webpage(self, webpage):
        '''
        Attempts to open the webpage and throws an exception if the URL is invalid.
        
        Argument:
            webpage(str): URL
        '''
        try:
            br.open_available_browser(webpage)
        except Exception as e:
            print("An error occurred:", e)

    def retrieve_first_paragraph(self, name):

        '''
        Extracts the first paragraph from the opened webpage and is 
        printed as a summary for the user.
        '''

        # The xpath is defined to target the first paragraph.
        search_first_paragraph = "xpath://*[@id='mw-content-text']/div[1]/p[2]"

        if name == 'Marie Curie':
            search_first_paragraph = "xpath://*[@id='mw-content-text']/div[1]/p[3]"

        # find_elements function fetches the element from the HTML page.
        paragraph_elem = br.find_elements(search_first_paragraph)
        
        # Prints the entire  first paragraph.
        for element in paragraph_elem:
            print(element.text)
        
    def close_webpage(self):

        '''
        Closes all the previously opened browsers.
        '''

        br.close_all_browsers()


    def search_date_elements(self):
        '''
        Searches the tabular data in the opened webpage to 
        return column data for rows with labels "Born" and "Died".

        Return:
            text_elem_born(str): Text retreived from the 'Born' row of the webpage (right column).
            text_elem_died(str): Text retreived from the the 'Died' row of the webpage (right column).
        '''

        try:
        # keyword to obtain row data elements by using xpath:
            search_row_keys= "xpath://th[@scope='row'][@class='infobox-label']"
            row_elem = br.find_elements(search_row_keys)

            # keyword for obtain column data elements for the respective row by using xpath:
            search_col_keys= "xpath://td[@class='infobox-data']"
            column_elem = br.find_elements(search_col_keys)

        # handle exceptions if elements are not found
        except Exception as e:
            print("An error occurred:", e)
        
        # Obtain the index of the Born and Died elements by creating a dictionary
        # with keys: 'Born' and 'Died' and indexes of these elements fetched using
        # find_elements are stored as values.
         
        # Variable i counts iteration. Currently the webpage structure has first 
        # two rows with label 'Born' and 'Died' (therefore we search only twice)
        # And if these keywords are not found probably wikipedia doesn't contain the death date.

        i=0
        date_dic={}
        for result in row_elem:
            try:
                if i!=2: # checks if the first two rows are Born or Died
                    #print(result.text)
                    if result.text =='Born':
                        date_dic['Born']= i # obtain index of Born keyword
                    
                    elif result.text == 'Died':
                        date_dic['Died'] = i # obtain index of Died keyword
                    i+=1
                
                elif i == 2: 
                    if (len(date_dic) == 2): # Checks if both born and dies elements have been fetched
                        break

                    elif (result.text!= 'Born' or 'Died'): # Checks if third element is Born or Died
                        print("This page does not contain Death Date for this person")
                        print("Or either this person is alive.")
                        #print("Enter a valid value")
                        raise ValueError("Invalid value") 

            except ValueError as e: # throws an exception if the page does not have these keywords
                print("Error:", str(e)) 
                sys.exit(1)    

        # Now that we have indexes for the Born and Died rows.
        # We use these indexes to obtain the data for the respective rows.

        # Get values (indexes) of keys 'Born' and 'Died'
        indx_born = date_dic.get('Born')
        indx_died = date_dic.get('Died') 

        # We return text stored in Born and Died elements:
        text_elem_born = column_elem[indx_born].text
        text_elem_died = column_elem[indx_died].text

        return text_elem_born, text_elem_died

