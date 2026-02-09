def main():
    while True:
        try:
            # Ask for the height of pyramid
            height = int(input("Height: "))

            # Keep asking for height if less than 2
            if height > 0 and height < 9:
                break
        # Exception if user gives non-integer value
        except ValueError:
            print("Please, provide an integer value")

    for row in range(height):
        # Build the spaces of the left side of the pyramid
        for spaces in range(height - row - 1):
            print(" ", end="")

        # Build the hashes of the left side of the pyramid
        for hash in range(row + 1):
            print("#", end="")

        # Add two spaces in between the sides of the pyramid
        print("  ", end="")

        # Build the hashes of the right side of the pyramid
        for hash in range(row + 1):
            print("#", end="")

        # Break line of each row
        print()


if __name__ == "__main__":
    main()
