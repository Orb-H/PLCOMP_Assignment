import sys


class Scanner:

    def __init__(self):
        self.separators = ['(', ')', '{', '}', ';']
        self.operators = ['+', '>', '<', '=']
        self.keywords = ['IF', 'THEN', 'ELSE', 'WHILE']
        self.digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.whitespaces = [' ', '\n', '\t', '\r']
        self.tokens = []
        self.table = SymbolTable()
    
    def scan_file(self, f):  # Run this function once to read all the inputs. Just call get_tokens at the end to get all the tokens from input.
        f = open(sys.argv[1], 'r')
        lines = f.readlines()
        for line in lines:
            self.scan_string(line)

    def scan_string(self, s):  # Run this function as many as you want. Just call get_tokens at the end to get all the tokens from input.
        while len(s) != 0:
            if self.check_separator(s):
                self.tokens.append(('separator', s[0]))
                s = s[1:]
            elif self.check_operator(s):
                self.tokens.append(('operator', s[0]))
                s = s[1:]
            else:
                a = self.check_keyword(s)
                if a > 0:
                    self.tokens.append(('keyword', s[0:a]))
                    s = s[a:]
                else:
                    a = self.check_digit(s)
                    if a > 0:
                        # print('num ' + s[0:a])
                        self.tokens.append(('num', s[0:a]))
                        s = s[a:]
                    else:
                        a = self.check_letter(s)
                        if a > 0:
                            # print('word ' + s[0:a])
                            self.tokens.append(('word', s[0:a]))
                            s = s[a:]
                        elif s[0] in self.whitespaces:
                            s = s[1:]
                        else:
                            print('Lexer Error: Unknown Symbol')
    
    def check_separator(self, s):
        if s[0] in self.separators:
            # print('separator ' + s[0])
            return True
        return False

    def check_operator(self, s):
        if s[0] in self.operators:
            # print('operator ' + s[0])
            if s[0] == '=':
                self.table.add_symbol(self.tokens[-1][1])
            return True
        return False

    def check_keyword(self, s):
        if (len(s) == 2 and s[0:2] == self.keywords[0]) or (len(s) > 2 and s[0:2] == self.keywords[0] and s[2] not in self.letters):
            # print('keyword IF')
            return 2
        elif (len(s) == 4 and s[0:4] == self.keywords[1]) or (len(s) > 4 and s[0:4] == self.keywords[1] and s[4] not in self.letters):
            # print('keyword THEN')
            return 4
        elif (len(s) == 4 and s[0:4] == self.keywords[2]) or (len(s) > 4 and s[0:4] == self.keywords[2] and s[4] not in self.letters):
            # print('keyword ELSE')
            return 4
        elif (len(s) == 5 and s[0:5] == self.keywords[3]) or (len(s) > 5 and s[0:5] == self.keywords[3] and s[5] not in self.letters):
            # print('keyword WHILE')
            return 5
        return 0

    def check_digit(self, s):
        length = 0
        if s[0] in self.digits:
            i = 0
            while i < len(s) and s[i] in self.digits:
                i = i + 1
            return i
        return 0
    
    def check_letter(self, s):
        length = 0
        if s[0] in self.letters:
            i = 0
            while i < len(s) and s[i] in self.letters:
                i = i + 1
            return i
        return 0
    
    def get_tokens(self):
        return self.tokens

    def get_symbol_table(self):
        return self.table


class SymbolTable:

    def __init__(self):
        self.d = {}
    
    def add_symbol(self, c):
        if self.find_symbol(c) == None:
            self.d[c] = [None, None]
    
    def find_symbol(self, c):
        return self.d.get(c)
    
    def get_scope(self, c):
        if self.d.get(c) == None:
            return None
        return self.d[c][0]
    
    def set_scope(self, c, scope):
        if self.d.get(c) == None:
            raise Error("No such symbol in table")
        self.d[c][0] = scope
        
    def get_value(self, c):
        if self.d.get(c) == None:
            return None
        return self.d[c][1]
    
    def set_value(self, c, value):
        if self.d.get(c) == None:
            raise Error("No such symbol in table")
        self.d[c][1] = value
        
    def __str__(self):
        s = 'Name\tScope\tValue\n'
        for i in self.d.keys():
            s += i + '\t' + str(self.get_scope(i)) + '\t' + str(self.get_value(i)) + '\n'
        return s


if __name__ == "__main__":  # main for TEST
    scan = Scanner()
    if len(sys.argv) == 1:
        while True:
            s = input()
            if s == '.':
                break
            scan.scan_string(s)
        print(scan.get_tokens())
        print(scan.get_symbol_table())
    elif len(sys.argv) == 2:
        scan.scan_file(open(sys.argv[1], 'r'))
        print(scan.get_tokens())
        print(scan.get_symbol_table())
        
