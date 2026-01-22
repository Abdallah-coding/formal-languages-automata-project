%{
#include "regexp.tab.h"
%}

%%
"a" { return A; }
"b" { return B; }
"c" { return C; }
"+" { return PLUS; }
"." { return DOT; }
"*" { return STAR; }
"(" { return '('; }
")" { return ')'; }

[ \t\r]+ { }
\n { return '\n'; }
. { }
%%
