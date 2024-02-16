# This program is designed to calculate the optimal rent and number of units to rent out for a real estate office.
# The calculations are based on the following assumptions:
# - When the rent is $600 per month, all the units are occupied.
# - For each $40 increase in rent, one unit becomes vacant.
# - Each occupied unit requires $27 per month for maintenance.

# The goal is to find the rent that should be charged and the number of occupied units that will maximize profits.

# The program provides a menu for the user to adjust the parameters and calculate the maximum profit.

# Please refer to the textbook chapters 5-15 for the underlying principles and methods used in this program.

# Let's start by defining the default parameters.
# Author: Abraham Reines 

# Initial parameters
units = 50  # Total number of units
base_rent = 600  # Base rent that results in all units being occupied
rent_increase = 40  # Increase in rent that results in an additional unit becoming vacant
maintenance = 27  # Maintenance cost for each rented unit

# Function to calculate profit
def calculate_profit(units, rent, maintenance):
    revenue = units * rent
    costs = units * maintenance
    profit = revenue - costs
    return profit

# Function to find the rent that maximizes profit
def maximize_profit(units, base_rent, rent_increase, maintenance):
    max_profit = 0
    optimal_units = units
    optimal_rent = base_rent
    for i in range(units):
        rent = base_rent + i * rent_increase
        profit = calculate_profit(units - i, rent, maintenance)
        if profit > max_profit:
            max_profit = profit
            optimal_units = units - i
            optimal_rent = rent
    return optimal_units, optimal_rent, max_profit

# Test the function
optimal_units, optimal_rent, max_profit = maximize_profit(units, base_rent, rent_increase, maintenance)
print(f'Rent {optimal_units} units at ${optimal_rent} per month for a net profit of ${max_profit:.2f}')

# Interactive menu for user input (refer to Chapter 6 for fruitful functions)
def get_choice():
    print('Welcome to the apartment program! Current values are: Units={}, Base rent=${}, Rent increase=${}, Maintenance=${}'.format(units, base_rent, rent_increase, maintenance))
    print('1. Change the number of units')
    print('2. Change the base rent')
    print('3. Change the rent increase')
    print('4. Change the maintenance')
    print('5. Use current values to determine max profit')
    print('6. Exit the program')
    choice = int(input('Enter choice: '))
    return choice

def get_new_value(message):
    new_value = int(input(message))
    while new_value <= 0:
        print('Invalid input. Please enter a positive number.')
        new_value = int(input(message))
    return new_value

# Main function to run the program (refer to Chapter 6 for fruitful functions)
def main():
    global units, base_rent, rent_increase, maintenance
    while True:
        choice = get_choice()
        if choice == 1:
            units = get_new_value('Please enter the new number of units: ')
        elif choice == 2:
            base_rent = get_new_value('Please enter the new base rent: ')
        elif choice == 3:
            rent_increase = get_new_value('Please enter the new rent increase: ')
        elif choice == 4:
            maintenance = get_new_value('Please enter the new maintenance: ')
        elif choice == 5:
            optimal_units, optimal_rent, max_profit = maximize_profit(units, base_rent, rent_increase, maintenance)
            print(f'Rent {optimal_units} units at ${optimal_rent} per month for a net profit of ${max_profit:.2f}')
        elif choice == 6:
            break
        else:
            print('Invalid choice. Please enter a number between 1 and 6.')

# Run the program
main()