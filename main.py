# Programming Assignment 2 - Database Technology
# Author: Ma'moun Abu-Naseer
import errno
from re import I
from attr import field
import mysql.connector
import methods as met
from mysql.connector import errorcode


def main():
    # Information needed to connect to SQL.
    # Change the variables accordingly:
    sql_user = "root"
    sql_pass = "root"
    sql_host = "localhost"
    db_name = "PA2_phones"

    # Tries to connect to mySQL, and closes the program if the information is incorrect.
    try:
        mydb = mysql.connector.connect(
            host=sql_host,
            user=sql_user,
            passwd=sql_pass
        )
        mcursor = mydb.cursor()
    except Exception:
        print("\nCouldn't connect to MySQL!\n"
              "Double check your SQL data in main.py "
              "(Host, User, Password...) and try again.")
        return
    else:
        print("\nConnected to MySQL!")

    # Fetching all databases named PA2-Phones
    mcursor.execute(f"SHOW DATABASES LIKE '%{db_name}%'")
    mresult = mcursor.fetchall()

    # If mresult = 0 then database PA2-Phones does not exist.
    if (len(mresult) == 0):
        print(f"\nThe database '{db_name}' does not exist.\n"
              f"Creating '{db_name}'...")

        # Creates database PA2-Phones
        mcursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

        # Connecting to the Database
        mcursor.execute(f"USE {db_name}")
        print(f"Connected to '{db_name}'!")

        # Reading CSV Files
        print("\nReading the CSV Files...")
        phones_table = met.read_csv('\\data\\phones.csv')
        customers_table = met.read_csv('\\data\\customers.csv')
        sellers_table = met.read_csv('\\data\\sellers.csv')

        # Creating phones table
        met.create_table(
            mydb,
            db_name,
            phones_table,
            "phones",

            "(phone_id INT PRIMARY KEY,"
            "phone_brand VARCHAR(20),"
            "model_name VARCHAR(20),"
            "size_in INT(1),"
            "year_announced INT(4))"
        )

        # Creating the customers table
        met.create_table(
            mydb,
            db_name,
            customers_table,
            "customers",

            "(customer_id INT PRIMARY KEY,"
            "first_name VARCHAR(10),"
            "last_name VARCHAR(10),"
            "salary INT,"
            "fav_brand VARCHAR(10))"
        )

        # Creating the sellers table
        met.create_table(
            mydb,
            db_name,
            sellers_table,
            "sellers",

            "(seller_id INT PRIMARY KEY,"
            "seller_name VARCHAR(30),"
            "available_brand VARCHAR(10),"
            "country VARCHAR(30))"
        )

    # To avoid repopulating the database everytime the program is run,
    # the tables will not be changed if the database already exists.
    # so if mresult is not = 0 then the tables are untouched.
    else:
        print(f"\nThe database '{db_name}' already exists.\n"
              f"Connecting to '{db_name}' ...")

        # Connecting to database
        mcursor.execute(f"USE {db_name}")
        print(f"Connected to '{db_name}'!")

    print("\n----------")
    user_input = input("Press any key to access main menu "
                       "(and exit to quit): ").lower()
    print("----------\n")
    while(user_input != 'exit'):
        met.menu_main()
        user_input = input("Please choose one option: ").lower()
        print("----------")

        # 1. List all sellers
        if (user_input == '1'):
            mcursor.execute("SELECT seller_name FROM sellers")
            mresult = mcursor.fetchall()
            print("\nThe names of all the sellers:")

            # Printing names of sellers.
            for row in mresult:
                print(row[0])

            print("\n----------")
            user_input = input("\nPress any key to return to main menu "
                               "(and exit to quit): ")

        # 2. Search for available phone models at Noor Shop
        elif (user_input == '2'):
            query = """SELECT phone_brand, model_name, size_in 
                       FROM phones 
                       JOIN sellers 
                       WHERE sellers.seller_name = 'Noor Shop' 
                       AND phone_brand = sellers.available_brand;"""
            mcursor.execute(query)
            mresult = mcursor.fetchall()
            print("\nThe available phone models at Noor Shop:")

            # Printing out all available phones at Noor Shop
            for row in mresult:
                print("Brand: ", row[0])
                print("Model: ", row[1])
                print("Size (inch): ", row[2])
                print("\n")

            print("\n----------")
            user_input = input("\nPress any key to return to main menu "
                               "(and exit to quit): ")

        # 3. Search for shops that have Martin's fav brand.
        elif (user_input == '3'):
            query = """ SELECT phone_brand, model_name, seller_name
                        FROM phones
                        JOIN customers
                        JOIN sellers
                        ON customers.customer_id = 1
                        AND phones.phone_brand = customers.fav_brand
                        AND sellers.available_brand = phones.phone_brand;
                        """

            mcursor.execute(query)
            mresult = mcursor.fetchall()
            print("\nShops that have Martin's favorite phone brand:")

            for row in mresult:
                print("Seller: ", row[2])
                print("Brand: ", row[0])
                print("Model: ", row[1])
                print("\n")

            print("\n----------")
            user_input = input("\nPress any key to return to main menu "
                               "(and exit to quit): ")

        # 4. Lists all phone brands in the database and the number of models for each brand.
        elif (user_input == '4'):

            query = """ SELECT phone_brand, 
                        COUNT(phone_brand)
                        FROM phones
                        GROUP BY phone_brand
                        """
            mcursor.execute(query)
            mresult = mcursor.fetchall()
            print("\nAll brands and the number of models available:")

            for row in mresult:
                print("Brand: ", row[0])
                print("Num of models: ", row[1])

            print("\n----------")
            user_input = input("\nPress any key to return to main menu "
                               "(and exit to quit): ")

        # 5. Creats a VIEW that contains all customers that have apple as fav_brand.
        elif (user_input == '5'):

            query = """ CREATE VIEW customers_fav_brand
                        AS SELECT * FROM customers
                        WHERE fav_brand = 'Apple';
                        """
            try:
                mcursor.execute(query)
                print("\nView created!")
            except mysql.connector.Error as eror:
                if eror.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("\nThe view already exists.")
                else:
                    print(eror.msg)

            print("\n----------")
            user_input = input("\nPress any key to return to main menu "
                               "(and exit to quit): ")

        # 6. Prints out the view made in query 5, Name: and fav_brand.
        elif (user_input == '6'):
            query = """ SELECT *
                        FROM customers_fav_brand;
                    """

            mcursor.execute(query)
            mresult = mcursor.fetchall()
            print("\nAll customers with Apple as thier favorite brand:")

            for row in mresult:
                print("\nName: ", row[1] + " " + row[2])
                print("Favorite brand: ", row[4])

            print("\n----------")
            user_input = input("\nPress any key to return to main menu "
                               "(and exit to quit): ")

    print("\nProgram has ended successfully!"
          "\n----------")


main()
