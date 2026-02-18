# Formal Languages & Automata (Academic Project)

Formal Languages &amp; Automata Project (Python, Lex/Yacc, DFA/NFA, Minimization)

## Project Objective

The goal of this project is to determine whether **two regular expressions are equivalent**
by proving that they recognize the **same language**.

This is achieved by:
1. Translating each regular expression into a finite automaton
2. Handling ε-transitions
3. Determinizing the automata (subset construction)
4. Completing the automata with a sink state
5. Minimizing the resulting deterministic automata
6. Checking equivalence between the final automata

If the resulting deterministic complete automata are equivalent, then the two regular
expressions are proven to be equivalent.


## Project Structure

theory-of-languages-automata/

├── README.md

├── Project_Specification.pdf

├── Makefile

├── python/

│ └── automate.py

├── lex_yacc/

│ ├── regexp.l

│ └── regexp.y

## Key Features
- Automata operations: union, concatenation, Kleene star
- ε-closure computation
- ε-transition elimination
- Determinization (subset construction)
- Completion with sink state
- Minimization (Moore algorithm)
- Language equivalence checking

## Academic Context
This project was carried out during the third year (L3) of a Computer Science degree and
demonstrates the application of **theoretical computer science concepts** in a concrete implementation.

## Author
Abdallah-coding
