
def longest_palindrome(ipt_str):
    m = len(ipt_str)
    rev_str = ipt_str[::-1]
    opt = np.zeros((n,n), dtype = int)
    ind = np.zeros((n,n), dtype = str)

    for j in range(0, m+1):
        opt[0][j] = 0

    for i in range(1, m+1):
        opt[i][0] = 0 
        print(opt[i])
        for j in range(1, m+1):
            if ipt_str[i - 1] == rev_str[j - 1]:
                opt[i][j] = opt[i-1][j-1] + 1
                index[i][j] = '*'
            
            elif opt[i][j - 1] > opt[i - 1][j]:
                opt[i][j] = opt[i][j - 1]
                index[i][j] = 'l'
            
            else:
                opt[i][j] = opt[i - 1][j]   
                index[i][j] = 'u'

    i = n - 1
    j = n - 1
    s = ""
    while i > 0 and j > 0:
        if ind[i][j] == '*':
            s = ipt_str[i] + s
            i = i - 1
            j = j - 1
        elif ind[i][j] == 'u':
            i = i - 1
        else:
            j = j - 1
    return opt[n-1][n-1], s



if __name__ == '__main__':
    s = 'badccbda'
    l,p = longest_palindrome(s)
    print("length of palindrome:", l)
    print("palindrome:", p)



