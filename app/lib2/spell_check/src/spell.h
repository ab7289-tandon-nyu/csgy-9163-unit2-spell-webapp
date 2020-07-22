/****************************************************************************
* spell.h
*
* Application Security, Assignment 1
*
* Adapted from code written by Ben Halperin
* Implemented by Alex Biehl
***************************************************************************/

#ifndef spell_h
#define spell_h

#include <stdbool.h>
#include <stdio.h>

// maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

#define HASH_SIZE 2000

#define MAX_MISSPELLED 1000

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

typedef node *hashmap_t;

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
int check_words(FILE *fp, hashmap_t hashtable[], char *misspelled[]);

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
bool check_word(const char *word, hashmap_t hashtable[]);

/**
 * Loads dictionary into memory.  Returns true if successful else false.
 */
/**
 * Inputs:
 *  dictionary_file:    Path to the words file.
 *  hashtable:          The hash table to be populated.
 *
 * Returns:
 *  bool:       Whether or not the hashmap successfully populated.
 *
 * Modifies:
 *  hashtable: This hashmap should be filled with words from the file provided.
 *
 * Example:
 *  bool success = load_dictionary("wordlist.txt", hashtable);
 **/
bool load_dictionary(const char *dictionary_file, hashmap_t hashtable[]);

/**
 * Already implemented in dictionary.c
 **/
int hash_function(const char *word);

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
bool lower_case(char *l_word, const char *word);

/**
 * Returns an array of strings and a length
 * */
/**
 * Inputs:
 *  line:           the line to be split
 *  word_list:      the array to fill with the words
 *  len:            the length of the passed in array
 * 
 * Returns:
 *  int:            the number of words in the returned list
 * 
 * Modifies:
 *  word_list:      word_list should be filled with the split words
 **/
int split_line(const char *line, char **word_list, int len);

/**
 * Removes all the punctionation marks from a word'
 * */
/**
 * Inputs:
 *  word:           the word to have punctuation stripped
 *  dest:           the word to be filled in
 * 
 * Modifies:
 *  dest:           word less punctuation
 * */
void remove_punc(const char *word, char *dest);

/**
 * Convenience function to free the dictionary after we're all done
 * */
void free_dictionary(hashmap_t hashtable[]);

/**
 * Main run function for the spell checker
 **/
/**
 * Inputs
 * words:           path to the file of words to be spell checked
 * dictionary:      path to the dictionary file
 * 
 * Side Effects
 * prints out to the console the list of misspelled words, if any
 * 
 * Returns
 * int:             whether or not it ran successfully
 * */
int spell_check(const char *words, const char *dictionary);

/**
 * Check if a word is all digits
 * */
bool is_number(const char *word);

#endif /* dictionary_h */
