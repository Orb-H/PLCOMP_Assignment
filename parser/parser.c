#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef TOKEN_STRUCT_DEFINED

typedef enum {
	SEPARATOR, OPERATOR, KEYWORD, NUMBER, WORD
} TYPE;

typedef struct {
	TYPE type;
	char* content;
} token;

typedef struct {
	struct _node* head;
	struct _node* tail;
	int length;
} list;

typedef struct _node {
	token* data;
	struct _node* next;
} node;

#endif

typedef struct {
	int type;//0 for const, 1 for token
	union u {
		token* t;
		int* n;
	};
	struct element* next;
} element;

typedef struct {
	int size;
	element* top;
} stack;