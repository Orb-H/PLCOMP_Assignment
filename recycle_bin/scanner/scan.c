#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

typedef struct {
	int state;
	int go_to[127];
	int endtype;// 0 for nothing, 1 for separator, 2 for operator, 3 for keyword, 4 for number, 5 for word
} trie;

int initialized = 0;
list* l;
trie* t[20];

void add_token(TYPE type, char* content) {
	token* t = (token*)malloc(sizeof(token));
	t->type = type;
	t->content = content;

	l->tail->next = (node*)malloc(sizeof(node));
	l->tail = l->tail->next;
	l->tail->data = t;
	l->tail->next = NULL;
	l->length++;
}

void print_tokens() {//for debugging
	node* cur = l->head;
	while (cur->next != NULL) {
		cur = cur->next;
		printf("%d %s\n", cur->data->type, cur->data->content);
	}
}

list* get_tokens() {
	return l;
}

void init() {
	l = (list*)malloc(sizeof(list));
	l->length = 0;
	l->head = (node*)malloc(sizeof(node));//dummy node for easy control
	l->head->data = NULL;
	l->head->next = NULL;
	l->tail = l->head;

	char temp;

	// node 0 in state diagram for NFA in report
	t[0] = (trie*)malloc(sizeof(trie));
	t[0]->state = 0;
	t[0]->endtype = 0;

	for (temp = 0; temp < 127; temp++) t[0]->go_to[temp] = -1;
	for (temp = '0'; temp <= '9'; temp++) t[0]->go_to[temp] = 19;
	for (temp = 'A'; temp <= 'Z'; temp++) t[0]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[0]->go_to[temp] = 18;
	t[0]->go_to['{'] = 1;
	t[0]->go_to['}'] = 1;
	t[0]->go_to['('] = 1;
	t[0]->go_to[')'] = 1;
	t[0]->go_to[';'] = 1;
	t[0]->go_to['<'] = 2;
	t[0]->go_to['>'] = 2;
	t[0]->go_to['+'] = 2;
	t[0]->go_to['='] = 2;
	t[0]->go_to['I'] = 3;
	t[0]->go_to['T'] = 5;
	t[0]->go_to['E'] = 9;
	t[0]->go_to['W'] = 13;
	t[0]->go_to[' '] = 0;
	t[0]->go_to['\t'] = 0;
	t[0]->go_to['\n'] = 0;
	t[0]->go_to['\r'] = 0;

	//node 1
	t[1] = (trie*)malloc(sizeof(trie));
	t[1]->state = 1;
	t[1]->endtype = 1;
	for (temp = 0; temp < 127; temp++) t[1]->go_to[temp] = -1;

	//node 2
	t[2] = (trie*)malloc(sizeof(trie));
	t[2]->state = 2;
	t[2]->endtype = 2;
	for (temp = 0; temp < 127; temp++) t[2]->go_to[temp] = -1;

	//node 3
	t[3] = (trie*)malloc(sizeof(trie));
	t[3]->state = 3;
	t[3]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[3]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[3]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[3]->go_to[temp] = 18;
	t[3]->go_to['F'] = 4;

	//node 4
	t[4] = (trie*)malloc(sizeof(trie));
	t[4]->state = 4;
	t[4]->endtype = 3;
	for (temp = 0; temp < 127; temp++) t[4]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[4]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[4]->go_to[temp] = 18;

	//node 5
	t[5] = (trie*)malloc(sizeof(trie));
	t[5]->state = 5;
	t[5]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[5]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[5]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[5]->go_to[temp] = 18;
	t[5]->go_to['H'] = 6;

	//node 6
	t[6] = (trie*)malloc(sizeof(trie));
	t[6]->state = 6;
	t[6]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[6]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[6]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[6]->go_to[temp] = 18;
	t[6]->go_to['E'] = 7;

	//node 7
	t[7] = (trie*)malloc(sizeof(trie));
	t[7]->state = 7;
	t[7]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[7]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[7]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[7]->go_to[temp] = 18;
	t[7]->go_to['N'] = 8;

	//node 8
	t[8] = (trie*)malloc(sizeof(trie));
	t[8]->state = 8;
	t[8]->endtype = 3;
	for (temp = 0; temp < 127; temp++) t[8]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[8]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[8]->go_to[temp] = 18;

	//node 9
	t[9] = (trie*)malloc(sizeof(trie));
	t[9]->state = 9;
	t[9]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[9]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[9]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[9]->go_to[temp] = 18;
	t[9]->go_to['L'] = 10;

	//node 10
	t[10] = (trie*)malloc(sizeof(trie));
	t[10]->state = 10;
	t[10]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[10]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[10]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[10]->go_to[temp] = 18;
	t[10]->go_to['S'] = 11;

	//node 11
	t[11] = (trie*)malloc(sizeof(trie));
	t[11]->state = 11;
	t[11]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[11]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[11]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[11]->go_to[temp] = 18;
	t[11]->go_to['E'] = 12;

	//node 12
	t[12] = (trie*)malloc(sizeof(trie));
	t[12]->state = 12;
	t[12]->endtype = 3;
	for (temp = 0; temp < 127; temp++) t[12]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[12]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[12]->go_to[temp] = 18;

	//node 13
	t[13] = (trie*)malloc(sizeof(trie));
	t[13]->state = 13;
	t[13]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[13]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[13]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[13]->go_to[temp] = 18;
	t[13]->go_to['H'] = 14;

	//node 14
	t[14] = (trie*)malloc(sizeof(trie));
	t[14]->state = 14;
	t[14]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[14]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[14]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[14]->go_to[temp] = 18;
	t[14]->go_to['I'] = 15;

	//node 15
	t[15] = (trie*)malloc(sizeof(trie));
	t[15]->state = 15;
	t[15]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[15]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[15]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[15]->go_to[temp] = 18;
	t[15]->go_to['L'] = 16;

	//node 16
	t[16] = (trie*)malloc(sizeof(trie));
	t[16]->state = 16;
	t[16]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[16]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[16]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[16]->go_to[temp] = 18;
	t[16]->go_to['E'] = 17;

	//node 17
	t[17] = (trie*)malloc(sizeof(trie));
	t[17]->state = 17;
	t[17]->endtype = 3;
	for (temp = 0; temp < 127; temp++) t[17]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[17]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[17]->go_to[temp] = 18;

	//node 18
	t[18] = (trie*)malloc(sizeof(trie));
	t[18]->state = 18;
	t[18]->endtype = 5;
	for (temp = 0; temp < 127; temp++) t[18]->go_to[temp] = -1;
	for (temp = 'A'; temp <= 'Z'; temp++) t[18]->go_to[temp] = 18;
	for (temp = 'a'; temp <= 'z'; temp++) t[18]->go_to[temp] = 18;

	//node 19
	t[19] = (trie*)malloc(sizeof(trie));
	t[19]->state = 19;
	t[19]->endtype = 4;
	for (temp = 0; temp < 127; temp++) t[19]->go_to[temp] = -1;
	for (temp = '0'; temp <= '9'; temp++) t[19]->go_to[temp] = 19;

	initialized = 1;
}

void scan(char* input, int len) {
	if (!initialized) init();

	char* res = (char*)malloc(20);
	int length = 0;
	int state = 0;
	int pos = 0;
	int next = -1;
	res[0] = 0;

	while(input[pos]!=0) {
		next = t[state]->go_to[input[pos]];
		if (next == -1) {
			if (t[state]->endtype != 0) {
				add_token(t[state]->endtype - 1, res);
				length = 0;
				res = (char*)malloc(20);
				state = 0;
			}
			else {
				printf("Lexer Error ----- unknown symbol: %c", input[pos]);
				exit(1);
			}
		}
		else if (next != 0) {
			state = next;
			if (length == strlen(res)) res = realloc(res, strlen(res) + 21);
			res[length] = input[pos++];
			res[++length] = 0;
		}
	}
	if (state != 0) {
		if (t[state]->endtype != 0) {
			add_token(t[state]->endtype - 1, res);
		}
		else {
			printf("Lexer Error ----- unknown symbol: %c", input[pos]);
			exit(1);
		}
	}
}

int main() {
	init();

	while (1) {
		char* c = malloc(100);
		scanf("%s", c);
		if (c[0] == '.') break;
		scan(c, strlen(c));
	}
	print_tokens();//debug
}