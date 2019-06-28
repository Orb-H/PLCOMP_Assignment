from scan import Scanner, SymbolTable
import sys


class Parser:
    
    def __init__(self, tokens, table):
        self.tokens = tokens
        self.table = table
        
        self.grammar = ['P->w()B', 'B->{L}', 'B->{}', 'L->LS', 'L->S', 'S->i(C)tBeB', 'S->h(C)B', 'S->w=E;', 'C->E>E', 'C->E<E', 'E->F', 'E->E+F', 'F->n', 'F->w']
        
        self.trie = []
        self.trie.append({'w':'S1'})  # 0
        self.trie.append({'(':'S2'})  # 1
        self.trie.append({')':'S3'})  # 2
        self.trie.append({'{':'S5', 'B':'G4'})  # 3
        self.trie.append({'$':'A'})  # 4
        self.trie.append({'w':'S11', 'i':'S9', 'h':'S10', '}':'S6', 'L':'G7', 'S':'G8'})  # 5
        self.trie.append({'w':'R2', 'i':'R2', 'e':'R2', 'h':'R2', '}':'R2', '$':'R2'})  # 6
        self.trie.append({'w':'S11', 'i':'S9', 'h':'S10', '}':'S12', 'S':'G13'})  # 7
        self.trie.append({'w':'R4', 'i':'R4', 'h':'R4', '}':'R4'})  # 8
        self.trie.append({'(':'S14'})  # 9
        self.trie.append({'(':'S15'})  # 10
        self.trie.append({'=':'S16'})  # 11
        self.trie.append({'w':'R1', 'i':'R1', 'e':'R1', 'h':'R1', '}':'R1', '$':'R1'})  # 12
        self.trie.append({'w':'R3', 'i':'R3', 'h':'R3', '}':'R3'})  # 13
        self.trie.append({'n':'S20', 'w':'S21', 'C':'G17', 'E':'G18', 'F':'G19'})  # 14
        self.trie.append({'n':'S20', 'w':'S21', 'C':'G22', 'E':'G18', 'F':'G19'})  # 15
        self.trie.append({'n':'S20', 'w':'S21', 'E':'G23', 'F':'G19'})  # 16
        self.trie.append({')':'S24'})  # 17
        self.trie.append({'<':'S26', '>':'S25', '+':'S27'})  # 18
        self.trie.append({'<':'R10', '>':'R10', '+':'R10', ';':'R10', ')':'R10'})  # 19
        self.trie.append({'<':'R12', '>':'R12', '+':'R12', ';':'R12', ')':'R12'})  # 20
        self.trie.append({'<':'R13', '>':'R13', '+':'R13', ';':'R13', ')':'R13'})  # 21
        self.trie.append({')':'S28'})  # 22
        self.trie.append({'+':'S27', ';':'S29'})  # 23
        self.trie.append({'t':'S30'})  # 24
        self.trie.append({'n':'S20', 'w':'S21', 'E':'G31', 'F':'G19'})  # 25
        self.trie.append({'n':'S20', 'w':'S21', 'E':'G32', 'F':'G19'})  # 26
        self.trie.append({'n':'S20', 'w':'S21', 'F':'G33'})  # 27
        self.trie.append({'{':'S5', 'B':'G34'})  # 28
        self.trie.append({'w':'R7', 'i':'R7', 'h':'R7', '}':'R7'})  # 29
        self.trie.append({'{':'S5', 'B':'G35'})  # 30
        self.trie.append({'+':'S27', ')':'R8'})  # 31
        self.trie.append({'+':'S27', ')':'R9'})  # 32
        self.trie.append({'<':'R11', '>':'R11', '+':'R11', ';':'R11', ')':'R11'})  # 33
        self.trie.append({'w':'R6', 'i':'R6', 'h':'R6', '}':'R6'})  # 34
        self.trie.append({'e':'S36'})  # 35
        self.trie.append({'{':'S5', 'B':'G37'})  # 36
        self.trie.append({'w':'R5', 'i':'R5', 'h':'R5', '}':'R5'})  # 37

    def parse(self):
        pos = 0
        state = 0
        scope = '0'
        self.tokens.append(('separator', '$'))
        length = len(self.tokens)
        stack = [0]
        nodes = []
        
        for i in range(length - 1):
            if self.tokens[i][0] == 'operator' or self.tokens[i][0] == 'separator' or self.tokens[i][0] == 'keyword':
                nodes.append(Node(self.tokens[i][1], None))
            else:
                nodes.append(Node(self.tokens[i][0], None))
                nodes[-1].child.append(Node(self.tokens[i][1], None))
                nodes[-1].child[-1].parent = nodes[-1]
        
        while pos < length:
            c = self.get_id(self.tokens[pos])
            action = self.trie[state].get(c)
            if action == None:
                print('Parser Error: Invalid token(\'{}\')'.format(self.tokens[pos][1]))
                return None
            if action[0] == 'S':
                state = int(action[1:])
                nodes[pos].id = c
                stack.append(nodes[pos])
                stack.append(state)
                pos = pos + 1
            elif action[0] == 'R':
                gram = self.grammar[int(action[1:])]
                offset = -1
                reduce = []
                while len(gram) + offset >= 3:
                    stack.pop()
                    reduce.append(stack.pop())
                    offset = offset - 1                
                state = int(self.trie[stack[-1]][gram[0]][1:])
                
                n = Node(gram[0], None)
                while len(reduce) != 0:
                    r = reduce.pop()
                    r.parent = n
                    n.child.append(r)
                
                stack.append(n)
                stack.append(state)
            elif action[0] == 'A':
                break
        
        tree = Node('P', None)
        for i in range(len(stack)):
            if type(stack[i]) is Node:
                stack[i].parent = tree
                tree.child.append(stack[i])
        
        self.scope(tree)
        self.tree = tree

    def scope(self, tree):
        level = -1
        scope = []
        visited = []
        stack = []
        
        visited.append(tree)
        stack.append(tree)
        
        while len(stack) != 0:
            flag = False
            
            if len(stack[-1].child) == 0:
                stack.pop()
            else:
                par = stack[-1]
                
            for i in range(0, len(par.child)):
                if par.child[i] not in visited:
                    flag = True
                    stack.append(par.child[i])
                    visited.append(par.child[i])
                    break
            if not flag:
                stack.pop()
        
        for i in range(len(visited)):
            t = visited[i]
            if t.type == '{':
                level = level + 1
                if len(scope) <= level:
                    scope.append(1)
                else:
                    scope[level] = scope[level] + 1
                    for i in range(level + 1, len(scope)):
                        scope[i] = 1
            elif t.type == '}':
                level = level - 1
            elif t.type == '=':
                self.table.add_scope(visited[i - 1].type, '.'.join([str(s) for s in scope[0:level + 1]]))
    
        for c in self.table.d.keys():
            s = self.table.d[c][0][:]
            removed = []
            for i in range(len(s)):
                if i in removed:
                    continue
                for j in range(i + 1, len(s)):
                    if j in removed:
                        continue
                    if s[i] in s[j]:
                        removed.append(j)
                    elif s[j] in s[i]:
                        removed.append(i)
            for i in range(len(removed), 0, -1):
                del s[i]
            self.table.d[c][0] = s
        
        scope = []
        for i in range(len(visited)):
            t = visited[i]
            if t.type == '{':
                level = level + 1
                if len(scope) <= level:
                    scope.append(1)
                else:
                    scope[level] = scope[level] + 1
                    for i in range(level + 1, len(scope)):
                        scope[i] = 1
            elif t.type == '}':
                level = level - 1
            elif len(scope) != 0 and t.type == 'word':
                u = visited[i + 1]
                s = self.table.get_scope(u.type)
                t = '.'.join([str(a) for a in scope[0:level + 1]])
                exist = False
                for sc in s:
                    if sc in t:
                        exist = True
                        break
                if not exist:
                    print("Parser Error: Undefined variable '{}' in scope {}".format(u.type, t))
                    sys.exit(0)

    def get_tree(self):
        return self.tree

    def get_id(self, token):
        if token[0] == 'number':
            return 'n'
        elif token[0] == 'word':
            return 'w'
        elif token[0] == 'operator' or token[0] == 'separator':
            return token[1]
        else:
            if token[1] == 'IF':
                return 'i'
            elif token[1] == 'THEN':
                return 't'
            elif token[1] == 'ELSE':
                return 'e'
            elif token[1] == 'WHILE':
                return 'h'
            else:
                return None

    def get_symbol_table(self):
        return self.table


class Node:
    
    def __init__(self, type, content, parent=None):
        self.child = []
        self.parent = parent
        self.type = type
        self.content = content
        self.id = ''
    
    def __repr__(self, level=0):
        ret = "\t" * level + self.type + ((': ' + self.content) if self.content != None else '') + "\n"
        for child in self.child:
            ret += child.__repr__(level + 1)
        return ret


if __name__ == '__main__':  # main for test
    scan = Scanner()
    if len(sys.argv) == 1:
        while True:
            s = input()
            if s == '.':
                break
            scan.scan_string(s)
        p = Parser(scan.get_tokens(), scan.get_symbol_table())
        print(str(p.parse()))
        print(p.get_symbol_table())
    elif len(sys.argv) == 2:
        scan.scan_file(open(sys.argv[1], 'r'))
        p = Parser(scan.get_tokens(), scan.get_symbol_table())
        print(str(p.parse()))
        print(p.get_symbol_table())
