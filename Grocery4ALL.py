from prettytable import PrettyTable
import argparse, time, datetime, string
"""
This program is made for the retail company “Grocery4ALL”. A new booking system that keeps track of their inventory, revenue, and costs regarding their business operations.
"""
#Initiation of Values that start with a value 0
revenue = costs = profits = totalValue = 0
"""
1st Section of the code is the functions section that are used for the program:
AddProduct is a function that adds the new product to the table through add_row function. The parameters it receives are the data input given by the user.
The number is 5 parameters as is the number of the columns of the table.
How it works: The myInventory table is updated with the new product data through add_row. Then the costs are recalculated.
And lastly the position of the new product in the table is tracked.
"""
def addProduct(id, name, quantity, purchase_price, selling_price):
    myInventory.add_row([id, name, quantity, purchase_price, selling_price])
    calculateCosts(float(purchase_price), int(quantity))
    positionOfIDs[name] =  len(positionOfIDs) # add to the dictionary the new product
    return myInventory
"""
The restockOrSellProduct is a function that deals with the restock and selling transactions.
The parameters it receives are the name of the product to be restocked or sold, the quantity that is sold or restocked and the choice values determines whether
we have a 'Restock a product' or 'Sell a product transactions. How it works: First line in 27 a search in the myInventory table happens that finds the specific data for the given product. Then id adds the new row with the quantity value, being updated.
Lastly, the transaction is tracked for History records.
"""
def restockOrSellProduct(name, quantity, choice):
    #Temporarily save row when given name is found so that it gets updated in the end of the function by the following logic, first get row that needs to be updated
    for row in myInventory:
        row.border = False
        row.header = False
        name2 = row.get_string(fields=["Name"]).strip()
        if name == name2:
            id = row.get_string(fields=["ID"]).strip()
            quantity2 = row.get_string(fields=["Quantity"]).strip()
            purchase_price = row.get_string(fields=["Purchasing price"]).strip()
            selling_price = row.get_string(fields=["Selling price"]).strip()
            break
    if choice == "r":
        myInventory.add_row([int(id), name, int(quantity) + int(quantity2), float(purchase_price), float(selling_price)]) #change my Inventory for restocking
        print("The product was updated successfully with the following new data:\n\nName:", name, "| Current Quantity:", quantity, " Thank you.")
        TrackLastTransaction = "Last transaction was 'Restock a product' on"
        current_time = datetime.datetime.now()
        calculateCosts(float(purchase_price), int(quantity))
        myInventory.del_row(positionOfIDs.get(name)) #clear old row
        restructureProductIDs(positionOfIDs.get(name))
        positionOfIDs[name] =  len(positionOfIDs) - 1
    else:
        if int(quantity2) < int(quantity):
            print("The transaction cannot be executed as the quantity given exceeds the inventory equal to", quantity2 ,". \nPlease retry by giving the correct selling quantity.")
        else:
            quant =  int(quantity2) - int(quantity)
            myInventory.add_row([int(id), name, quant, float(purchase_price), float(selling_price)]) #change my Inventory for selling the product
            print("The product was updated successfully with the following new data:\n\nName:", name, "| Current Quantity:", quantity)
            TrackLastTransaction = "Last transaction was 'Sell a product' on"
            current_time = datetime.datetime.now()
            calculateRevenue(float(selling_price), int(quantity))
            myInventory.del_row(positionOfIDs.get(name)) #clear old row
            restructureProductIDs(positionOfIDs.get(name))
            positionOfIDs[name] =  len(positionOfIDs) - 1
    time.sleep(3)
    return myInventory
#Reposition of products funtion depending on the new addition of the table in Lines 29, 40. Parameter index that shows the position of the product that is being updated
def restructureProductIDs(index):
    for x in positionOfIDs:
        if index < positionOfIDs.get(x):
            positionOfIDs[x] =  positionOfIDs[x] - 1 # UPDATE the positions to its product located after the product restocked or sold
