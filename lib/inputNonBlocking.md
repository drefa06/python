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

The basic solution is to use:
- select and sys.stdin for linux:

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


- msvcrt for windows:
```python
sys.stdout.write('Enter something: ')
sys.stdout.flush()
inputString=""
while msvcrt.kbhit():
    char = msvcrt.getche()
    #recupere chaque caractere, si '\r' est lu, placer la ligne dans la queue
    if char != '\r':
        inputString += char
    else:
        inputString = ""
        break
```

msvcrt get every char until a '\r' char is read. 
This is naturally a non blocking system.

## First Evolution ##

- Put the previous basic system in a thread.
- Command the polling by a threading event that permit to interrupt it from outside the thread.
- Use a queue to get the inputString

You obtain something like:
```python
# ===============================================================================================
class chkSysInput(threading.Thread):
    def __init__(self,qRead,interrupt,timeout=1):
	#init thread
	#get attribute qRead(reading queue), interrupt(threading event) and timeout

    def run(self):
        while not self.__interrupt.isSet():
            # tant que l'event n'est pas activé, controle sys.stdin pour linux ou n'importe quel charactere pour nt
            if os.name == 'nt':
                #windows polling with msvcrt
		self.qRead.put(inputString)

            else:
                #linux polling with select
		self.qRead.put(inputString)


# ===============================================================================================
class mngInput:
    def __init__(self,prompt):
        #init qRead (queue.Queue()), interruptEvent(threading.Event)
	#init thread (chkSysInput) as daemon

        sys.stdout.write(prompt)    #write prompt
        sys.stdout.flush()

    def interruptInput(self,*args, **kwargs):
        if self.threadRead.is_alive():
            # If thread is alive try to set the interrupt event
            try:
                self.interruptEvent.set()
            except threading.ThreadError as err:
                if str(err) == 'release unlocked lock':
                    #specific case of error: locker unlocked => ignore it
                    pass
                else:
                    #for other cases of error
                    raise threading.ThreadError(str(err))
        return True


    def getInput(self):
        text=None
        if not self.threadRead.is_alive():
            #If thread is not alive, clear the event and start the thread
            self.interruptEvent.clear()
            self.threadRead.start()

        else:
            #If thread is alive, check the queue.
            if not self.q_read.empty():
                #if queue is not empty, get the text and interrupt the thread.
                text = self.q_read.get()
                self.interruptInput()

        return text
```

And it's enough to work.
But you might manage to create the mngInput instance and be very carefull if you have several input in several thread in your script.

So here is my final evolution to manage this case.

## Final solution ##

- Create a module variable CIN init to None. This will contains the mngInput instance
- instanciate the mngInput class only when input is needed and protect it with a threading locker,
- delete the instance and re init CIN as None for the interrupt

The result is:
```python
CIN     = None			# Variable that will contains instance of mngInput
CINlock = threading.Lock()	# Locker to protect the CIN usage and access

# ===============================================================================================
def Input(prompt):
    global CIN
    #activate locker
    CINlock.acquire()

    #Instanciate mngInput if not already done
    if CIN == None:
        CIN = mngInput(prompt)

    #get Input
    val = CIN.getInput()

    #a line is read, interrupt the input and remove the instance
    if val != None:
        CIN.interruptInput()
        del CIN
        CIN=None
        val=-1

    #release locker
    CINlock.release()

    return val


# ===============================================================================================
def interruptInput(*args, **kwargs):
    global CIN
    val=None
    # activate locker
    CINlock.acquire()

    #if instance of mngInput exist, interrupt the input and remove the instance
    if CIN != None:
        CIN.interruptInput()
        del CIN
        CIN=None
        val=-1

    #release locker
    CINlock.release()

    return val
```

## usage ##

Do not forget it is a polling system !
So you need to include it in a loop.

example:
```python
#import Input and interruptInput
from inputNonBlocking import  Input,interruptInput,interruptEvent

def readInput(prompt,timeout=1000):
    startTime = time.time()
    while not interruptEvent:
        ret = Input(prompt)

        if ret:
            return ret
            break

        if time.time()-startTime > int(timeout):
            interruptInput()
            break

        time.sleep(0.1)
```

## test ##

### manual test ###

You can run:
```>python inputNonBlocking.py Input "Enter Something: " 10```

And you can try:
- enter a sentence before 10sec
- just return carriage before 10 sec
- enter nothing and wait 10sec
- enter nothing and CTRL+C before 10sec

### automatic test ###

under ../module_tests/lib, you will find test_inputNonBlocking.py

you can run ```python -m unittest module_tests.lib.test_inputNonBlocking```












