/****************************************************************************
 * spell.c
 *
 * Application Security, Assignment 1
 *
 * Adapted from code written by Ben Halperin.
 * Implemented by Alex Biehl
 ***************************************************************************/

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "spell.h"

// Hash table is an array of linked lists.
node *hashtable[HASH_SIZE];

// Maps a word to an integer value to place it in the hash table.
// Sum the value of each character in the word, then find the
// remainder after dividing by the size of the hash table.
int hash_function(const char *word)
{
    int sum = 0;
    int word_length = strlen(word);

    for (int i = 0; i < word_length; i++)
    {
        sum += word[i];
    }

    int bucket = sum % HASH_SIZE;
    return bucket;
}

// given a dictionary file and a hashtable, load the dictionary file
// into the hastable
// if successfull returns true
// otherwise returns false
bool load_dictionary(const char *dictionary_file, hashmap_t hashtable[])
{

    // check if hashtable is null
    if (hashtable == NULL)
    {
        // hashtable was not initialized
        return false;
    }

    // initialize each of its values to NULL if it's valid
    for (int i = 0; i < HASH_SIZE; i++)
    {
        hashtable[i] = NULL;
    }

    // make sure we weren't handed an empty pointer
    if (dictionary_file == NULL)
    {
        printf("dictionary_file was null");
        return false;
    }

    FILE *fptr;
    char *line = NULL;
    size_t len = 0;
    ssize_t read;

    fptr = fopen(dictionary_file, "r");
    if (fptr == NULL)
    {
        printf("fptr was null");
        return false;
    }

    int iter = 0;
    while ((read = getline(&line, &len, fptr)) != -1)
    {
        // printf("read word %s\n", line);
        if (read <= LENGTH)
        {
            //printf("Iteration %d, creating node for: %s \n", ++iter, line);

            //hashmap_t new_node = (hashmap_t) malloc(sizeof(hashmap_t));
            // i don't know why this words vs the previous but it does
            hashmap_t new_node = malloc(sizeof(*new_node));
            new_node->next = NULL;
            strcpy(new_node->word, line);

            int len = strlen(new_node->word);
            for (int i = len - 1; i >= 0; --i)
            {
                if (new_node->word[i] == '\n')
                {
                    new_node->word[i] = 0;
                }
            }

            // printf("\tcopied word is: %s\n", new_node->word);
            int bucket = hash_function(new_node->word);

            if (hashtable[bucket] == NULL)
            {
                hashtable[bucket] = new_node;
            }
            else
            {
                new_node->next = hashtable[bucket];
                hashtable[bucket] = new_node;
            }
        }
        else
        {
            printf("word was too big %s", line);
        }
    }

    // free memory allocated by getline()
    free(line);
    line = NULL;
    // close file
    int result = fclose(fptr);
    if (result != 0)
    {
        printf("unable to close the file");
    }
    return true;
}

/**
 * Returns true if word is in dictionary else false.
 */
/**
 * Inputs:
 *  word:       A word to check the spelling of.
 *  hashtable:  The hash table used to determine spelling
 *
 * Returns:
 *  bool:       A boolean value indicating if the word was correctly spelled.
 *
 * Modifies:
 *
 * Example:
 *  bool correct  = check_word(word, hashtable);
 **/
