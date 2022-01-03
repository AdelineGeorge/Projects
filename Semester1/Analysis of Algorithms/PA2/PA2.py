import numpy as np
import sys

# function to to output the longest palindrome subsequence and it's length
def longest_palindrome(ipt_str):
    n = len(ipt_str)                                  # calculating the length of input string
    rev_str = ipt_str[::-1]                           # reversing the string
    
    opt = np.zeros((n + 1, n + 1), dtype = int)       # Initializing opt - array
    ind = np.zeros((n + 1, n + 1), dtype = str)       # Initializing array to store indices of matches

    for j in range(0, n + 1):
        opt[0][j] = 0                                 # Initializing the the first row with 0s

    for i in range(1, n + 1):
        opt[i][0] = 0                                 # Initializing the the first column with 0s

        for j in range(1, n + 1):

            if ipt_str[i - 1] == rev_str[j - 1]:      # Checking if there is a match
                opt[i][j] = opt[i-1][j-1] + 1
                ind[i][j] = '*'                       # Updating "ind" array with "*" to indicate a match
            
            elif opt[i][j - 1] > opt[i - 1][j]:       # Updating with value on the left if it is greater
                opt[i][j] = opt[i][j - 1]
                ind[i][j] = '<'                       # Updating "ind" array with "<" to show that the value on the left is greater
            
            else:                                     # Updating with the value above if it is greater
                opt[i][j] = opt[i - 1][j]   
                ind[i][j] = '^'                       # Updating "ind" array with "^" to show that the value above is greater

    i = n                                             # Backtracking the "ind" array to print the subsequence
    j = n
    s = ""
    while i > 0 and j > 0:
        if ind[i][j] == '*':                          
            s = ipt_str[i - 1] + s
            i = i - 1
            j = j - 1
        elif ind[i][j] == '^':
            i = i - 1
        else:
            j = j - 1
    return opt[n][n], s                                # Returning the palindromic subsequence and the last element of "opt" array as the palindrome length



if __name__ == '__main__':    
    line = sys.stdin.readline()                        # Reading input
    l,p = longest_palindrome(line)                     # Function call
    print(l)                                           # Printing the length of the palindromic subsequence
    print(p)                                           # Printing the palindromic subsequence



