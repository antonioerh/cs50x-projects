import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py <database.csv> <sequence.txt>")
        sys.exit()

    # Read database file into a variable
    database = []

    try:
        with open(sys.argv[1]) as file:
            reader = csv.DictReader(file)

            header = reader.fieldnames

            strs = [h for h in header if h != "name"]

            for row in reader:
                database.append(row)
    except FileNotFoundError:
        print("Database file not found")
        sys.exit()

    # Read DNA sequence file into a variable
    try:
        with open(sys.argv[2]) as file:
            sequence = file.read()
    except FileNotFoundError:
        print("Sequence file not found")
        sys.exit()

    # Find longest match of each STR in DNA sequence
    counts = {}

    for s in strs:
        counts[s] = longest_match(sequence, s)

    # Check database for matching profiles
    found = False

    for person in database:
        if all(int(person[s]) == counts[s] for s in strs):
            print(person["name"])
            found = True
            break
        else:
            continue

    if found == False:
        print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


if __name__ == "__main__":
    main()
