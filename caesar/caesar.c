#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digits(string key);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Make sure every character in argv[1] is a digit
    if (!only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Convert argv[1] from a `string` to an `int`
    int k = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext: ");

    // Print "ciphertext: " for later
    printf("ciphertext: ");

    // For each character in the plaintext:
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        // Rotate the character if it's a letter
        char c = rotate(plaintext[i], k);
        // Print each encrypted character of plaintext
        printf("%c", c);
    }
    // Break line
    printf("\n");
}

bool only_digits(string key)
{
    // For each character in key
    for (int i = 0; key[i] != '\0'; i++)
    {
        // Check if it is not a digit
        if (!isdigit(key[i]))
        {
            return false;
        }
    }
    // Return true if the if statement doesn't run
    return true;
}

char rotate(char p, int n)
{
    // If character is uppercase
    if (isupper(p))
    {
        return ((p - 'A' + n) % 26) + 'A';
    }
    // If character is lowercase
    else if (islower(p))
    {
        return ((p - 'a' + n) % 26) + 'a';
    }
    // If character is not in the alphabet
    else
    {
        return p;
    }
}
