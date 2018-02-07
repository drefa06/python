# A non blocking input #

## Goal ##

The classic input mode is:

under python 2:
```python
inputString = raw_input('Enter something: ')
```

under python 3:
```python
inputString = input('Enter something: ')
```

Both stayed blocked until something entered. This is not a problem for many of your case but imagine the following case:

- you have 2 threads asking user to enter some commands transfered to main programme. 
  => classic input is ok for that
- if one user enter a special command, e.g. 'start', both threads shall change their status and process something else.
  => this will work for the user thread where you enter the command but not for the 2nd one !!! 

That's why we sometime need to create an input that is not blocked until we enter something.

The other constraints are:
- use only standard library
- work on python 2 and 3
- work on multiple os

## basic solution ##

The basic solution is to use select and sys.stdin like:

```python
sys.stdout.write('Enter something: ')
sys.stdout.flush()
while not read:
    read, _, _ = select.select([sys.stdin], [], [], 1)

if read:
    inputString = read[0].readline()
```

Select poll over 3 lists: read, write and error.

We need to poll over read only and configure the read file to sys.stdin

Select use a timeout (here set to 1 sec) to interrupt the operation and continue, 
so we need to encapsulate the select in a while loop that will end only if something is read.











