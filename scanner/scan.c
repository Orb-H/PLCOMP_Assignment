#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int check_separator(char* input, int len){
	if((input[0]=='(')||(input[0]==')')||(input[0]=='{')||(input[0]=='}')||(input[0]==';')){
		printf("separator %c\n",input[0]);
		return 1;
	}
	return 0;
}

int check_operator(char* input, int len){
	if((input[0]=='+')||(input[0]=='>')||(input[0]=='<')||(input[0]=='=')){
		printf("operator %c\n",input[0]);
		return 1;
	}
	return 0;
}

int check_keyword(char* input, int len){
	if(len>=2 && !strncmp(input,"IF",2)){
		printf("keyword IF\n");
		return 2;
	} else if(len>=4 && !strncmp(input,"THEN",4)){
		printf("keyword THEN\n");
		return 4;
	} else if(len>=4 && !strncmp(input,"ELSE",4)){
		printf("keyword ELSE\n");
		return 4;
	} else if(len>=5 && !strncmp(input,"WHILE",5)){
		printf("keyword WHILE\n");
		return 5;
	}
	return 0;
}

int check_digit(char* input, int len){
	int length=0;
	if(input[0]>='0' && input[0]<='9'){
		int i=0;
		while(i++<len){
			if(input[i]<'0' || input[i]>'9') break;
		}
		return i;
	}
	return 0;
}

int check_letter(char* input, int len){
	int length=0;
	if((input[0]>='A' && input[0]<='Z')||(input[0]>='a' && input[0]<='z')){
		int i=0;
		while(i++<len){
			if((input[i]<'A' || input[i]>'Z')&&(input[i]<'a' || input[i]>'z')) break;
		}
		return i;
	}
	return 0;
}

void scan(char* input, int len){
	if(len==0) return;
	if(check_separator(input,len)) scan(input+1,len-1);
	else if(check_operator(input,len)) scan(input+1,len-1);
	else{
		int a=check_keyword(input,len);
		if(a>0) scan(input+a,len-a);
		else{
			a=check_digit(input,len);
			if(a>0){
				printf("num %.*s\n",a,input);
				scan(input+a,len-a);
			} else{
				a=check_letter(input,len);
				if(a>0){
					printf("word %.*s\n",a,input);
					scan(input+a,len-a);
				}else{
					printf("Lexer Error: Unknown Symbol\n");
				}
			}
		}
	}
}

int main(){
	char* c=(char*)malloc(100);
	while(1){
		scanf("%s",c);
		scan(c,strlen(c));
	}
}