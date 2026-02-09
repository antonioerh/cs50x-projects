#include <cs50.h>
#include <stdio.h>

void print_row(int bricks);

int main(void)
{
    int height;

    do
    {
        height = get_int("Height: ");
    }
    while (height < 1);

    for (int row = 0; row < height; row++)
    {
        // Build the spaces of the left side of the pyramid
        for (int spaces = 0; spaces < height - row - 1; spaces++)
        {
            printf(" ");
        }
        // Build the hashes of the left side of the pyramid
        for (int hash = 0; hash <= row; hash++)
        {
            printf("#");
        }

        // Add the two spaces in between the sides of the pyramid
        printf("  ");

        // Build the hashes of the right side of the pyramid
        for (int hash = 0; hash <= row; hash++)
        {
            printf("#");
        }

        // Break line for each row
        printf("\n");
    }
}
