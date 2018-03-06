# -*- coding: utf-8 -*-

""" This Module contains usefull and simple way to get local IP address.
    it works with builtins module only
"""
import os, re, sys
import subprocess

if (sys.version_info < (3, 0)):
    input = raw_input


# ===============================================================================================
def posixGetAddr(line):
    """get ip address from specific shell command result
    FOR POSIX OS ONLY

    :param line: line extracted by subprocess
    :return: the address found
    """
    m = re.match('(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)\s+(.*)\s+([\d\.]+)', line)
    if m:
        return m.group(7)
    else:
        return None


# ===============================================================================================
def ntGetAddr(line):
    """get ip address from specific shell command result
    FOR NT OS ONLY

    :param line: line extracted by subprocess
    :return: the address found
    """
    m = re.match('\d+\s+(\d+).(\d+).(\d+).(\d+)', line)
    if m:
        return '{}.{}.{}.{}'.format(m.group(1), m.group(2), m.group(3), m.group(4))
    else:
        return None

# ===============================================================================================
def askIP():
    """
    Demande et retourne l'adresse IP
    """
    correct = False
    while not correct:
        sys.stdout.write('Entrer votre addresse IP: ')
        sys.stdout.flush()
        addr = sys.stdin.readline()
        #addr = input('Entrer votre addresse IP: ')
        if re.match('(\d+).(\d+).(\d+).(\d+)', addr):
            correct = True
        else:
            print("    Wrong IPv4 format")

    return addr

# ===============================================================================================
def getLanIp():
    """get ip address from specific shell command result
    If OS is unknown or error happen => ask the IP to user

    :param line: line extracted by subprocess
    :return: the address found
    """
    addr = ""
    if os.name == 'nt':
        #set NT OS specific elements
        cmd = 'pathping -n -w 1 -h 1 -q 1 8.8.8.8'
        eol = '\r\n'
        getAddr = ntGetAddr

    elif os.name == 'posix':
        # set POSIX OS specific elements
        cmd = ['ip -4 route get 8.8.8.8 | head -n1']
        eol = '\n'
        getAddr = posixGetAddr

    else:
        # unknown OS
        cmd = None

    if cmd:
        try:
            #subprocess the specific command and analyse result
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (lines, err) = proc.communicate()
            for l in lines.decode('utf-8').strip().split(eol):
                if l.strip() == '': continue

                addr = getAddr(l.strip())
                if addr: break
        except:
            addr = askIP()

    else:
        addr = askIP()

    return addr

# ===============================================================================================
if __name__ == "__main__":
    #Cette partie permet d'appeller une fonction de ce module en ligne de commande: python lib/ip.py <fonction> [<arg> [<arg>] ... ]
    #c'est utilisé par les test pour le cas particulier de askIP pour simuler une entrée de commande par l'utilisateur
    import sys,time
    fct = locals()[sys.argv[1]]
    time.sleep(1)
    if len(sys.argv) >2:
        args=sys.argv[2:]
        ret = fct(*args)
    else:
        ret = fct()

    print('read: {}'.format(ret))