#calculate the revenue function that gets as input the selling price of a product and the quantity and counts the revenue. Lastly adds the new revenue to the total revenue.
def calculateRevenue(s,q):
    global revenue
    s = s * q
    revenue = revenue + s
#calculateCosts function that gets as input the purchase price multiple the quantity of products. Parameters: n equals the price and q equals to quantity. Lastly, it adds to the total costs of the company the value.
def calculateCosts(n, q):
    global costs
    n = n * q
    costs = costs + n
#calculateProfit function that gets as input the total revenue and the total costs. Parameters: r equals the total revenue and c equals to total costs.
#Exception: For the case that the costs are more than the revenue the value given is 0 and not negative. Admin choice.
def calculateProfit(r, c):
    global profit
    if r > c:
        profit = abs(r-c)
    else:
        profit = 0
    return profit
#calculateTotalValue function takes specific IDs in a list and calculates their value by searching and adding their value to their total Value variable from the myInventory table. Parameters: listOfIDs list of Product IDs. It returns their total value.
def calculateTotalValue(listOfIDs):
    global totalValue
    for x in listOfIDs:
        for row in myInventory:
            row.border = False
            row.header = False
            id2 = row.get_string(fields=["ID"]).strip()
            if x == id2:
                quantity2 = row.get_string(fields=["Quantity"]).strip()
                selling_price = row.get_string(fields=["Selling price"]).strip()
                totalValue = totalValue + (int(quantity2)*float(selling_price))
                break
    return totalValue
#Check if parameter n is integer function
def is_integer(n):
    try:
        n = float(n)
        if n == int(n):
            return True
        else:
            return False
    except ValueError:
        # Handle the exception of a non numeric input
        return False
#Check if parameter n is float function for selling and purchasing prices
def is_float(f):
    try:
        n = float(f)
        return True
    except ValueError:
        # Handle the exception of a non numeric input
        return False
