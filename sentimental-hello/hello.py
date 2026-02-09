def main():
    # Ask for name
    name = input("What is your name? ")

    # If name not blank
    if len(name) > 1:
        print(f"hello, {name}")


if __name__ == "__main__":
    main()
