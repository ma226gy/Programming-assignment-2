# Programming Assignment 2 - Database Technology
# Author: Ma'moun Abu-Naseer

import pandas as pan
import numpy as nump
import os


# Reads CSV file
def read_csv(file_location):
    mainPath = os.getcwd()  # Gets Current Path

    # Reading the CSV Tables
    table = pan.read_csv(mainPath + file_location,
                         index_col=False, delimiter=',')

    # NA and N/A will be replaced with None.
    table = table.fillna(nump.nan).replace([nump.nan], [None])

    return table


# Creates a table in the database.
def create_table(mydb, database_name, table, table_name, columns_attributes):
    if mydb.is_connected():
        mcursor = mydb.cursor()

        nump_columns = len(columns_attributes.split(','))
        nump_columns_lst = ["%s"] * nump_columns
        s_values = (','.join(nump_columns_lst))

        mcursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        mcursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} "
                        f"{columns_attributes}")
        print(f"Table '{table_name}' has been created!")

        for i, row in table.iterrows():
            sql = (f"INSERT INTO {database_name}.{table_name} "
                   f"VALUES ({s_values})")
            # Only adds the row if its name is not 0
            # (as the name is the primary key)
            if row[0]:
                mcursor.execute(sql, tuple(row))
                mydb.commit()

        print(f" The table '{table_name}' has successfully been populated!")

    else:
        print("\nNot connected to MySQL \n"
              "Double check your SQL data "
              "(Host, User, Password...) and try again.")
        quit()


# The function for printing Main Menu
def menu_main():
    print("\n-------"
          "\nMain menu:"
          "\n1. List all sellers."
          "\n2. Available phone models at Noor Shop."
          "\n3. Which shops have Martin Jacob favorite brand and their available models."
          "\n4. List the number of models from all phone brands."
          "\n5. Create a view that includes all customers with Apple as their favorite brand."
          "\n6. Show the view that contains all customers with Apple as their favorite brand."
          "\nexit. Ends the program"
          "\n----------")
