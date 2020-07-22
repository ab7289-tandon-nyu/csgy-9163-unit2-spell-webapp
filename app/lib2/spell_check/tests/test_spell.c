//
//  test_spell.c
//  csgy-9163-unit1-spell
//
//  Created by Alex Biehl on 5/30/20.
//  Copyright © 2020 Alex Biehl. All rights reserved.
//
#include <config.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <check.h>
#include "../src/spell.h"

#define DICTIONARY "../res/wordlist.txt"
#define TESTDICT "../res/test_wordlist.txt"
#define TESTWORDS "../res/test1.txt"

// TODO add tests

bool check_bucket(hashmap_t hashtable[], char *test_val);

// start dictionary load test cases
START_TEST(test_dictionary_normal)
{
    hashmap_t hashtable[HASH_SIZE];
    ck_assert(load_dictionary(TESTDICT, hashtable));
    // check buckets

    char *test_val = "first";
    ck_assert(check_bucket(hashtable, test_val));

    test_val = "second";
    // hash = hash_function(test_val);
    ck_assert(check_bucket(hashtable, test_val));

    test_val = "third";
    //hash = hash_function(test_val);
    ck_assert(check_bucket(hashtable, test_val));

    test_val = "test";
    //hash = hash_function(test_val);
    ck_assert(check_bucket(hashtable, test_val));

    free_dictionary(hashtable);
}
END_TEST

START_TEST(test_dictionary_one_bucket)
{

    hashmap_t hashtable[HASH_SIZE];
    ck_assert(load_dictionary("../res/one_bucket.txt", hashtable));

    char *test_vals[] = {
        "Justice",
        "lasagna",
        "creased",
        "Corinth",
        "Grumman",
        "gribble",
        NULL};

    for (int i = 0; test_vals[i]; ++i)
    {
        int hash = hash_function(test_vals[i]);
        printf("%s hash %d \n", test_vals[i], hash);
        // ck_assert(check_bucket(hashtable[hash], test_vals[i]));
        ck_assert(check_bucket(hashtable, test_vals[i]));
        ck_assert(check_word(test_vals[i], hashtable));
    }

    free_dictionary(hashtable);
}
END_TEST

START_TEST(test_dictionary_bad_hashtable)
{

    hashmap_t hashtable = NULL;
    ck_assert(!load_dictionary(TESTDICT, hashtable));
}
END_TEST

START_TEST(test_dictionary_null_hashtable)
{

    ck_assert(!load_dictionary(TESTDICT, NULL));
}
END_TEST

START_TEST(test_dictionary_empty_filename)
{

    hashmap_t hashtable[HASH_SIZE];
    ck_assert(!load_dictionary("bad_file.txt", hashtable));

    free_dictionary(hashtable);
}
END_TEST
// end dictionary load test cases

//start check_word test cases
START_TEST(test_check_word_empty_word)
{

    hashmap_t hashtable[HASH_SIZE];
    load_dictionary(TESTDICT, hashtable);
    const char *null_word = NULL;
    ck_assert(!check_word(null_word, hashtable));

    free_dictionary(hashtable);
}
END_TEST

START_TEST(test_check_word_empty_table)
{

    hashmap_t hashtable[HASH_SIZE];
    load_dictionary(TESTDICT, hashtable);
    const char *word = "first";
    ck_assert(!check_word(word, NULL));

    free_dictionary(hashtable);
}
END_TEST

START_TEST(test_check_word)
{

    hashmap_t hashtable[HASH_SIZE];
    load_dictionary(TESTDICT, hashtable);

    const char *w = "first";
    ck_assert(check_word(w, hashtable));

    const char *word = "FIRST";
    ck_assert(check_word(word, hashtable));

    const char *word1 = "sEconD";
    ck_assert(check_word(word1, hashtable));

    const char *word_invalid = "nOt HeRe";
    ck_assert(!check_word(word_invalid, hashtable));

    free_dictionary(hashtable);
}
END_TEST

