line a1
line b2
line c3
line d4
line 5
line 6

line a1
line a1
line b2
line c3
line d4
line b2
line c3
line d4

line 6

    -  use /s
line 1
line 2
line 3

line 1
line 2
    -  use /str+ CR
line 1
line 2
    -  use /str+ CR
    - n get next match
    - N get prev match
# test file for vi 

to search:
    -  use /str+ CR
    - n get next match
    - N get prev match

o copy a block of lines:
    - mark initial posn
    - go to end of block
    - yank block

to paste
    - go to target
    - Paste the lines

to copy a block of lines:
    - mark initial posn

# test file for vi 
to search:
    -  use /str+ CR
    - n get next match
    - N get prev match

to copy a block of lines:
    - mark initial posn
    - go to end of block
 
# test file for vi 
to search:
    -  use /str+ CR
    - n get next match
    - N get prev match

to copy a block of lines:
    - mark initial posn
    - go to end of block