bool check_word(const char *word, hashmap_t hashtable[])
{

    if (word == NULL || hashtable == NULL)
    {
        return false;
    }

    // make sure that the word isn't a number
    if (is_number(word))
    {
        return true;
    }

    int bucket = hash_function(word);
    hashmap_t cursor = hashtable[bucket];

    while (cursor != NULL)
    {
        if (strcmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    // set word to lowercase
    char l_word[LENGTH + 1];
    lower_case(l_word, word);

    bucket = hash_function(l_word);
    cursor = hashtable[bucket];

    while (cursor != NULL)
    {
        if (strcmp(l_word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

/**
 * Array misspelled is populated with words that are misspelled. Returns the length of misspelled.
 */
/**
 * Inputs:
 *  fp:         A file pointer to the document to check for spelling errors.
 *  hashtable:  The hash table used to determine spelling
 *  misspelled: An empty char* array to be populated with misspelled words.
 *              This array will never be greater than 1000 words long.
 *
 * Returns:
 *  int:        The number of words in the misspelled arary.
 *
 * Modifies:
 *  misspelled: This array will be filled with misspelled words.
 *
 * Example:
 *  int num_misspelled = check_words(text_file, hashtable, misspelled);
 **/
int check_words(FILE *fp, hashmap_t hashtable[], char *misspelled[])
{

    int num_misspelled = 0;
    char *line = NULL;
    size_t len = 0;

    if (fp == NULL)
    {
        printf("fp was null");
        return -1;
    }

    while ((getline(&line, &len, fp)) != -1)
    {
        // split line on spaces
        int length = 32;
        char *word_list[length];
        for (int i = 0; i < length; ++i)
        {
            word_list[i] = NULL;
        }
        int count = split_line(line, word_list, len);

        //for each word in line
        for (int i = 0; i < count; ++i)
        {
            int dest_len = strlen(word_list[i]) + 1;
            char dest[dest_len];
            for (int i = 0; i < dest_len; ++i)
            {
                dest[i] = NULL;
            }
            //remove punctuation
            remove_punc(word_list[i], dest);
            //if not check word
            if (!check_word(dest, hashtable) && num_misspelled < MAX_MISSPELLED)
            {
                //append to mispelled
                *misspelled++ = strdup(dest);
                // increment num_mispelled
                ++num_misspelled;
            }
        }
        // make sure to free the memory we alloc'd for word list
        for (int i = 0; i < length; ++i)
        {
            if (word_list[i] != NULL)
            {
                free(word_list[i]);
                word_list[i] = NULL;
            }
        }
    }

    // free memory allocated by getline()
    free(line);
    line = NULL;

    return num_misspelled;
}

/**
 * Returns a string as lower case
 * */
/**
 * Inputs:
 *  l_word:     the word to be populated
 *  word:       the word to be made lower_case
 * 
 * Returns:
 *  bool:      whether or not the word was made lower case
 * 
 * Modifies:
 *  l_word:      l_word should be filled by the word all lower case
 **/
bool lower_case(char *l_word, const char *word)
{

    if (l_word == NULL || word == NULL)
    {
        return false;
    }

    for (int i = 0; i < LENGTH; i++)
    {
        l_word[i] = NULL;
    }

    for (int i = 0; word[i]; ++i)
    {
        l_word[i] = (char)tolower(word[i]);
    }
    return true;
}

/**
 * Returns an array of strings and a length
 * */
/**
 * Inputs:
 *  line:           the line to be split
 *  word_list:      the array of size to fill with the words
 *  len:            the length of the passed in array
 * 
 * Returns:
 *  int:            the number of words in the returned list
 * 
 * Modifies:
 *  word_list:      word_list should be filled with the split words
 **/
int split_line(const char *line, char **word_list, int list_length)
{
    int word_size = 0;
    char delim[] = " ";

    int line_size = strlen(line);
    char temp_str[line_size];
    // want to copy to a temporary string since strtok modifies
    // the original
    strcpy(temp_str, line);

    // remove line breaks
    int temp_len = strlen(temp_str);
    for (int i = temp_len - 1; i >= 0; --i)
    {
        if (temp_str[i] == '\n')
        {
            temp_str[i] = 0;
        }
    }

    // get the pointer to the first token
    char *split_ptr = strtok(temp_str, delim);
    while (split_ptr != NULL && word_size < list_length)
    {
        // allocate space for the new word
        //*word_list = (char *) malloc(strlen(split_ptr) * sizeof(char*));
        // again, don't know why the below line works better than the previous but it does
        // the previous line led to writes that sometimes went beyond the end of the heap
        *word_list = malloc(strlen(split_ptr) * sizeof(*word_list));

        // copy it from the token
        strcpy(*word_list, split_ptr);

        split_ptr = strtok(NULL, delim);
        ++word_size;
        ++word_list; // increment the list ptr so next iteration we're looking at next index
    }

    return word_size;
}

// removes punctuation marks from a word
// assumes that the word is not an empty string
void remove_punc(const char *word, char *dest)
{
    char punc[] = {',', '!', '.', '?', ';', ':', '-', '{', '}', '[', ']', '(', ')', '\'', '"', NULL};

    for (; *word; ++word)
    {
        bool is_punc = true;
        for (int i = 0; punc[i]; ++i)
        {
            if (*word == punc[i])
            {
                is_punc = false;
                break;
            }
        }
        if (is_punc)
        {
            *dest++ = *word;
        }
    }
    *dest = 0;
}

void free_dictionary(hashmap_t hashtable[])
{
    for (int i = 0; i < HASH_SIZE; ++i)
    {
        if (hashtable[i] != NULL)
        {
            hashmap_t node = hashtable[i];
            while (node != NULL)
            {
                hashmap_t temp = node;
                node = node->next;
                free(temp);
                temp = NULL;
            }
        }
    }
}

// main driver for the library
int spell_check(const char *words, const char *dictionary)
{

    if (!words || !dictionary)
    {
        printf("Warning! Please specify 2 arguments!\n");
        return 1;
    }

    hashmap_t hashtable[HASH_SIZE];
    bool loaded = load_dictionary(dictionary, hashtable);
    if (!loaded)
    {
        printf("Warning! Unable to load the dictionary file!\n");
        return 1;
    }

    char *misspelled[MAX_MISSPELLED];
    for (int i = 0; i < MAX_MISSPELLED; ++i)
    {
        misspelled[i] = NULL;
    }

    FILE *fp = fopen(words, "r");
    if (!fp)
    {
        printf("Warning! Unable to open the word file!\n");
        return 1;
    }

    int num_misspelled = check_words(fp, hashtable, misspelled);
    if (num_misspelled > 0)
    {
        printf("The following %d words are misspelled!\n\n", num_misspelled);
        for (int i = 0; i < num_misspelled; ++i)
        {
            printf("%s \n", misspelled[i]);
        }
    }
    else
    {
        printf("All words are correctly spelled!\n");
    }

    fclose(fp);
    for (int i = 0; i < MAX_MISSPELLED; ++i)
    {
        if (misspelled[i] != NULL)
        {
            free(misspelled[i]);
            misspelled[i] = NULL;
        }
    }
    free_dictionary(hashtable);
    return 0;
}

bool is_number(const char *word)
{

    for (int i = 0; word[i] != '\0'; ++i)
    {
        if (isdigit(word[i]) == 0)
        {
            return false;
        }
    }
    return true;
}