START_TEST(test_check_word_normal)
{

    hashmap_t hashtable[HASH_SIZE];
    load_dictionary(DICTIONARY, hashtable);
    const char *correct_word = "Justice";
    const char *punctuation_word_2 = "pl.ace";
    ck_assert(check_word(correct_word, hashtable));
    ck_assert(!check_word(punctuation_word_2, hashtable));
    // Test here: What if a word begins and ends with "?

    const char *question_word = "?question?";
    ck_assert(!check_word(question_word, hashtable));

    free_dictionary(hashtable);
}
END_TEST

START_TEST(test_check_word_num)
{
    hashmap_t hashtable[HASH_SIZE];
    load_dictionary(DICTIONARY, hashtable);
    const char *word = "1234";
    ck_assert(check_word(word, hashtable));

    free_dictionary(hashtable);
}
END_TEST

START_TEST(test_check_word_num_invalid)
{
    hashmap_t hashtable[HASH_SIZE];
    load_dictionary(DICTIONARY, hashtable);
    const char *word = "12abc34";
    ck_assert(!check_word(word, hashtable));

    free_dictionary(hashtable);
}
END_TEST

//end check word_test cases

// start check_words test case

START_TEST(test_check_words_normal)
{

    hashmap_t hashtable[HASH_SIZE];
    load_dictionary(DICTIONARY, hashtable);
    char *expected[3];
    expected[0] = "sogn";
    expected[1] = "skyn";
    expected[2] = "betta";
    char *misspelled[MAX_MISSPELLED];
    for (int i = 0; i < MAX_MISSPELLED; ++i)
    {
        misspelled[i] = NULL;
    }
    FILE *fp = fopen(TESTWORDS, "r");
    int num_misspelled = check_words(fp, hashtable, misspelled);
    ck_assert(num_misspelled == 3);
    bool test = strlen(misspelled[0]) == strlen(expected[0]);
    int len1 = strlen(misspelled[0]);
    int len2 = strlen(expected[0]);
    ck_assert_msg(test, "%d!=%d", len1, len2);
    ck_assert_msg(strcmp(misspelled[0], expected[0]) == 0);
    ck_assert_msg(strcmp(misspelled[1], expected[1]) == 0);
    ck_assert_msg(strcmp(misspelled[2], expected[2]) == 0);

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
}
END_TEST

// end check_words test case

// start lower_case test cases

START_TEST(test_lower_null_l_word)
{

    char *word = "WORD";
    ck_assert(!lower_case(NULL, word));
}
END_TEST

START_TEST(test_lower_null_word)
{

    char l_word[LENGTH];
    ck_assert(!lower_case(l_word, NULL));
}
END_TEST

START_TEST(test_lower_word)
{

    char l_word[LENGTH + 1];
    char *word = "WORD";
    ck_assert(lower_case(l_word, word));
    ck_assert(strcmp(l_word, "word") == 0);
}
END_TEST

// end lower_case test cases

// start split_line test cases

START_TEST(test_split_line_empty)
{

    char *line = "";
    int len = 32;
    char *word_list[len];
    for (int i = 0; i < len; ++i)
    {
        word_list[i] = NULL;
    }
    int count = split_line(line, word_list, len);
    bool count_correct = count == 0;

    ck_assert(count_correct);
    // make sure to free the memory we alloc'd for word list
    for (int i = 0; i < len; ++i)
    {
        if (word_list[i] != NULL)
        {
            free(word_list[i]);
            word_list[i] = NULL;
        }
    }
}
END_TEST

START_TEST(test_split_line_single)
{

    char *line = "hello";
    int len = 32;
    char *word_list[len];
    for (int i = 0; i < len; ++i)
    {
        word_list[i] = NULL;
    }
    int count = split_line(line, word_list, len);

    bool count_correct = count == 1;
    bool word_correct = (strcmp(*word_list, "hello") == 0);

    for (int i = 0; i < count; ++i)
    {
        free(word_list[i]);
        word_list[i] = NULL;
    }

    ck_assert(count_correct);
    ck_assert(word_correct);
}
END_TEST

