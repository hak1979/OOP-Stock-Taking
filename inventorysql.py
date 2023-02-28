'''
A program that performs stock taking for a Nike warehouse using OOP.

!!!!IMPORTANT!!!!!
If you are not running python 3.10 or above the program will not run
as it uses match-case. Please update your python version to 3.10+.

'''

# import libraries
import os
import sqlite3
from tabulate import tabulate

# ========The beginning of the class==========


class Shoe:
    ''' A Shoe class with the country, code, product, cost and quantity attributes.
        The class has a get_cost and get_quantity methods to get the cost and
        quantity of the object respectively.'''

    def __init__(self, country, code, product, cost, quantity):
        '''Initialise the following attributes'''
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        ''' returns the cost of the shoe in this method.'''
        return int(self.cost)

    def get_quantity(self):
        ''' returns the quantity of the shoes. '''
        return int(self.quantity)

    def __str__(self):
        ''' returns a string representation of a class. '''
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


# =============Shoe list===========
# The list will be used to store a list of objects of shoes.
shoe_list = []

# the column names of the shoes table
shoes_column_names = ['Country', 'Code', 'Product', 'Cost', 'Qty']


# ==========Functions outside the class==============

def connect_database():
    ''' A function that connects to the shoes_db database and
        returbs the database'''

    # try to connect the the shoes_db database
    try:
        database = sqlite3.connect('data/shoes_db')

    # if the data folder doesn't exist an error will be raised
    # create a folder called data
    except sqlite3.OperationalError:
        os.mkdir('data')

    # connect/create the shoes_db database in path
    finally:
        database = sqlite3.connect('data/shoes_db')

    return database


def read_shoes_data():
    ''' This function willcreate a shoes object with the data from the shoes_db
    and append this object into the shoes list. One line in this file represents
    data to create one object of shoes.'''

    # select all items in the shoes table and stor ein items_list list
    items_list = cursor.execute(
        '''SELECT * FROM shoes'''
    ).fetchall()

    # the the shoes table is empty, print out message
    if items_list == []:
        print("No entries in database.")

    # if the shoes tbale is populated append shoes_list with the shoe object
    else:
        for item in items_list:
            shoe_list.append(
                Shoe(item[0], item[1], item[2], item[3], item[4]))


def capture_shoes():
    ''' This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.  '''

    # ask for the user to input the information for the new shoes
    print("Please enter the information for the new shoes")
    new_shoe_country = input("Please enter the country: ").strip()
    new_shoe_code = input("Please enter the product code: ").strip()
    new_shoe_product = input("Please enter the product name: ").strip()

    while True:
        try:
            new_shoe_cost = int(input("Please enter the shoe cost: ").strip())
            break
        except ValueError:
            print("You did not enter a number")

    while True:
        try:
            new_shoe_qunatity = int(
                input("Please enter the quantity in stock: ").strip())
            break
        except ValueError:
            print("You did not enter a number")

    # create a new_shoe shoe object and add to shoe_list
    new_shoe = Shoe(new_shoe_country, new_shoe_code,
                    new_shoe_product, new_shoe_cost, new_shoe_qunatity)

    shoe_list.append(new_shoe)

    # append the new shoe in the shoe table
    cursor.execute(
        '''INSERT INTO shoes VALUES (?,?,?,?,?)''', (new_shoe_country,
                                                     new_shoe_code, new_shoe_product,
                                                     new_shoe_cost, new_shoe_qunatity)
    )

    # print the details of the newly entered shoe on screen
    print("\nNew shoe entered.\n")
    print(tabulate([[shoe_list[-1].country, shoe_list[-1].code, shoe_list[-1].product,
                     shoe_list[-1].get_cost(), shoe_list[-1].get_quantity()]],
                   headers=shoes_column_names, tablefmt="fancy_grid"))

    db.commit()


def view_all():
    ''' This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module. '''

    print(tabulate([[shoe.country, shoe.code, shoe.product, shoe.cost,
                     shoe.quantity] for shoe in shoe_list],
                   headers=shoes_column_names, tablefmt="fancy_grid"))


def re_stock():
    '''This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe. '''

    # set the lowest quantity as the quantity of the first item initially
    lowest_quantity = shoe_list[0].get_quantity()

    # compare all shoes and if any other shoe has a lower_quantity, set this as
    # lowest quantity and set the shoe as the shoe to be re-stoked.
    for shoe in shoe_list:
        if shoe.get_quantity() < lowest_quantity:
            lowest_quantity = shoe.get_quantity()
            restock_shoe = shoe

    # print the information of shoe with lowest stock on screen
    print(f"\nThere are {restock_shoe.get_quantity()} of {restock_shoe.product} shoes "
          "and needs to be re-stocked.")

    # ask user to input how many of the shoes they would like to add
    while True:
        try:
            restock_quantity = int(
                input("\nPlease enter how many more you would like "
                      "to add to stock or -1 for main menu: "))

            if restock_quantity == -1:
                return None

            if restock_quantity > 0:
                break
            else:
                print("\nYou need to enter a positive number.")
        except ValueError:
            print("\nYou did not enter a number.")

    # update the quantity attribute by adding inputted quantity to already available
    restock_shoe.quantity = restock_shoe.get_quantity() + restock_quantity

    # update the shoes table with the restoked quantity value
    cursor.execute(
        '''UPDATE shoes SET Qty=? WHERE Code=?''', (
            restock_shoe.quantity, restock_shoe.code)
    )

    db.commit()

    # call the read_shoes_data function to repopulate shoe_list
    read_shoes_data()

    # print the new quantity of the shoes
    print(
        f"\nNow there are {restock_shoe.get_quantity()} of {restock_shoe.product} shoes.")


