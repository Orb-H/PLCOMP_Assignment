separators = ['(', ')', '{', '}', ';']
operators = ['+', '>', '<', '=']
keywords = ['IF', 'THEN', 'ELSE', 'WHILE']
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
tokens = []


def check_separator(s):
    if s[0] in separators:
        print('separator ' + s[0])
        return True
    return False


def check_operator(s):
    if s[0] in operators:
        print('operator ' + s[0])
        return True
    return False


def check_keyword(s):
    if (len(s) == 2 and s[0:2] == keywords[0]) or (len(s) > 2 and s[0:2] == keywords[0] and s[2] not in letters):
        print('keyword IF')
        return 2
    elif (len(s) == 4 and s[0:4] == keywords[1]) or (len(s) > 4 and s[0:4] == keywords[1] and s[4] not in letters):
        print('keyword THEN')
        return 4
    elif (len(s) == 4 and s[0:4] == keywords[2]) or (len(s) > 4 and s[0:4] == keywords[2] and s[4] not in letters):
        print('keyword ELSE')
        return 4
    elif (len(s) == 5 and s[0:5] == keywords[3]) or (len(s) > 5 and s[0:5] == keywords[3] and s[5] not in letters):
        print('keyword WHILE')
        return 5
    return 0


def check_digit(s):
    length = 0
    if s[0] in digits:
        i = 0
        while i < len(s) and s[i] in digits:
            i = i + 1
        return i
    return 0


def check_letter(s):
    length = 0
    if s[0] in letters:
        i = 0
        while i < len(s) and s[i] in letters:
            i = i + 1
        return i
    return 0


def scan(s):
    if len(s) == 0:
        return
    if check_separator(s):
        tokens.append(('separator', s[0]))
        scan(s[1:])
    elif check_operator(s):
        tokens.append(('operator', s[0]))
        scan(s[1:])
    else:
        a = check_keyword(s)
        if a > 0:
            tokens.append(('keyword', s[0:a]))
            scan(s[a:])
        else:
            a = check_digit(s)
            if a > 0:
                print('num ' + s[0:a])
                tokens.append(('num', s[0:a]))
                scan(s[a:])
            else:
                a = check_letter(s)
                if a > 0:
                    print('word ' + s[0:a])
                    tokens.append(('word', s[0:a]))
                    scan(s[a:])
                else:
                    print('Lexer Error: Unknown Symbol')
        

if __name__ == "__main__": #main for TEST
    while True:
        s = input()
        if s == '.':
            break
        scan(s)
    print(tokens)
