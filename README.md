# PLCOMP_Assignment
Team Assignment for 'Programming Language and Compiler' class

## Assignment File
[File](Compiler_Project-2019.pdf)

## Things to do
 - Scanner
 - Parser
 - Code Generator

## Scanner
### Grammar
```
prog    ::= word "(" ")" block ;
block	::= "{" slist "}"	
        |   ;
slist 	::= slist stat
        |   stat ;
stat 	::= IF "(" cond ")" THEN block ELSE block
        |   WHILE "(" cond ")" block
        |   word "=" expr ";"
        |   ;
cond 	::= expr ">" expr
        |   expr "<" expr ;
expr 	::= fact
        |   expr "+" fact ;	
fact 	::= num
        |   word ;
word	::= ([a-z] | [A-Z])* ;
num     ::= [0-9]*
```
### Each Grammar to NFA
 - num
 
 ![NFA_num](scanner/image/nfa_num.png)
 - word
 
 ![NFA word](scanner/image/nfa_word.png)
 - fact
 
 ![NFA fact](scanner/image/nfa_fact_simple.png)
 - expr
 
 ![NFA expr](scanner/image/nfa_expr_simple.png)
 - cond
 
 ![NFA cond](scanner/image/nfa_cond_simple.png)
 - stat
 
 ![NFA stat](scanner/image/nfa_stat_simple.png)
 - slist
 
 ![NFA slist](scanner/image/nfa_slist_simple.png)
 - block
 
 ![NFA block](scanner/image/nfa_block_simple.png)
 - prog
 
 ![NFA prog](scanner/image/nfa_prog_simple.png)

### Combining NFAs
TODO.

## Parser
TODO.

## Code Generator
TODO.
