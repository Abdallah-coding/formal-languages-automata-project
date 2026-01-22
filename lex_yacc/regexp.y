%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define _GNU_SOURCE

int yylex(void);
void yyerror(const char *s) { fprintf(stderr, "Erreur: %s\n", s); }

char buffer[4096];
%}

%union { char* s; }

%token A B C PLUS STAR DOT
%type <s> expr

%left PLUS
%left DOT
%right STAR

%start input

%%
input : expr NL expr optNL
	{
		FILE *f = fopen("main.py", "w");
		if(!f) { perror("main.py"); exit(1); }

		fprintf(f, "from automate import *\n\n");
		fprintf(f, "A1 = %s\n", $1);
		fprintf(f, "A2 = %s\n\n", $3);
		
		fprintf(f, "if egal(A1, A2):\n");
		fprintf(f, "	print(\"EGAL\")\n");
		fprintf(f, "else:\n");
		fprintf(f, "	print(\"NON EGAL\")\n");

		fclose(f);

		printf("Fichier main.py a été generé avec succès :");
};

optNL : | optNL NL ;

NL : '\n';

expr : 
	expr PLUS expr { sprintf(buffer, "union(%s,%s)", $1, $3); $$ = strdup(buffer);}

	| expr DOT expr { sprintf(buffer, "concatenation(%s, %s)", $1, $3); $$ = strdup(buffer);}
	
	| expr STAR { sprintf(buffer, "etoile(%s)", $1); $$ = strdup(buffer);}
	
	| '(' expr ')' { $$ = $2; }

	| A { $$ = strdup("automate(\"a\")"); }
	
	| B { $$ = strdup("automate(\"b\")"); }

	| C { $$ = strdup("automate(\"c\")"); }
	;
%%

int main() { return yyparse(); }
