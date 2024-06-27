# Training Generator
# Database with different exercises
# sqlite3
# https://www.tutorialspoint.com/sqlite/sqlite_create_database.htm
#
# Database structure:
# Columns:
# 1. Exercise name - The exercise should have an easy to identify name
# 2. Description text - should describe the exercise
# 3. Description link - Link to picture or video
# 4. Skill level - all, kids, normal, rambo, senior, beginners
# 5. Type of training - warming up, game, strength, stretching, balance, reaction
# 6. Body part - legs, upper body, shoulder and arms
# 7. Equipment needed - 1 soft-ball, several soft-balls, bean bags, pistarit, tennis balls, stretching band
# 8. Amount of persons - 1,2,3,4,5,6,7,8 or more
# 9. Not suitable for - knees, back, breast, hip, neck, ankle
# 10. Duration - x minutes
# 11. Variants - Variants of the exercise (e.g., backwards, sidewards etc.)
# 12. Comments - optional free text
# 13. Backup - just in case I need a field more

# Main UI
# User selects task (after that he is returned to here):
# - Do you want to add an exercise?
# - Do you want to create a training plan?
# - Modify an existing training plan?
# - Do you want to view all the exercises in the database?
# - Do you want to edit/remove an exercise?

# Crate training plan function (after "want to create a training plan")
#
# User choose from dropdown menu:
# age, type, body part, equipment need, amount of persons, not suitable for
# This is repeated till he says "enough exercises" (age is cached)
# Outcome: Training plan, sorting for warming up, main training, in-between games, flexing

