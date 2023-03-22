# import libraries
import pandas
import math


# *** functions go here ***

# checks that input is either a float or an
# integer that is more than zero. Takes in custom error messages
def num_check(question, error, num_type):
    valid = False

    while not valid:

        try:
            response = num_type(input(question))

            if response <= 0:
                print(error)
            else:
                return response

        except ValueError:
            print(error)


# Checks that user has entered yes / no to a question
def yes_no(question):
    to_check = ["yes", "no"]

    valid = False
    while not valid:

        response = input(question).lower()

        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item

        print("Please enter either yes or no...\n")


# displays instructions
def show_instructions():
    print('''\n
***** Instructions *****

This program will ask you for...
- The name of the product you are selling
- How many items you plan on selling
- The costs for each component of the product
- How much money you want to make

It will then output an itemised list of the costs
with subtotals for the variable and fixed costs.
Finally it will tell you how much you should sell
each item for to reach your profit goal.

This data will also be written to a text file which has the same name as your product.

**** Program launched! ****''')
    print()


# Checks that user string response is not blank
def not_blank(question, error):
    valid = False
    while not valid:
        response = input(question)

        if response == "":
            print("{}.  \nPlease try again. \n".format(error))
            continue

        return response


# currency formatting function
def currency(x):
    return "${:.2f}".format(x)


# Gets expenses, returns list which has
# the data frame and sub-total
def get_expenses(var_fixed):
    # Set up dictionaries and lists

    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    # loop to get component, quantity and price
    item_name = ""
    while item_name.lower() != "xxx":

        print()
        # get name, quantity and item
        item_name = not_blank("Item name: ",
                              "The component can't be "
                              "blank.")
        if item_name.lower() == "xxx":
            break

        if var_fixed == "variable":
            quantity = num_check("Quantity: ",
                                 "The amount must be a whole number",
                                 int)
        else:
            quantity = 1

        price = num_check("How much for a single item? $",
                          "The price must be a number <more "
                          "tha 0>",
                          float)

        # add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']

    # Find sub-total
    sub_total = expense_frame['Cost'].sum()

    # Currency Formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]


# Prints expense frames
def expense_print(heading, frame, sub_total):
    print()
    print("**** {} Costs ****".format(heading))
    print(frame)
    print()
    print("{} Costs: ${:.2f}".format(heading, sub_total))
    return ""


# work out profit goal and total sales required
def profit_goal(total_costs):
    # Initialise variables and error message
    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:

        # ask for a profit goal...
        response = input("What is your profit goal (eg $500 or 50%) ")

        # check if first character is $...
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount (everything before the %)
            amount = response[:-1]

        else:
            # set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # Check amount is a number more than zero...
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no("Do you mean ${:.2f}. "
                                 "ie {:.2f} dollars? "
                                 "(y / n) ".format(amount, amount))

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no("Do you mean {}%? "
                                  "(y / n) ".format(amount))
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


# rounding function
def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to


# *** Main Routine goes here ***
# get product name
print("Welcome to the great Fund Raising Calculator")
print()
want_instructions = yes_no("Would you like to read the instructions? ")
if want_instructions == "yes":
    show_instructions()

product_name = not_blank("Product name: ",
                         "The product name can't be blank")

how_many = num_check("How many items will you be producing? ",
                     "The number of items must be a whole "
                     "number more than zero", int)

print()
print("Please enter your variables costs below...")
# Get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

have_fixed = yes_no("Do you have fixed costs? ")
# get fixed costs
if have_fixed == "yes":

    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]

else:
    fixed_frame = ""
    fixed_sub = 0


# work out total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculates total sales needed to reach goal
sales_needed = all_costs + profit_target

# Ask user for rounding
round_to = num_check("Round to nearest...? $",
                     "Can't be 0", int)

# Calculate recommended price
selling_price = sales_needed / how_many
print("Selling Price (unrounded): ${:.2f}".format(selling_price))

recommended_price = round_up(selling_price, round_to)
print("Recommended Price: ${:.2f}".format(recommended_price))

# change frames to strings (and generate additional strings as needed)
variable_txt = pandas.DataFrame.to_string(variable_frame)
if have_fixed == "yes":
    fixed_txt = pandas.DataFrame.to_string(fixed_frame)
else:
    fixed_txt = ""

# list holding stuff to print / write to file
to_write = [product_name, variable_txt, fixed_txt,
            profit_target, selling_price,
            recommended_price]


# *** Printing Area ***

print()
print("**** Fund Raising - {} ****".format(product_name))
expense_print("Variable", variable_frame, variable_sub)

if have_fixed == "yes":
    expense_print("Fixed", fixed_frame[['Cost']], fixed_sub)

print()
print("**** Total Costs: ${:.2f} ****".format(all_costs))
print()

print("**** Profit & Sales Targets ****")
print("Profit Target: ${:.2f}".format(profit_target))
print("Total Sales: ${:.2f}".format(all_costs + profit_target))

print()
print("**** Pricing ****")
print("Minimum Price: ${:.2f}".format(selling_price))
print("Recommended Price: ${:.2f}".format(recommended_price))

for item in to_write:
    print(item)
    print()

# Write to file...
# create file to hold data (add .txt extension)
file_name = "{}.txt".format(product_name)
text_file = open(file_name, "w+")

# heading
for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")

# close file
text_file.close()


