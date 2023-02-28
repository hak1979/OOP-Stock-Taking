# A program that performs stock taking for a Nike warehouse using OOP.

##Important information before running the program

This program uses the match-case feature and it will only run on python 3.10 and above. Otherwise, theprogram will not run and you will see an error. Please update your python to the latest version.

The program also utilises the sqlite3 and tabulate libraries. These will have to be installed into your python environment before you run the program.

##The features of the program
The program allows the user to 
* item calculate the total stock value of each shoe model
* item change the shoe quantity once re-stocked
* item view all the shoes in the store
* item add new shoes to the database
* item put the shoe with the highest quantity on sale
* item search for a shoe by code
* item delete a shoe model by shoe code

## The database
On initial run of the program, it will create a folder called "data" if it doesn't exist
and within it it will create a database called shoes_db. 

The database stores the book data in the shoes table that includes the country, code (unique),
product, cost and quantity as qty. 

![Image of shoes table](/images/shoes_table.jpg)

## How to run the program
* item Clone or download the inventorysql.py file onto a local folder of your choice 
* item Start your python environment that includes tabulate and sqlite3
* item In the terminal navigate to the folder where you have stored inventorysql.py
* item Run the program by typing "python inventorysql.py" or "python3 inventorysql.py" depending on your setup
* item the program runs on the terminal, please follow the instructions onscreen. 

## How to use the program
When the program is run the user is presented with a menu as below.

![Image of shoes menu](/images/menu_items.jpg)


The user can select the option by entering the number only. No other inputs will be accepted.

### Menu 0: Exit
When this option is selected, the database will be closed and the program will exit.
### Menu 1:Value per item
Table of shoes with total values of each row displayed on screen. This shows the total stock value
of each shoe. 
### Menu 2: Option to re_stock shoes with lowest quantity
The shoe with the lowest quantity can be re-stocked by specifying the number of shoes to be added to
stock.
### Menu 3: View all
In this menu all the shoes are displaed on screen in a table.
### Menu 4: New shoe
The user enters the details of the new shoe to be entered into the database.
### Menu 5: Put on sale
The shoe with the highest quantity is put on sale. 
### Menu 6: Search
Allows the user to search for a shoe by code only.
### Menu 7: Delete
Allows the user to delete a shoe line by code only. 