#2nd Section below the Grocery4All app funtions
# Creation of table of inventory of products, chose Pretty table for the user friendly experience through the cmd
myInventory = PrettyTable(["ID", "Name", "Quantity", "Purchasing price", "Selling price"])
# Adding 10 first data entry rows in the myInventory Table
myInventory.add_row([1, "Eggs", 10, 2, 3])
#Costs do occur whenever a transaction (add product, reorder product) is processed:
calculateCosts(2, 10)
myInventory.add_row([2, "Potatoes", 10, 3, 3.6])
calculateCosts(3, 10)
myInventory.add_row([3, "Apples", 10, 1, 2])
calculateCosts(1, 10)
myInventory.add_row([4, "Oranges", 10, 2, 2.5])
calculateCosts(2, 10)
myInventory.add_row([5, "Bananas", 20, 4, 6])
calculateCosts(4, 20)
myInventory.add_row([6, "BlueBerries", 10, 2, 3])
calculateCosts(2, 10)
myInventory.add_row([7, "Broccoli", 10, 2, 4])
calculateCosts(2, 10)
myInventory.add_row([8, "Honey", 10, 12, 20])
calculateCosts(12, 10)
myInventory.add_row([9, "CocconutOil", 10, 6, 10])
calculateCosts(6, 10)
myInventory.add_row([10, "Avocado", 10, 3, 5])
calculateCosts(3, 10)
#Variables to be used for the History Track of Last Transaction
TrackLastTransaction = "No transactions have been made yet."
id = 10
current_time = datetime.datetime.now()
#Track position of each product in the Pretty table for restocking and selling transactions cases
positionOfIDs = {"Eggs": 0, "Potatoes": 1, "Apples": 2, "Oranges": 3, "Bananas": 4, "BlueBerries": 5, "Broccoli": 6, "Honey": 7, "CocconutOil": 8,  "Avocado": 9}
print("\nWelcome to 'Grocery4ALL' app! \n")
while True:
    print("Below the current Inventory and the last transaction are shown:\n")
    myInventory.sortby = "ID"
    print(myInventory)
    beautify_datetime = ('%d.%d.%02d %02d:%02d'%(current_time.day, current_time.month, current_time.year, current_time.hour, current_time.minute))
    print("\nHistory Track:", TrackLastTransaction, "DateTime:", beautify_datetime)
    print("\nWhat to do next? Please choose the next action from the below options:\n\n1. Add a new product\n2. Restock a product\n3. Sell a product\n4. Make a calculation\n5. Exit\n\nPlease type a number between 1-5 options. Thank you.")
    user_choice = input("Enter your choice: ")
    if user_choice == "5":
        print("Exiting the application...")
        time.sleep(2)
        break
    elif user_choice == "4": # user_choice for calculations:
        print("\nPlease choose the calculation from the below options:\n\n1. The total revenue\n2. The total value of the inventory\n3. The total profit\n4. The total costs\n5. Exit\n\nPlease type a letter between 1-5 options. Thank you.")
        calculation = input("Enter your choice: ")
        if calculation == "1":
            print("The total revenue is:", revenue)
            time.sleep(2)
        elif calculation == "2":
            print("\nDo you want to be informed for the total value of specific IDs?\n\n1.YES\n2.NO")
            answer = input("Enter your choice: ")
            if answer == "2":
                products = myInventory.get_string(fields=["ID"])
                allIDs = [id.strip(string.punctuation) for id in products.split() if id.strip(string.punctuation).isalnum()]
                print("The total value of the Inventory is:", calculateTotalValue(allIDs))
                time.sleep(2)
            elif answer == "1":
                i = 0
                givenIDs = []
                products = myInventory.get_string(fields=["ID"])
                allIDs = [id.strip(string.punctuation) for id in products.split() if id.strip(string.punctuation).isalnum()]
                while True:
                    if i == 0:
                        inputID = input("Enter your choice: ")
                    else:
                        print("Do you want to add more IDs?\n1. YES 2.NO")
                        inputID = input("Enter your choice: ")
                        if inputID == "2":
                            break
                        elif inputID != "1" and inputID != "2":
                            time.sleep(1)
                            print("Invalid option.")
                            break
                        else:
                            inputID = input("Enter your choice: ")
                    if i == len(allIDs)-1:
                        print("The IDs provided reached the length of the inventory.")
                        break
                    if not inputID in allIDs:
                        print("The id given does not exist in the Inventory. Please enter a new id.\nOnly integers are accepted. Thank you.")
                        inputID = input("Enter your choice: ")
                    elif inputID == "ID":
                        print("The id given does not exist in the Inventory. Please enter a new id.\nOnly integers are accepted. Thank you.")
                        inputID = input("Enter your choice: ")
                    else:
                        givenIDs.append(inputID)
                    i = i + 1
                myset = set(givenIDs) # get only the unique IDs for the scenario of same IDs
                mynewlist = list(myset)
                mynewlist.sort() # sorted for optimization of code to lessen the iterations
                time.sleep(2)
                print("The total value of the Inventory with IDs", givenIDs," is:", calculateTotalValue(mynewlist))
                time.sleep(2)
            else:
                print("Invalid option. Taking you back in the start page.")
                time.sleep(2)
        elif calculation == "3":
            print("The total profit is:", calculateProfit(revenue, costs))
            time.sleep(2)
        elif calculation == "4":
            print("The total costs are:", costs)
            time.sleep(2)
        elif calculation == "5":
            print("Exiting the application...")
            time.sleep(2)
            break
        else:
            print("Invalid option.")
            time.sleep(2)
    elif user_choice == "3": # Sell a product transaction
        print("Please type which product was sold. Thank you.")
        name = input("Enter your choice: ")
        while True:
            products = myInventory.get_string(fields=["Name"])
            allNames = [word.strip(string.punctuation) for word in products.split() if word.strip(string.punctuation).isalnum()]
            if name in allNames: #Check if the sold product can be found in the current Inventory
                break
            else:
                print("Current Inventory:\n", products)
                print("The product given cannot be found in the Inventory. Please reenter the product.\nOnly characters are accepted. Thank you.")
                name = input("Enter your choice: ")
        print("Please type how much of the product was sold. Only integers are accepted. Thank you.")
        quantity = input("Enter your choice: ")
        while is_integer(quantity) == False:
            print("The quantity can only be an integer number. Please reenter. Thank you.")
            quantity = input("Enter your choice: ")
        restockOrSellProduct(name, quantity, "s")
    elif user_choice == "2": # Restock a product transaction
        print("Please type the Name of the product to be restocked. Thank you.")
        name = input("Enter your choice: ")
        while True:
            products = myInventory.get_string(fields=["Name"])
            allNames = [word.strip(string.punctuation) for word in products.split() if word.strip(string.punctuation).isalnum()]
            if name in allNames:
                break
            else:
                print("Current Inventory:\n", products)
                print("The product given cannot be found in the Inventory. Please reenter the product.\nOnly characters are accepted. Thank you.")
                name = input("Enter your choice: ")
        print("Please type how much of the product will be restocked. Only integers are accepted. Thank you.")
        quantity = input("Enter your choice: ")
        while is_integer(quantity) == False:
            print("The quantity can only be an integer number. Please reenter. Thank you.")
            quantity = input("Enter your choice: ")
        restockOrSellProduct(name, quantity, "r")
    elif user_choice == "1": # Add a new product transaction
        print("Please type the Name of the new product. Only characters are accepted. Thank you.")
        name = input("Enter your choice: ")
        while True:
            products = myInventory.get_string(fields=["Name"])
            allNames = [word.strip(string.punctuation) for word in products.split() if word.strip(string.punctuation).isalnum()] #Create a list
            if not name.isalpha(): #Check if the input is characters
                print("Only characters are accepted. Please reenter the name of the product. Thank you.")
                name = input("Enter your choice: ")
            elif name in allNames:
                print("The product given already exists in the Inventory. Please enter a new product.\nOnly characters are accepted. Thank you.")
                name = input("Enter your choice: ")
            else:
                break
        print("Enter the quantity of the new product.\nOnly integers numbers are accepted. Thank you.")
        quantity = input("Enter your choice: ")
        while is_integer(quantity) == False:
            print("The quantity can only be an integer number. Please reenter. Thank you.")
            quantity = input("Enter your choice: ")
        print("\nPlease enter the Purchase Price of the new product.\nOnly decimals are accepted. Thank you.\n")
        purchase_price = input("Enter your choice: ")
        while is_float(purchase_price) == False:
            print("The Purchase Price can only be a numeric value for example '25.5'. Please reenter. Thank you.")
            purchase_price = input("Enter your choice: ")
        print("\nPlease enter the Selling Price of the new product.\nOnly decimals are accepted. Thank you.")
        selling_price = input("Enter your choice: ")
        while is_float(selling_price) == False:
            print("The Selling Price can only be a numeric value for example '25.5'. Please reenter. Thank you.")
            selling_price = input("Enter your choice: ")
        id += 1
        addProduct(id, name, int(quantity), float(purchase_price), float(selling_price))
        print("The new product was added successfully with the following values:\n\nName:", name, "| Quantity:", quantity, "| Purchase Price:", purchase_price, "| Selling price:", selling_price)
        time.sleep(1)
        TrackLastTransaction = "Last transaction was 'Add a new product' on"
        current_time = datetime.datetime.now()
    else:
        time.sleep(1)
        print("Invalid option.")
    print('─' * 100) #beautification of the screen
    time.sleep(1) #help for the user to get informed in the necessary time to read
