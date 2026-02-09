#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "rb");

    // Check if it opened correctly
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[BLOCK_SIZE];
    FILE *img = NULL;
    int count = 0;
    char filename[8];

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        // Compute requirements of a JPEG file's beggining
        bool is_header = buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
                         (buffer[3] & 0xf0) == 0xe0;

        // Check if the requirements are met
        if (is_header)
        {
            // Close previous image if open
            if (img != NULL)
            {
                fclose(img);
            }

            // Create JPEGs from the data
            sprintf(filename, "%03i.jpg", count++);
            img = fopen(filename, "wb");
            if (img == NULL)
            {
                fclose(card);
                return 1;
            }
        }

        // If currently writing a JPEG, write this block
        if (img != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }

    // Close any remaining open files
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(card);

    return 0;
}
