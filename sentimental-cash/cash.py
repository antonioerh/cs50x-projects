def main():
    # Keep prompting until it satifies the algorithm
    while True:
        try:
            # Prompt the user for change owed, in cents
            dollars = float(input("Change owed: "))

            if dollars < 0:
                print("Please, enter a non-negative value")
                continue
            break

        except ValueError:
            print("Please, enter a digit")

    dollars_str = str(dollars)
    cents = 0

    # Check if dollars variable is less than 1
    if dollars_str[0:2] == "0.":
        dollars_str = dollars_str[2:]
        cents = int(dollars_str)
    # Check if dollars is more than or equal to 1
    elif dollars_str[0] in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        cents = dollars * 100
        cents = int(cents)

    # Calculate how many quarters you should give customer
    # Subtract the value of those quarters from cents
    quarters = calculate_quarters(cents)
    cents -= (quarters * 25)

    # Calculate how many dimes you should give customer
    # Subtract the value of those dimes from remaining cents
    dimes = calculate_dimes(cents)
    cents -= (dimes * 10)

    # Calculate how many nickels you should give customer
    # Subtract the value of those nickels from remaining cents
    nickels = calculate_nickels(cents)
    cents -= (nickels * 5)

    # Calculate how many pennies you should give customer
    # Subtract the value of those pennies from remaining cents
    pennies = calculate_pennies(cents)
    cents -= (pennies * 1)

    # Sum the number of quarters, dimes, nickels, and pennies used
    # Print that sum
    sum = quarters + dimes + nickels + pennies
    print(sum)


def calculate_quarters(cents):
    quarters = 0

    while cents >= 25:
        quarters += 1
        cents -= 25

    return quarters


def calculate_dimes(cents):
    dimes = 0

    while cents >= 10:
        dimes += 1
        cents -= 10

    return dimes


def calculate_nickels(cents):
    nickels = 0

    while cents >= 5:
        nickels += 1
        cents -= 5

    return nickels


def calculate_pennies(cents):
    pennies = 0

    while cents >= 1:
        pennies += 1
        cents -= 1

    return pennies


if __name__ == "__main__":
    main()
