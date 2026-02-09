def main():
    # Prompt the user for some text
    text = input("Text: ")

    # Count the number of letters, words, and sentences in the text
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Compute the Coleman-Liau index
    L = (letters / words) * 100
    S = (sentences / words) * 100

    index = 0.0588 * L - 0.296 * S - 15.8

    # Print the grade level
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index:.0f}")


def count_letters(text):
    letters = 0

    # Loop through each index of the string
    for i in text:
        # Check if the index is in the alphabet
        if i.isalpha():
            # Add one to the variable letters
            letters += 1

    # Return the number of letters in text
    return letters


def count_words(text):
    words = 1

    # Loop through each index of the string
    for i in text:
        # Check if the index is a space
        if i.isspace():
            # Add one to the variable words
            words += 1

    # Return the number of words in text
    return words


def count_sentences(text):
    sentences = 0

    # Loop through each index of the string
    for i in text:
        # Check if the index is a punctuation
        if i in [".", "!", "?"]:
            # Add one to the variable sentences
            sentences += 1

    # Return the number of sentences in text
    return sentences


if __name__ == "__main__":
    main()
