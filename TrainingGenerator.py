# Training Generator
# Database with different exercises
# sqlite3
# https://www.tutorialspoint.com/sqlite/sqlite_create_database.htm
#
# Database structure:
# Columns:
# Exercise name - The exercise should have an easy to identify name
# Description text - should describe the exercise
# Description link - Link to picture or video
# Skill level - all, kids, normal, rambo, senior, beginners
# Type of training - warming up, game, strength, stretching, balance, reaction
# Body part - legs, upper body, shoulder and arms
# Equipment needed - 1 soft-ball, several soft-balls, bean bags, pistarit, tennis balls, stretching band
# Amount of persons - 1,2,3,4,5,6,7,8 or more
# Not suitable for - knees, back, breast, hip, neck, ankle
# Duratation - x minutes
# 

# Intended usage:
# User choose from dropdown menu:
# age, type, body part, equipment need, amount of persons, not suitable for
# This is repeated till he says "enough exercises" (age is cached)
# Outcome: Training plan, sorting for warming up, main training, in-between games, flexing

# Additional features
# Adding of exercises
# Modification of entries in the database
# Modification of received trainings plan

import sqlite3
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import tkinter as tk
from tkinter import IntVar


def insert_new_exercise(cursor):  # this function is for adding new exercises to the database
    new_exercise = []  # Initialize a list to store exercise elements

    # Create a function to store the sentences in an array
    def store_exercise_elements():
        element1 = entry1.get()  # Exercise Name
        element2 = entry2.get()  # Exercise Description
        element3 = entry3.get()  # Exercise Link

        # Multiple Choice entry by user to be stored for the skill level (formerly categories)
        selected_skill_level = [skill_level for skill_level, vari in skill_level_vars.items() if vari.get()]
        element4 = ", ".join(selected_skill_level)  # Join selected skill levels

        ########CHECK BELOW WHICH GET NORMAL TEXT!!!

        element5 = entry5.get()
        element6 = entry6.get()
        element7 = entry7.get()
        element8 = entry8.get()
        element9 = entry9.get()
        element10 = entry10.get()

        new_exercise.append((element1, element2, element3, element4, element5, element6, element7,
                             element8, element9, element10))

        entry1.delete(0, 'end')  # Clear the input fields
        entry2.delete(0, 'end')
        for vari in skill_level_vars.values():
            vari.set(0)  # Reset checkbox values

        # CLEAN OTHER ELEMENTS

        print("Exercise elements added successfully!")

    def create_popup():  # Function to create a pop-up window
        popup = tk.Toplevel()
        popup.title("Insert Exercises to Database")
        popup.geometry("600x250")

        for i, (element1, element2, element3) in enumerate(new_exercise):
            label = tk.Label(popup, text=f"Exercise {i + 1}:")
            label.pack()
            label1 = tk.Label(popup, text=f"Name: {element1}")
            label1.pack()
            label2 = tk.Label(popup, text=f"Description: {element2}")
            label2.pack()
            label3 = tk.Label(popup, text=f"Type of exercise: {element3}")
            label3.pack()

    # Initialize the main window
    root = tk.Tk()
    root.title("Exercise Input")

    label1 = tk.Label(root, text="Enter the name of the exercise (Exercise name):")
    label2 = tk.Label(root, text="Enter the description of the exercise:")
    label3 = tk.Label(root, text="Enter a link to a video or picture (if not just press enter):")
    label4 = tk.Label(root, text="Select skill level from menu:")
    label5 = tk.Label(root, text="What kind of training is this exercise (select from menu):")
    label6 = tk.Label(root, text="Which body part is trained in this exercise (select from menu):")
    label7 = tk.Label(root, text="What kind of equipment do you need (select from menu):")
    label8 = tk.Label(root, text="How many persons are needed at least to perform this exercise (select from menu):")
    label9 = tk.Label(root, text="For what / whom is this exercise NOT suitable (select from menu):")
    label10 = tk.Label(root, text="How long will the exercise take (optional, if you do not know just press return):")

    # Exercise name - The exercise should have an easy to identify name
    # Description text - should describe the exercise
    # Description link - Link to picture or video
    # Skill level - all, kids, normal, rambo, senior, beginners
    # Type of training - warming up, game, strength, stretching, balance, reaction & sparring
    # Body part - legs, upper body, shoulder and arms, cardio, all
    # Equipment needed - none, 1 soft-ball, several soft-balls, bean bags, pistarit, tennis balls,
    # stretching band, other (multiple entries possible and free text with other)
    # Amount of persons - 1,2,3,4,5,6,7,8 or more (only one entry)
    # Not suitable for - None, kids, beginners, knees, back, breast, hip, neck, ankle (multiple entries possible)
    # Duration - x minutes (optional)

    entry1 = tk.Entry(root)
    entry2 = tk.Entry(root)
    entry3 = tk.Entry(root)
    entry4 = tk.Entry(root)
    entry5 = tk.Entry(root)
    entry6 = tk.Entry(root)
    entry7 = tk.Entry(root)
    entry8 = tk.Entry(root)
    entry9 = tk.Entry(root)
    entry10 = tk.Entry(root)

    label1.pack()
    entry1.pack()
    label2.pack()
    entry2.pack()
    label3.pack()
    entry3.pack()
    label4.pack()
    entry4.pack()
    label5.pack()
    entry5.pack()
    label6.pack()
    entry6.pack()
    label7.pack()
    entry7.pack()
    label8.pack()
    entry8.pack()
    label9.pack()
    entry9.pack()
    label10.pack()
    entry10.pack()
    # Checkboxes for exercise categories
    category_vars = {
        "Games": IntVar(),
        "Warming Up": IntVar(),
        "Stretching": IntVar(),
        "Taekwondo": IntVar()
    }

    for category, var in category_vars.items():
        checkbox = tk.Checkbutton(root, text=category, variable=var)
        checkbox.pack()

    # Create a "Done" button to store the exercise elements
    done_button = tk.Button(root, text="Done", command=store_exercise_elements)
    done_button.pack()

    # Create a "View Exercises" button to open the pop-up window
    view_button = tk.Button(root, text="View Exercises", command=create_popup)
    view_button.pack(pady=5)

    # Create an array to store the exercise elements
    # new_exercise = []
    # Create labels and entry fields
    #label1 = tk.Label(root, text="Enter the name of the exercise:")
    # label2 = tk.Label(root, text="Enter the description of the exercise:")
    # label3 = tk.Label(root, )
    # entry1 = tk.Entry(root)
    # entry2 = tk.Entry(root)

    # label1.pack()
    # entry1.pack()
    # label2.pack()
    # entry2.pack()
    # Create a "Done" button to store the sentences
    # done_button = tk.Button(root, text="Done", command=store_exercise_elements)
    # done_button.pack()

    view_button = tk.Button(root, text="View Exercise Elements", command=create_popup)
    view_button.pack(pady=5)

    # Create a "Stop" button to stop insertion
    stop_button = tk.Button(root, text="Stop", command=stop_insertion)
    stop_button.pack(pady=5)

    root.mainloop()



def Search_and_Display(cursor):
    # Function for searching and displaying
    # Function to search for a contact by name and display it
    # def search_contact_by_name(name):
    #    cursor.execute("SELECT * FROM contacts WHERE name=?", (name,))
    #    contact = cursor.fetchone()
    #    if contact:
    #        print(f"Contact found: ID={contact[0]}, Name={contact[1]}, Email={contact[2]}")
    #    else:
    #        print(f"No contact found with the name: {name}")

    # Search for a contact by name
    #search_name = input("Enter the name to search: ")
    #search_contact_by_name(search_name)

    # Test if db work
    # Execute a SELECT query to retrieve data from the table
    # cursor.execute("SELECT * FROM tbl1")

    # Fetch all the rows from the result set
    rows = cursor.fetchall()

    # Print the contents of the table
    for row in rows:
        print(f" Name of exercise: {row[0]}, Description: {row[1]}")



def main():

    # Connect to the SQLite database (or create one if it doesn't exist)
    conn = sqlite3.connect('test2.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table (if it doesn't exist) to store data
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')

    # Call the function to insert new exercise and display it
    Insert_New_Exercise(cursor)

    # Call the function to search and display exercises
    Search_and_Display(cursor)

    # Close the cursor and the connection
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