START_TEST(test_split_line_multiple)
{

    char *line = "hello world";
    int len = 32;
    char *word_list[len];
    for (int i = 0; i < len; ++i)
    {
        word_list[i] = NULL;
    }
    int count = split_line(line, word_list, len);
    bool count_correct = count == 2;

    char *answers[] = {"hello", "world"};
    bool word_correct = true;
    for (int i = 0; i < count; i++)
    {
        //printf("Word %d is: %s \n", i, word_list[i]);
        if (strcmp(word_list[i], answers[i]) != 0)
        {
            word_correct = false;
            break;
        }
    }

    for (int i = 0; i < count; ++i)
    {
        free(word_list[i]);
        word_list[i] = NULL;
    }

    ck_assert(count_correct);
    ck_assert(word_correct);
}
END_TEST

START_TEST(test_split_line_multi_spaces)
{

    char *line = " hello  world   mate ";
    int len = 32;
    char *word_list[len];
    for (int i = 0; i < len; ++i)
    {
        word_list[i] = NULL;
    }
    int count = split_line(line, word_list, len);
    bool count_correct = count == 3;

    char *answers[] = {"hello", "world", "mate"};
    bool word_correct = true;
    for (int i = 0; i < count; ++i)
    {
        //printf("Word %d is: %s \n", i, word_list[i]);
        if (strcmp(word_list[i], answers[i]) != 0)
        {
            word_correct = false;
            break;
        }
    }

    for (int i = 0; i < count; ++i)
    {
        free(word_list[i]);
        word_list[i] = NULL;
    }

    ck_assert(count_correct);
    ck_assert(word_correct);
}
END_TEST

// end split_line test cases

// start remove_punc tests

START_TEST(test_remove_punc_one)
{

    char *word = "...wo!!r?d..";
    char dest[strlen(word)];
    remove_punc(word, dest);
    ck_assert(strcmp(dest, "word") == 0);
}
END_TEST

START_TEST(test_remove_punc_two)
{

    char *word = "{w}()o{?}r!!d";
    char dest[strlen(word)];
    remove_punc(word, dest);
    ck_assert(strcmp(dest, "word") == 0);
}
END_TEST

// end remove_punc tests

// start spell_check tests

START_TEST(test_spell_check_null_wordlist)
{
    char *words = NULL;
    char *dictionary = TESTDICT;
    ck_assert(spell_check(words, dictionary) == 1);
}
END_TEST

START_TEST(test_spell_check_null_dictionary)
{
    char *words = TESTWORDS;
    char *dictionary = NULL;
    ck_assert(spell_check(words, dictionary) == 1);
}
END_TEST

START_TEST(test_spell_check_fn_null_inputs)
{
    char *words = NULL;
    char *dictionary = NULL;
    ck_assert(spell_check(words, dictionary) == 1);
}
END_TEST

START_TEST(test_spell_check_invalid_word_list)
{
    char *words = "invalid.txt";
    char *dictionary = TESTDICT;
    ck_assert(spell_check(words, dictionary) == 1);
}
END_TEST

START_TEST(test_spell_check_invalid_dictionary)
{
    char *words = TESTWORDS;
    char *dictionary = "invalid_dict.txt";
    ck_assert(spell_check(words, dictionary) == 1);
}
END_TEST

START_TEST(test_spell_check_invalid_inputs)
{
    char *words = "invalid.txt";
    char *dictionary = "invalid_dict.txt";
    ck_assert(spell_check(words, dictionary) == 1);
}
END_TEST

START_TEST(test_spell_check_valid)
{
    char *words = TESTWORDS;
    char *dictionary = DICTIONARY;
    ck_assert(spell_check(words, dictionary) == 0);
}
END_TEST
// end spell_check tests

// start is_number tests

START_TEST(test_is_num_valid)
{

    char *word = '1111';
    ck_assert(is_number(&word));
}
END_TEST

START_TEST(test_is_num_invalid)
{
    char *word = '1a11';
    ck_assert(!is_number(&word));
}
END_TEST

// end is_number tests

