#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
} candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    // Iterate over each candidate
    for (int i = 0; i < candidate_count; i++)
    {
        // Compare candidates[i].name and name
        if (strcmp(candidates[i].name, name) == 0)
        {
            //
            preferences[voter][rank] = i;
            return true;
        }
    }
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    // Iterate over each voter
    for (int i = 0; i < voter_count; i++)
    {
        // Iterate over each candidate
        for (int j = 0; j < candidate_count; j++)
        {
            // Check if candidate is not eliminated
            if (!candidates[preferences[i][j]].eliminated)
            {
                // i voter add candidate to j rank
                candidates[preferences[i][j]].votes++;
                break;
            }
        }
    }
    return;
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    // Minimum of votes to win
    int threshold = voter_count / 2;

    // Iterate over each candidate
    for (int i = 0; i < candidate_count; i++)
    {
        // Check if candidate is not eliminated and has more votes than threshold
        if (!candidates[i].eliminated && (candidates[i].votes > threshold))
        {
            printf("%s\n", candidates[i].name);
            return true;
        }
    }
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    // Least voted candidate's votes
    int min = voter_count;

    // Iterate over all candidates
    for (int i = 0; i < candidate_count; i++)
    {
        // Ignore candidates who are already eliminated
        if (!candidates[i].eliminated)
        {
            // Track the lowest vote count among remaining candidates
            if (candidates[i].votes < min)
            {
                min = candidates[i].votes;
            }
        }
    }
    // Return that lowest value
    return min;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    // Iterate over all candidates
    for (int i = 0; i < candidate_count; i++)
    {
        // Ignore candidates who are already eliminated
        if (!candidates[i].eliminated)
        {
            // Check if any candidate has votes different from "min"
            if (candidates[i].votes != min)
            {
                // If yes, then not all are tied -> return false
                return false;
            }
        }
    }
    // If loop finishes, all remaining candidates are tied -> return true
    return true;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    // Iterate over all candidates
    for (int i = 0; i < candidate_count; i++)
    {
        // If candidate is not eliminated AND candidate's votes == min
        if (!candidates[i].eliminated && candidates[i].votes == min)
        {
            // Mark candidate as eliminated
            candidates[i].eliminated = true;
        }
    }
}
