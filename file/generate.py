import sys
from scan import Scanner, SymbolTable
from parse2 import Parser, Node


class Generator():

    def __init__(self, tree, table, file):
        self.tree = tree
        self.table = table
        self.file = file
        
        self.jump = 0
        self.max = 0
    
    def generate(self):
        name = self.tree.child[0].child[0].type
        self.code = 'BEGIN {}\n'.format(name)
        self.table.add_symbol(name)
        self.table.add_scope(name, '0')
        self.table.set_type(name, 'Func')
        
        self.code += self.generate_code(self.tree.child[3])
        
        self.code += 'END {}\n'.format(self.tree.child[0].child[0].type)
        
        self.code += '\n{} registers used'.format(self.get_reg_max())
        
    def generate_code(self, node, num=0):
        if self.max < num:
            self.max = num
        if node.type == 'B':
            if node.child[1].type != '}':
                return self.generate_code(node.child[1], num);
            return '';
        if node.type == 'L':
            s = ''
            for i in range(len(node.child)):
                s += self.generate_code(node.child[i], num)
            return s
        if node.type == 'C':
            s = self.generate_code(node.child[0], num) + self.generate_code(node.child[2], num + 1)
            if node.child[1].type == '<':
                s += '\tLT\tREG#{},\tREG#{},\tREG#{}\n'.format(num, num, num + 1)
            else:
                s += '\tLT\tREG#{},\tREG#{},\tREG#{}\n'.format(num, num + 1, num)
            return s
        if node.type == 'F':
            return '\tLD\tREG#{},\t{}\n'.format(num, node.child[0].child[0].type)
        if node.type == 'S':
            if node.child[1].type == '=':
                s = self.generate_code(node.child[2], num)
                s += '\tST\tREG#{},\t{}\n'.format(num, node.child[0].child[0].type)
                return s
            if node.child[0].id == 'i':
                s = self.generate_code(node.child[2], num)
                self.jump += 2
                j = self.jump
                s += '\tJUMPF\tREG#{},\t.L{}\n'.format(num, j - 1)
                s += self.generate_code(node.child[5], num)
                s += '\tJUMP\t.L{}\n'.format(j)
                s += '.L{}\n'.format(j - 1)
                s += self.generate_code(node.child[7], num)
                s += '.L{}\n'.format(j)
                return s
            elif node.child[0].id == 'h':
                self.jump += 2
                j = self.jump
                s = '.L{}\n'.format(j - 1)
                s += self.generate_code(node.child[2], num)
                s += '\tJUMPF\tREG#{},\t.L{}\n'.format(num, j)
                s += self.generate_code(node.child[4], num)
                s += '\tJUMP\t.L{}\n'.format(j - 1)
                s += '.L{}\n'.format(j)
                return s
        if node.type == 'E':
            if len(node.child) == 1:
                return self.generate_code(node.child[0], num)
            else:
                s = self.generate_code(node.child[0], num) + self.generate_code(node.child[2], num)
                s += '\tADD\tREG#{},\tREG#{},\tREG#{}\n'.format(num, num, num + 1)
                return s
    
    def get_code(self):
        return self.code
    
    def get_reg_max(self):
        return self.max + 1
    
    def write_file(self):
        f = open(self.file + '.code', 'w')
        f.write(self.get_code())
        f.close()
        
        f = open(self.file + '.symbol', 'w')
        f.write(str(self.table))
        f.close()