Suite *check_dictionary_suite(void)
{
    Suite *suite;
    TCase *check_dictionary_case;
    TCase *check_dictionary_input_case;
    TCase *check_word_case;
    TCase *check_words_case;
    TCase *check_lower_case;
    TCase *check_split_line_case;
    TCase *check_remove_punc_case;
    TCase *check_spell_check_case;
    TCase *check_is_num_case;

    suite = suite_create("check_dictionary");

    check_dictionary_case = tcase_create("Core");
    tcase_add_test(check_dictionary_case, test_dictionary_normal);
    suite_add_tcase(suite, check_dictionary_case);

    check_dictionary_input_case = tcase_create("Inputs");
    tcase_add_test(check_dictionary_input_case, test_dictionary_bad_hashtable);
    tcase_add_test(check_dictionary_input_case, test_dictionary_empty_filename);
    tcase_add_test(check_dictionary_input_case, test_dictionary_null_hashtable);
    tcase_add_test(check_dictionary_input_case, test_dictionary_one_bucket);
    suite_add_tcase(suite, check_dictionary_input_case);

    check_word_case = tcase_create("Check Word");
    tcase_add_test(check_word_case, test_check_word_empty_word);
    tcase_add_test(check_word_case, test_check_word_empty_table);
    tcase_add_test(check_word_case, test_check_word);
    tcase_add_test(check_word_case, test_check_word_normal);
    tcase_add_test(check_word_case, test_check_word_num);
    tcase_add_test(check_word_case, test_check_word_num_invalid);
    suite_add_tcase(suite, check_word_case);

    check_words_case = tcase_create("Check Words");
    tcase_add_test(check_words_case, test_check_words_normal);
    suite_add_tcase(suite, check_words_case);

    check_lower_case = tcase_create("Lower Case");
    tcase_add_test(check_lower_case, test_lower_null_l_word);
    tcase_add_test(check_lower_case, test_lower_null_word);
    tcase_add_test(check_lower_case, test_lower_word);
    suite_add_tcase(suite, check_lower_case);

    check_split_line_case = tcase_create("Split Line");
    tcase_add_test(check_split_line_case, test_split_line_empty);
    tcase_add_test(check_split_line_case, test_split_line_single);
    tcase_add_test(check_split_line_case, test_split_line_multiple);
    tcase_add_test(check_split_line_case, test_split_line_multi_spaces);
    suite_add_tcase(suite, check_split_line_case);

    check_remove_punc_case = tcase_create("Remove Punctuation");
    tcase_add_test(check_remove_punc_case, test_remove_punc_one);
    tcase_add_test(check_remove_punc_case, test_remove_punc_two);
    suite_add_tcase(suite, check_remove_punc_case);

    check_spell_check_case = tcase_create("Spell Check");
    tcase_add_test(check_spell_check_case, test_spell_check_null_wordlist);
    tcase_add_test(check_spell_check_case, test_spell_check_null_dictionary);
    tcase_add_test(check_spell_check_case, test_spell_check_fn_null_inputs);
    tcase_add_test(check_spell_check_case, test_spell_check_invalid_word_list);
    tcase_add_test(check_spell_check_case, test_spell_check_invalid_dictionary);
    tcase_add_test(check_spell_check_case, test_spell_check_invalid_inputs);
    tcase_add_test(check_spell_check_case, test_spell_check_valid);
    suite_add_tcase(suite, check_spell_check_case);

    check_is_num_case = tcase_create("Is Number");
    tcase_add_test(check_is_num_case, test_is_num_valid);
    tcase_add_test(check_is_num_case, test_is_num_invalid);
    suite_add_tcase(suite, check_is_num_case);

    return suite;
}

int main(void)
{
    int failed;
    Suite *suite;
    SRunner *runner;

    suite = check_dictionary_suite();
    runner = srunner_create(suite);
    srunner_set_log(runner, "test.log");
    // uncomment the next line if debugging
    // srunner_set_fork_status(runner, CK_NOFORK);
    srunner_run_all(runner, CK_VERBOSE);
    failed = srunner_ntests_failed(runner);
    srunner_free(runner);

    return (failed == 0 ? EXIT_SUCCESS : EXIT_FAILURE);
}

bool check_bucket(hashmap_t hashtable[], char *test_val)
{
    hashmap_t map = hashtable[hash_function(test_val)];

    if (!map)
    {
        return false;
    }
    while (map != NULL)
    {
        if (strcmp(map->word, test_val) == 0)
        {
            return true;
        }
        map = map->next;
    }
    return false;
}
