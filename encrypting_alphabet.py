# Constants at the top of the file
NORMAL_ALPHABET = ["a", "b", "c", "d"]
ENCRYPTED_ALPHABET = ["d", "c", "a", "b"]

def find_index_of_char(alphabet_list, char):
    """
        Function that finds the index of a character in a list containing characters (an alphabet)
        
        If the letter is not found we return a "bad" index, something that will indicate to the other functions
        that the letter was not found. In this case we return length_of_alphabet_list. We do this to cause 
        an "IndexError" in any program/function that uses this function.
        
        Paramaters:
            alphabet_list (list) : the list containing the letters to look for
            char           (str) : the letter you are looking for
        
        Return:
            int : if the letter is found we return the position in the string, otherwise we return a bad index
    """
    # *enumerate* is a nice function python gives you
    # basically it converts a list into a list of tuples like so
    # ["h","e", "l", "l", "o"] -> [(0,"h"), (1, "e"), (2, "l"), (3, "l"), (4, "o")]
    for i, char2 in enumerate(alphabet_list):
        
        if char2 == char: # if the characters match
            
            return i # return the position -> remember the function ends when it hits a "return line"
                     # so if the character is found, we return this position and don't continue to the
                     # return below!
    
    
    
    # so as mentioned in class, if a list has N items in it, the indexes of the list go from 0 -> N-1.
    # however python allows you to do some cool things with lists
    # if you wanted to access the last element of the list there are two ways you can do this:
    # list[N-1]
    # list[-1] # TRY THIS
    # not all languages allow this! this is a nice thing python does for you!
    # 
    # so I return len(alphabet_list) instead of -1 (in most languages you would return -1),
    # because I know list[N] will cause an error.
    
    return len(alphabet_list)

def convert_string(string, current_alphabet, converted_alphabet):
    """
        Converts a string from one alphabet ordering to another alphabet ordering
        
        Paramaters:
            string              (str) : text to be converted
            current_alphabet   (list) : the current ordering of letters the string is using
            converted_alphabet (list) : the ordering you want the string to be converted into
        
        Return:
            str : the converted string
    """
    try:
        converted_string = "" # the converted string I will ultimately output
        
        for char in string: # for each letter in the string
            
            index = find_index_of_char(current_alphabet, char) # find the position of the letter in the current alphabet
            
            converted_letter = converted_alphabet[index] # look up what letter the above position refers to in the converted alphabet
            
            converted_string = converted_string + converted_letter # add that converted letter to your output string
        
        return converted_string
    
    except IndexError:
        # so remember if I can't find the position of a letter in the alphabet, I return an index that causes an error
        # I'm letting the user know they caused an error, and that error is caused by them giving me a bad string
        print("\nYour inputed string contained letters outside the alphabet!")
    
    except:
        # here I am catching an error that I couldn't think of, not very helpful for the user though
        print("\nUh oh I errored :/")

def bad_input():
    """
        An example of a "void" function
        
        This has no parameters and returns nothing -> the returning nothing part makes it void
    """
    print("\nYou didn't input e or d!")

def main():
    """
        Function that starts up the encryption/decryption program
        
        Again this is a void function, there is no return statement!
    """
    user_wants_to_continue = True
    
    # this is how you can make a program run forever (remember while loops need to be ended)
    while user_wants_to_continue:
        string_to_convert = input("Please input the string you would like to encrypt."\
                                  "\nMake sure the letters in your string are in my accepted alphabet!")
        
        user_request = input("\nWould you like to encrypt or decrypt your string?"\
                             " Enter e for encrypt or d for decrypt.")
        output = None
        
        if user_request == "e":
            output = convert_string(string_to_convert, NORMAL_ALPHABET, ENCRYPTED_ALPHABET)
            if output: # only printing if output != None
                print("\nHere is your encrypted string: ", output)
        
        elif user_request == "d":
            output = convert_string(string_to_convert, ENCRYPTED_ALPHABET, NORMAL_ALPHABET)
            if output: # only printing if output != None
                print("\nHere is your decrypted string: ", output)
        
        else:
            bad_input()
        
        user_response = input("\nWould you like to try another example, enter y or n\n\n")
        
        # not only am I accepting the response of "n" to end the program, but I am also penalizing users who
        # try to mess with my program. If the user doesn't explicitly type in "y" then I am quitting on them.
        if user_response != "y":
            user_wants_to_continue = False # will cause the loop to end
            
    print("PEACE OUT")

if __name__ == "__main__":
    main()