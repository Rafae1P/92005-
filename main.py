'''This program is an example of what the Te Puia database managment interface could look like. This python file uses
the sqlite3 library to connect to a sqlite database and uses the tabulate library to present tables.
By Rafael Percy
Date 19-09-2025'''

import sqlite3
from tabulate import tabulate
import os

#This is the main function that produces the home screen and handles the user input for the home screen
def main_function():
    while True:

        print_home_screen()

        user_option_selected = input(": ")
        

        # if statement that handles what the user selected
        if user_option_selected == "1":

            customer_table_loop()

        elif user_option_selected == "2":

            order_table_loop()


        elif user_option_selected == "3":

            inventory_table_loop()

        #if the user enters 4 this while loop will break and the program will stop
        elif user_option_selected == "4":

            break

        #catching any errors
        else:
            print("Please enter a number between 1-4")


#this function just prints out the home screen text
def print_home_screen():
    print('''-----Home Menu-----
Too search, delete, or update certain data view the corrasponding table
Enter the corrasponding number to the option you would like to select:

1 View all Customer information
2 View all Orders
3 View Inventory
4 Exit''')


#these next three functions reitarate their respictive menu when the user is viewing a table until the user selects 4
# which will return "back" thus returning the user to the home menu
def customer_table_loop():

    table_menu_value = ""

    while table_menu_value != "back":

        headings = ["Customer_ID", "Surname", "First_Name", "Address", "Email"]
        alignments = ("left", "left", "left", "left", "left")

        #calls the show_table function which will print the table with the tabulate library
        show_table('SELECT * FROM customer;', headings, alignments)

        #calls the table_menu function which will print the table menu when viewing a table and handle the user input
        # when the user is viewing a table
        table_menu_value = table_menu("customer")



def order_table_loop():

    table_menu_value = ""

    while table_menu_value != "back":

        headings = ["Order_ID", "Order_Date", "Customer_ID", "Product_ID", "Order_Quantity"]
        alignments = ("left", "left", "left", "left", "center")

        #calls the show_table function which will print the table with the tabulate library
        show_table('SELECT * FROM "order";', headings, alignments)

        #calls the table_menu function which will print the table
        # menu when viewing a table and handle the user input when the user is viewing a table
        table_menu_value = table_menu('"order"')
        



def inventory_table_loop():

    table_menu_value = ""

    while table_menu_value != "back":

        headings = ["Product_Id", "Product_Name", "Price", "Quantity", "Number_Sold"]
        alignments = ("left", "left", "left", "center", "center")

        #calls the show_table function which will print the table with the tabulate library
        show_table("SELECT * FROM inventory;", headings, alignments)

        #calls the table_menu function which will print the table menu when viewing a table and handle the user input
        # when the user is viewing a table
        table_menu_value = table_menu("inventory")
        


#function which will the recive the tabulate configurations and print out the selected table
def show_table(query, heading_config, alignment_config):

    #setting up the database connection and cursor
    database_connection = sqlite3.connect("92005_database.db")
    cursor = database_connection.cursor()

    cursor.execute(query)
    records = cursor.fetchall()

    #prints out the table with the tabualte configurations
    print(tabulate(records, heading_config, tablefmt="plain", colalign = alignment_config))

    #closes the database connection
    database_connection.commit()
    database_connection.close()


#function that prints out and handles the user input in the table menu
def table_menu(table_name):

    #while loop to reiterate through the menu incase the user entered a not valid input
    while True:

        print('''
    ----------Table Menu-----------
    
    1 Add
    2 Delete
    3 Search
    4 Back''')

        user_option_selected = input(": ")

        #if statement that handles the user input
        if user_option_selected == "1":

            add_to_table_menu(table_name)
            
            break

        elif user_option_selected == "2":

            delete_from_table_menu(table_name)
            
            break

        elif user_option_selected == "3":

            search_table_menu(table_name)
            
            break

        elif user_option_selected == "4":

            return "back"

        #else to catch any not valid input
        else:
            print("Error please select a number between 1-4")


#function that prints out the add to table menu and handles user input
def add_to_table_menu(table_name):

    #while loop to reitierate if there is an error
    while True:

        try:

            print('To add records to the table please sepearate each record with "; " and each field with ", " (including the space)')
            records_to_be_added = input(": ")

            #calls add_records function which will add the records to the table
            add_records(records_to_be_added, table_name)
            
            break

        except:

            print("Error please check you have added the correct amount of fields and spaced each field/record out properly")


