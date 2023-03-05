# import libraries


# *** Functions go here ***

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


# main routine goes here
get_int = num_check("How many do you need? ,"
                    "Please enter an amount moe than 0\n",
                    int)
get_cost = num_check("How much does it cose? $",
                     "Please enter a number more than 0\n",
                     float)

print("You need: {}".format(get_int))
print("It costs: ${}".format(get_cost))
 