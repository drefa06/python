# -*- coding: utf-8 -*-
import sys,os,time, re
import unittest
import threading,socket,select

if (sys.version_info < (3, 0)):
    import Queue as queue
else:
    import queue

if __name__ == "__main__":
    import __init__

from lib import threadCom
from lib import ip

class threadComTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    # =====================================================
    def test_0901_ThreadBroadcast(self):
        """
        test ThreadBroadcast before timeout
        :return:
        """

        #broadcast constant
        ipAddr = ip.getLanIp()
        broadcastAddr = '{}.255'.format(".".join(ipAddr.split('.')[0:3]))
        broadcast = (broadcastAddr, 12800)
        broadcastEvent = threading.Event()

        timeout = 5
        mapName = "map1.txt"

        #create broadcast server
        thBroadcast = threadCom.ThreadBroadcast(broadcast, broadcastEvent, timeout, mapName)
        thBroadcast.daemon = True
        thBroadcast.start()

        #broadcast server is running and alive
        time.sleep(1)
        self.assertTrue(thBroadcast.isAlive())

        #create broadcast client
        cnxClientBroadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cnxClientBroadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        #send "RQST;" to server
        req = "RQST;"
        cnxClientBroadcast.sendto(req.encode('utf-8'), broadcast)

        #get answer from server
        runningServers=()
        start = time.time()
        while time.time() - start < timeout:
            read, _, _ = select.select([cnxClientBroadcast], [], [], 1)
            if read:
                recv, addr = read[0].recvfrom(1024)
                recv = recv.decode('utf-8')
                if recv == 'RQST;':
                    pass
                elif recv.startswith('OK'):
                    runningServers = (addr, recv.split(':')[1], recv.split(':')[2].rstrip(';'))

        #if ok server shall return runningServers = ((<server addr>, <server port>),<server name>,<game map name>)
        self.assertTrue(isinstance(runningServers[0],tuple))
        m = re.match('(\d+).(\d+).(\d+).(\d+)',runningServers[0][0])
        self.assertTrue(m)
        self.assertEqual(12800,runningServers[0][1])
        self.assertEqual(socket.gethostname(),runningServers[1])
        self.assertEqual(mapName,runningServers[2])

        #go over server timeout and check it is no more alive
        time.sleep(5)
        self.assertFalse(thBroadcast.isAlive())


    # =====================================================
    def test_0902_ThreadBroadcast_timeout(self):
        """
        test ThreadBroadcast after timeout
        :return:
        """

        # broadcast constant
        ipAddr = ip.getLanIp()
        broadcastAddr = '{}.255'.format(".".join(ipAddr.split('.')[0:3]))
        broadcast = (broadcastAddr, 12800)
        broadcastEvent = threading.Event()

        timeout = 5
        mapName = "map1.txt"

        # create broadcast server
        thBroadcast = threadCom.ThreadBroadcast(broadcast, broadcastEvent, timeout, mapName)
        thBroadcast.daemon = True
        thBroadcast.start()

        # broadcast server is running and alive
        time.sleep(1)
        self.assertTrue(thBroadcast.isAlive())

        #simulate a server timeout
        time.sleep(5)
        self.assertFalse(thBroadcast.isAlive())

        # create broadcast client
        cnxClientBroadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cnxClientBroadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        req = "RQST;"
        cnxClientBroadcast.sendto(req.encode('utf-8'), broadcast)

        # get answer from server
        runningServers=()
        start = time.time()
        while time.time() - start < timeout:
            read, _, _ = select.select([cnxClientBroadcast], [], [], 1)
            if read:
                recv, addr = read[0].recvfrom(1024)
                recv = recv.decode('utf-8')
                if recv == 'RQST;':
                    pass
                elif recv.startswith('OK'):
                    runningServers = (addr, recv.split(':')[1], recv.split(':')[2].rstrip(';'))

        #nothing receive, no runningServers
        self.assertEqual((),runningServers)

    # =====================================================
    def test_0903_ThreadCom(self):

        #create server connection
        cnxServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cnxServer.bind(('localhost',12800))
        q_send = queue.Queue()
        q_receive = queue.Queue()

        #manage server cnx with ThreadCom
        thComServer = threadCom.ThreadCom(cnxServer, q_send, q_receive, "test_name")
        thComServer.daemon = True
        thComServer.start()

        time.sleep(1)

        #create client connection
        cnxClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cnxClient.connect(('localhost',12800))

        time.sleep(1)

        #TEST1: client send "TEST_RQST_1;"
        cnxClient.send("TEST_RQST_1;".encode('utf-8'))

        time.sleep(1)

        #get and test q_receive queue
        self.assertFalse(q_receive.empty())
        if not q_receive.empty():
            receive = q_receive.get()
            clientName, msg = receive.popitem()

            msg = msg.split('=')
            request = msg.pop(0)

        self.assertEqual("TEST_RQST_1",request)
        self.assertEqual("test_name",clientName)
        self.assertTrue(q_receive.empty())

        #TEST2: client send partials messages
        cnxClient.send("TEST_".encode('utf-8'))

        time.sleep(1)

        cnxClient.send("RQST_2; TEST_RQST_3; TEST_RQST".encode('utf-8'))

        time.sleep(1)
        self.assertFalse(q_receive.empty())
        if not q_receive.empty():
            receive = q_receive.get()
            clientName, msg = receive.popitem()

            msg = msg.split('=')
            request = msg.pop(0)

        self.assertEqual("TEST_RQST_2", request)
        self.assertEqual("test_name", clientName)
        self.assertFalse(q_receive.empty())
        if not q_receive.empty():
            receive = q_receive.get()
            clientName, msg = receive.popitem()

            msg = msg.split('=')
            request = msg.pop(0)
        self.assertEqual("TEST_RQST_3", request)
        self.assertEqual("test_name", clientName)

        #change prefix
        q_send.put("PREFIX=test_name_bis")
        time.sleep(0.5)

        cnxClient.send("_4;".encode('utf-8'))

        time.sleep(1)
        self.assertFalse(q_receive.empty())
        if not q_receive.empty():
            receive = q_receive.get()
            clientName, msg = receive.popitem()

            msg = msg.split('=')
            request = msg.pop(0)

        self.assertEqual("TEST_RQST_4", request)
        self.assertEqual("test_name_bis", clientName)

        #send msg to server
        msgToSend="the quick brown fox jump over the lazy duck"
        q_send.put(msgToSend+";")
        time.sleep(0.5)
        if not q_receive.empty():
            receive = q_receive.get()
            clientName, msg = receive.popitem()

            msg = msg.split('=')
            request = msg.pop(0)

        self.assertEqual(msgToSend, request)
        self.assertTrue(thComServer.isAlive())

        q_send.put("STOP")
        time.sleep(0.5)

        self.assertFalse(thComServer.isAlive())












if __name__ == "__main__":
    unittest.main()