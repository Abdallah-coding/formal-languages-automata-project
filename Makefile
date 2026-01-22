CC = gcc
CFLAGS = -Wall
LEX = flex
YACC = bison
PYTHON = python3

LEX_FILE = regexp.l
YACC_FILE = regexp.y

LEX_C = regexp.yy.c
YACC_C = regexp.tab.c
YACC_H = regexp.tab.h

EXEC = regexp

all: $(EXEC)

$(YACC_C) $(YACC_H): $(YACC_FILE)
	$(YACC) -d $(YACC_FILE)

$(LEX_C): $(LEX_FILE) $(YACC_H)
	$(LEX) -o $(LEX_C) $(LEX_FILE)

$(EXEC): $(LEX_C) $(YACC_C)
	$(CC) $(CFLAGS) -o $(EXEC) $(YACC_C) $(LEX_C) -lfl

test:
	$(PYTHON) automate.py

clean:
	rm -f $(EXEC) $(LEX_C) $(YACC_C) $(YACC_H) main.py

