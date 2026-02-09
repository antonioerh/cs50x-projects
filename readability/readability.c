#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text
    float letters = count_letters(text);
    float words = count_words(text);
    float sentences = count_sentences(text);

    // Compute the Coleman-Liau index
    float L = (letters / words) * 100;
    float S = (sentences / words) * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = round(index);

    // Print the grade level
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{
    // Return the number of letters in text
    int letters = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        // Check if the index is in the alphabet
        if (isalpha(text[i]))
        {
            // Add one to the variable letters
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    // Return the number of words in text
    int words = 1;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        // Check if the index is a space
        if (isspace(text[i]))
        {
            // Add one to the variable words
            words++;
        }
    }
    return words;
}

int count_sentences(string text)
{
    // Return the number of sentences in text
    int sentences = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        // Check if the index is either one of the punctuation marks
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            // Add one to the variable sentences
            sentences++;
        }
    }
    return sentences;
}