# function which prints out the delete from table menu and handles user input
def delete_from_table_menu(table_name):

    #while loop to reitierate if there is an error
    while True:

        try:

            print("To delete a record please enter the record's id (left most field)")
            record_to_be_deleted_pk = input(": ")

            #calls delete record function which will delete the record
            delete_record(record_to_be_deleted_pk, table_name)
            
            break

        except:

            print("Error that primary key does not exist please check for a valid primary key")



def search_table_menu(table_name):

    #while loop to reiterate if there is an error
    while True:

        try:

            print('To search this table please enter any number or term and the column you would like to search seperated by ", " (including the space)')

            #splits the input into a list and then makes sure that the column name is lower case
            term_and_column = input(": ").split(", ")
            term_and_column[1] = term_and_column[1].lower()

            #calls search_table function which will search and print out the record(s) the user asked for
            serch_and_return_record(table_name, term_and_column)
            
            break

        except:

            print("Error that column doesn't exist please check you have spelt it wrong (spaces should be replaced with _ )")

#function that adds records to the database
def add_records(user_data, table_name):

    #calls the convert to list of tuples function to seperate each record from eachother and converts each record into a
    #tuple
    user_data = convert_to_list_of_tuples(user_data)

    #loops through the list of records and adds them to the database
    for record in user_data:

        sql_statement = f"INSERT INTO {table_name} VALUES {record}"

        #calls run sql statement function which will run the sql statment thus adding the record to the database
        run_sql_statement(sql_statement)



#this function deletes a record but double checks with the user first
def delete_record(record_to_be_deleted_pk, table_name):

    #sets the pk of the table
    primary_key_column_name = f"{table_name}_id"

    record_to_be_deleted_query = f"SELECT * FROM {table_name} WHERE {primary_key_column_name} = {record_to_be_deleted_pk}"

    #calls run sql query which will return the record that the user wants to delete
    record_to_be_deleted = run_sql_query(record_to_be_deleted_query)

    #while loop to reiterate if there is an error
    while True:

        #double checks with user
        double_check = input(f"Are you sure you want to delete {record_to_be_deleted}? y/n : ")
        

        if double_check == "y":

            sql_delete_statement = f"DELETE FROM {table_name} WHERE {primary_key_column_name} = {record_to_be_deleted_pk}"
            #calls run sql statement that will delete the record
            run_sql_statement(sql_delete_statement)

            #breaks out of the loop and returns to the table menu
            break

        elif double_check == "n":

            #breaks out of the loop and returns to the table menu
            break

        #else statement to catch any errors
        else:

            print("Please enter y or n")


#function that runs a query on the database and prints the selected record(s)
def serch_and_return_record(table_name, term_and_column):

    #seperates the term and the column given by the user
    term = term_and_column[0]
    column = term_and_column[1]

    sql_query = f"SELECT * FROM {table_name} WHERE  {column} LIKE '%{term}%';"

    #calls run sql query which will return the record(s)
    record = run_sql_query(sql_query)

    print(*record)
    
    
#this function converts a string into a list filled with tuples which is used when adding multiple records to a table
def convert_to_list_of_tuples(string):

    #inner and outer dilimiters set
    inner_delimiter = ", "
    outer_delimiter = "; "

    #temporary list wich does not contain tupels
    temporary_list = string.split(outer_delimiter)

    #set the double list that will be returned
    double_list = []

    for record in temporary_list:

        record = record.split(inner_delimiter)
        record = tuple(record)

        double_list.append(record)

    return double_list

#this function will run a sql statement which is used for adding and deleting records
def run_sql_statement(sql_statment):

    #connecting to database
    database_connection = sqlite3.connect("92005_database.db")
    cursor = database_connection.cursor()

    cursor.execute(sql_statment)

    #closing connection
    database_connection.commit()
    database_connection.close()

#this function will run a query and return any record(s) found
def run_sql_query(query):

    #connecting to database
    database_connection = sqlite3.connect("92005_database.db")
    cursor = database_connection.cursor()

    cursor.execute(query)
    record = cursor.fetchall()

    #closeing connection
    database_connection.commit()
    database_connection.close()

    return record





if __name__ == '__main__':

    
    print("Welcome to the Te Puia database managment interface.")

    main_function()

    print("Interface closed")