def search_shoe():
    ''' This function will search for a shoe from the list using the
        shoe code and return this object so that it will be printed.'''

    while True:
        # ask user to enter the item code
        search_code = input("\nPlease enter the product code to search for it"
                            " or -1 to exit to main menu: ").strip()

        # if -1 entered, it will go back to main menu and return None
        if search_code == "-1":
            print("\nGoing back to the main menu.")
            return None

        # if the shoe is in the shoe_list it will return the shoe.
        for shoe in shoe_list:
            if shoe.code == search_code:
                print(f"\nProduct with product code {search_code} found.\n")
                return shoe

        print(f"\nNo product with product code {search_code} found.")


def value_per_item():
    ''' This function will calculate the total value for each item.
         Please keep the formula for value in mind: value = cost * quantity.
         Print this information on the console for all the shoes.'''

    # store column titles locallay since we are changing it
    table = shoes_column_names

    # add "value" to the column titles
    table.append("Value")

    # print the table including the values column on screen
    print(tabulate([[shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity,
                    shoe.get_cost() * shoe.get_quantity()] for shoe in shoe_list],
                   headers=table, tablefmt="fancy_grid"))


def highest_qty():
    ''' function to determine the product with the highest quantity and
    print this shoe as being for sale.'''

    # set highest quantity as the quantity of the first item
    highest_quantity = shoe_list[0].get_quantity()

    # The shoe with the highest quantity will be the one to go on sale
    for shoe in shoe_list:
        if shoe.get_quantity() >= highest_quantity:
            highest_quantity = shoe.get_quantity()
            sale_item = shoe.product

    print(f"\n{sale_item} is on sale!")


def delete_shoe():
    ''' A function that deletes a shoe by code'''

    while True:
        shoe_to_delete = input("\nPlease enter the code of the shoe to delete:"
                               " or -1 to exit to main menu: ").strip()

        # if -1 entered, it will go back to main menu and return None
        if shoe_to_delete == "-1":
            print("\nGoing back to the main menu.")
            return None

        # if the shoe is in the shoe_list it will return the shoe.
        for index, shoe in enumerate(shoe_list, start=0):
            if shoe.code == shoe_to_delete:
                cursor.execute(
                    '''DELETE FROM shoes WHERE code=?''', (shoe_to_delete,)
                )
                db.commit()
                shoe_list.pop(index)
                print(
                    f"\nProduct with product code {shoe_to_delete} deleted.\n")
                return None

        print(f"\nNo product with product code {shoe_to_delete} found.")


# ==========Main Menu=============

# this is the string to display the options for the user
options_string = "\nPlease select from one of the options:"
options_string += "\n0 - to quit"
options_string += "\n1 - to show the value of shoe stock "
options_string += "\n2 - to re-stock shoe with lowest quantity"
options_string += "\n3 - to view the whole shoe stock "
options_string += "\n4 - to enter the information for a new shoe range"
options_string += "\n5 - to show the shoe to put on sale"
options_string += "\n6 - to search for a shoe by code"
options_string += "\n7 - to delete a shoe by code"

# populate the shoe_list by calling the read_shoes_data function
# after connecting to the shoes_db database and setting the cursor
db = connect_database()
cursor = db.cursor()
read_shoes_data()

# the user will be asked to make choice from the options given
while True:
    print(options_string)
    user_choice = input("\nPlease enter your choice: ").strip()

    match(user_choice):

        # the progmram will quit
        case '0':
            # close the database when exiting
            db.close()
            print("\nThe program will now temrinate. Goodbye!\n")
            break

        # table of shoes with total values of each column
        case '1':
            value_per_item()

        # option to re_stock shoes with lowest quantity
        case '2':
            re_stock()

        # to view th table of all shoes' details
        case '3':
            view_all()

        # to ask the user to enter a new shoe
        case '4':
            capture_shoes()

        # this will display the shoe with the highest quantity, and
        # to be put on sale
        case '5':
            highest_qty()

        # the user can search for a shoe by code
        case '6':
            # search_shoe returns a shoe object
            searched_shoe = search_shoe()

            # print the found shoe using tabulate to look tidy only if shoe found
            if searched_shoe is not None:
                print(tabulate([[searched_shoe.country, searched_shoe.code,
                                 searched_shoe.product, searched_shoe.cost,
                                 searched_shoe.quantity, ]],
                               headers=shoes_column_names, tablefmt="fancy_grid"))

        # To delete a shoe by code
        case '7':
            delete_shoe()

        # this is the defualt case, if no valid user_choice it displays an error
        case _:
            print("\nwrong input, try again!")