# Planned functions
# Adding of new exercises
# Modification of entries in the database
# Listing of all exercises in the database in a readable format
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
    def store_exercise_elements(cursor_intern, entry1_int, entry2_int, entry3_int, skill_level_details_int,
                                training_type_details_int, equipment_material_int,
                                entry7_int, entry8_int, entry9_int, entry10_int, entry11_int, entry12_int,
                                element13_int):

        element1 = entry1_int.get()  # 1. Exercise Name
        element2 = entry2_int.get()  # 2. Exercise Description
        element3 = entry3_int.get()  # 3. Exercise Link

        # 4. Skill Level - Multiple Choice entry by user to be stored for the skill level (formerly categories)
        selected_skill_level = [skill_level for skill_level, j in skill_level_details_int.items() if j.get()]
        element4 = ", ".join(selected_skill_level)  # Join selected skill levels

        # 5. Type of training - warming up, game, strength, stretching, balance, reaction
        selected_type_of_training = [training_type for training_type, j in training_type_details_int.items() if j.get()]
        element5 = ", ".join(selected_type_of_training)  # Join selected training types

        # 6. Needed Equipment


        # CHECK BELOW WHICH GET NORMAL TEXT!!

        element6 = entry6_int.get()
        element7 = entry7_int.get()
        element8 = entry8_int.get()
        element9 = entry9_int.get()

        #####################
        element10 = entry10_int.get()  # 10. Duration - x minutes
        element11 = entry11_int.get()  # 11. Variations
        element12 = entry12_int.get()  # 12. Comments
        element13 = "Backup field"
        # element13 = entry12.get()  # Backup field can be used if the DB needs one column more

        new_exercise.append((element1, element2, element3, element4, element5, element6, element7,
                             element8, element9, element10, element11, element12, element13))

        # Cleaning of input fields
        entry1_int.delete(0, 'end')  # Clear the input fields for text input 1. Exercise Name
        entry2_int.delete(0, 'end')  # Clear the input fields for text input 2. Exercise Description
        entry3_int.delete(0, 'end')  # Clear the input fields for text input 3. Exercise Link

        # Cleaning of input field 4. Skill Level
        for j in skill_level_details_int.values():
            j.set(0)  # Reset checkbox values

        # Cleaning of input field 5. Training Type
        for j in training_type_details_int.values():
            j.set(0)  # Reset checkbox values

        # CLEAN OTHER ELEMENTS
        # Store exercise elements in the database
        for exercise in new_exercise:
            cursor_intern.execute("INSERT INTO tbl1 (name, description, link, skill_level, training_type, body_part, "
                                  "equipment, num_persons, not_suitable, duration, variations, comments, backup) "
                                  "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)", exercise)

        conn.commit()  # Commit the changes to the database

        print("Exercise elements added successfully!")

    def create_popup_for_viewing_exercise():  # Function to create a pop-up window to view the inserted exercise
        popup = tk.Toplevel()
        popup.title("Exercise that was inserted:")
        popup.geometry("600x250")
        # Not working right now, to be updated when input of exercise is ok
        for j, (element1, element2, element3) in enumerate(new_exercise):
            label = tk.Label(popup, text=f"Exercise {j + 1}:")
            label.pack()
            label1 = tk.Label(popup, text=f"Name: {element1}")
            label1.pack()
            label2 = tk.Label(popup, text=f"Description: {element2}")
            label2.pack()
            label3 = tk.Label(popup, text=f"Type of exercise: {element3}")
            label3.pack()

    def user_input(cursor_intern):
        # Initialize the main window for inserting the exercise details
        root = tk.Tk()
        root.title("Exercise Input")

        # Definition of Labels for each entry
        # 1. Exercise name - The exercise should have an easy to identify name
        label1 = tk.Label(root, text="Enter the name of the exercise (Exercise name):")
        # 2. Description text - should describe the exercise
        label2 = tk.Label(root, text="Enter the description of the exercise:")
        # 3. Description link - Link to picture or video (text format)
        label3 = tk.Label(root, text="Enter a link to a video or picture (if not just press enter):")
        # 4. Skill level - all, kids, normal, rambo, senior, beginners
        label4 = tk.Label(root, text="Select skill level from menu:")
        # 5. Type of training - warming up, game, strength, stretching, balance, reaction
        label5 = tk.Label(root, text="What kind of training is this exercise (select from menu):")
        # 6. Body part - legs, upper body, shoulder and arms
        label6 = tk.Label(root, text="Which body part is trained in this exercise (select from menu):")
        # 7. Equipment needed - soft-ball, several soft-balls, bean bags, pads, tennis balls, stretching band
        label7 = tk.Label(root, text="What kind of equipment do you need (select from menu):")
        # 8. Amount of persons - 1,2,3,4,5,6,7,8 or more
        label8 = tk.Label(root, text="How many persons are needed at least to perform this exercise (select from "
                                     "menu):")
        # 9. Not suitable for - knees, back, breast, hip, neck, ankle
        label9 = tk.Label(root, text="For what / whom is this exercise NOT suitable (select from menu):")
        # 10. Duration - x minutes
        label10 = tk.Label(root, text="How long will the exercise take (optional, if you do not know just press "
                                      "return):")
        # 11. Variations - optional free text
        label11 = tk.Label(root, text="Variations:")
        # 12. Comments - optional free text
        label12 = tk.Label(root, text="Comments:")
        # 13. Backup - just in case I need a field more
        label13 = tk.Label(root, text="Backup:")
        labels = [label1, label2,label3, label4, label5, label6, label7, label8, label9, label10, label11, label12,
                  label13]

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
        entry11 = tk.Entry(root)
        entry12 = tk.Entry(root)
        entry13 = tk.Entry(root)

        label1.pack()
        entry1.pack()
        label2.pack()
        entry2.pack()
        label3.pack()
        entry3.pack()

        # Checkboxes for skill level (4. Element)
        label4.pack()

        # Checkboxes for skill level (4. Element)
        skill_level_details = {
            "All": IntVar(),
            "Kids": IntVar(),
            "Normal (lower belt)": IntVar(),
            "Advanced (upper belt)": IntVar(),
            "Very advanced (rambo)": IntVar(),
            "Senior": IntVar(),
            "Beginners": IntVar(),
            "Other": IntVar()
        }
        entry4.pack()

        label5.pack()  # Question for Training Type

        # Checkboxes for training type (5. Element)
        training_type_details = {
            "Game": IntVar(),
            "Warming Up": IntVar(),
            "Strength": IntVar(),
            "Duration": IntVar(),
            "Balance": IntVar(),
            "Reaction": IntVar(),
            "Stretching": IntVar(),
            "Taekwondo": IntVar(),
            "Other": IntVar()
        }

        label5 = tk.Label(root, text=labels[4])
        label5.pack()
        for training_type, var in training_type_details.items():
            checkbox = tk.Checkbutton(root, text=training_type, variable=var)
            checkbox.pack(anchor='w')
        # for training_type, i in training_type_details.items():
        #    checkbox = tk.Checkbutton(root, text=training_type, variable=i)
        #    checkbox.pack()

        entry5.pack()

        label6.pack()  # Question for equipment needed
        equipment_material_details = {

            "1-2 Soft Ball": IntVar(),
            "Soft Ball per person": IntVar(),
            "Soft Ball per two persons": IntVar(),
            "Tennis Ball per person": IntVar(),
            "Tennis Ball per two persons": IntVar(),
            "Bean Bags": IntVar(),
            "Stretching Band": IntVar(),
            "Kicking pads (small)": IntVar(),
            "Kicking pads (large)": IntVar()
        }

        # Create and pack the checkboxes
        for equipment_material, var in equipment_material_details.items():
            checkbox = tk.Checkbutton(root, text=equipment_material, variable=var)
            checkbox.pack(anchor='w')

        # Create a label and text entry for "Other" directly under the checkboxes
        other_label = tk.Label(root, text="Other (insert text):")
        other_label.pack(anchor='w')
        other_entry = tk.Entry(root, width=50)
        other_entry.pack(anchor='w')

        entry6.pack()

        label7.pack()
        entry7.pack()
        label8.pack()
        entry8.pack()
        label9.pack()
        entry9.pack()
        label10.pack()
        entry10.pack()
        label11.pack()
        entry11.pack()
        label12.pack()
        entry12.pack()
        label13.pack()
        entry13.pack()

        # Create a "Done" button to store the exercise elements
        done_button = tk.Button(root, text="Done",
                                command=lambda: store_exercise_elements(cursor_intern, entry1, entry2,
                                                                        entry3, skill_level_details,
                                                                        training_type_details,
                                                                        equipment_material_details,
                                                                        entry6, entry8, entry9,
                                                                        entry10, entry11, entry12))


        # Create a "View Exercises" button to open the pop-up window
        view_button = tk.Button(root, text="View Exercises", command=create_popup_for_viewing_exercise)
        view_button.pack(pady=5)

        # Create an array to store the exercise elements
        # new_exercise = []
        # Create labels and entry fields
        # label1 = tk.Label(root, text="Enter the name of the exercise:")
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

        # Create a "Stop" button to stop insertion
        # stop_button = tk.Button(root, text="Stop", command=stop_insertion)
        # stop_button.pack(pady=5)
        root.mainloop()
    user_input(cursor)


def search_and_display(cursor):
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
    # search_name = input("Enter the name to search: ")
    # search_contact_by_name(search_name)

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
    insert_new_exercise(cursor)

    # Call the function to search and display exercises
    search_and_display(cursor)

    # Close the cursor and the connection
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()

