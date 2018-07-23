# -*- coding: utf-8 -*-
import sys,os, time
import unittest
import subprocess


if __name__ == "__main__":
    import __init__

import server, client

class serverTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        if self.bg.poll() is None:
            self.bg.kill()


    # =====================================================
    def test_1101_stop_at_init(self):
        self.bg = subprocess.Popen(['python', 'roboc.py', '-s', '-m', os.path.join(os.getcwd(),"tests","test_map", 'map1.txt')], \
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        time.sleep(1)

        #create client
        obj1 = client.Client('test')
        self.assertTrue(obj1.connect())

        #check 1st reception
        msg = obj1.receiveFromServer(2)
        self.assertTrue('PlayerName' in msg)
        obj1.sendToServer("Player=test;")
        msg = obj1.receiveFromServer(2)
        self.assertIsNone(msg)
        obj1.sendToServer("PlayerName=test;")
        msg = obj1.receiveFromServer(2)
        self.assertEqual(6, len(msg))
        self.assertTrue('ACK PlayerName=' in msg[0])
        self.assertTrue('SETUP_DIR=' in msg[1])
        self.assertTrue('SETUP_ACT=' in msg[2])
        self.assertTrue('SETUP_OBJ=' in msg[3])
        self.assertTrue('SETUP_END' in msg[4])
        self.assertTrue('ASK=READY' in msg[5])

        obj1.sendToServer("END=test;")
        msg = obj1.receiveFromServer(2)
        self.assertIsNone(msg)
        self.assertTrue(obj1._Client__thCom.isAlive())
        obj1.sendToServer("STOP")
        time.sleep(0.5)
        self.assertFalse(obj1._Client__thCom.isAlive())
        del obj1


    # =====================================================
    def test_1102_stop_at_game(self):
        self.bg = subprocess.Popen(
            ['python', 'roboc.py', '-s', '-m', os.path.join(os.getcwd(), "tests", "test_map", 'map1.txt')], \
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        time.sleep(1)

        # create client
        obj1 = client.Client('test')
        self.assertTrue(obj1.connect())

        # check 1st reception
        msg = obj1.receiveFromServer(2)
        self.assertTrue('PlayerName' in msg)
        obj1.sendToServer("PlayerName=test;")
        msg = obj1.receiveFromServer(2)
        self.assertEqual(6, len(msg))
        self.assertTrue('ACK PlayerName=' in msg[0])
        self.assertTrue('ASK=READY' in msg[5])

        obj1.sendToServer("START;")
        msg = obj1.receiveFromServer(2)
        self.assertEqual(2, len(msg))
        self.assertTrue(msg[0].startswith('MAP='))
        self.assertTrue('ASK=GAME' in msg[1])

        obj1.close()
        del obj1

    # =====================================================
    def test_1103_multiple_client_stop_start(self):
        self.bg = subprocess.Popen(
            ['python', 'roboc.py', '-s','-m', os.path.join(os.getcwd(), "cartes", '01-facile.txt')], \
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        time.sleep(1)
        print(self.bg.poll())

        # create 3 clients
        obj1 = client.Client('test')
        self.assertTrue(obj1.connect())
        msg1 = obj1.receiveFromServer(2)
        self.assertTrue('PlayerName' in msg1)

        obj2 = client.Client('test')
        self.assertTrue(obj2.connect())
        msg2 = obj2.receiveFromServer(2)
        self.assertTrue('PlayerName' in msg2)

        obj3 = client.Client('test')
        self.assertTrue(obj3.connect())
        msg3 = obj3.receiveFromServer(2)
        self.assertTrue('PlayerName' in msg3)

        # init obj3
        obj3.sendToServer("PlayerName=test;")
        msg3 = obj3.receiveFromServer(2)
        self.assertEqual(6, len(msg3))
        self.assertTrue('ACK PlayerName=' in msg3[0])
        self.assertTrue('ASK=READY' in msg3[5])

        # init obj1
        obj1.sendToServer("PlayerName=test;")
        msg1 = obj1.receiveFromServer(2)
        self.assertEqual(6, len(msg1))
        self.assertTrue('ACK PlayerName=' in msg1[0])
        self.assertTrue('ASK=READY' in msg1[5])

        # init obj2
        obj2.sendToServer("PlayerName=test;")
        msg2 = obj2.receiveFromServer(2)
        self.assertEqual(6, len(msg2))
        self.assertTrue('ACK PlayerName=' in msg2[0])
        self.assertTrue('ASK=READY' in msg2[5])

        #obj2 quit
        obj2.close()
        del obj2

        #obj3 start game
        obj3.sendToServer("START;")
        msg3 = obj3.receiveFromServer(2)
        self.assertEqual(1, len(msg3))
        self.assertTrue(msg3[0].startswith('MAP='))

        msg1 = obj1.receiveFromServer(2)
        self.assertEqual(3, len(msg1))
        self.assertTrue(msg1[0].startswith('START'))
        self.assertTrue(msg1[1].startswith('MAP='))
        self.assertTrue('ASK=GAME' in msg1[2])

        # obj1 quit
        obj1.close()
        del obj1

        # obj3 can continue alone
        obj3.sendToServer("CMD_DIR=S:2;")
        msg3 = obj3.receiveFromServer(2)
        self.assertTrue('ASK=GAME' in msg3)

        # obj1 quit
        obj3.close()
        del obj3

        st = time.time()
        while self.bg.poll() is None:
            time.sleep(0.1)
        print('Server Closed {}sec after last client'.format(time.time()-st))
        self.assertIsNotNone(self.bg.poll())

    # =====================================================
    def test_1104_move(self):
        self.bg = subprocess.Popen(
            ['python', 'roboc.py', '-s', '-m', os.path.join(os.getcwd(), "tests", "test_map", 'map1.txt')], \
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        time.sleep(1)

        # create client
        obj1 = client.Client('test')
        self.assertTrue(obj1.connect())

        # check 1st reception
        msg = obj1.receiveFromServer(2)
        self.assertTrue('PlayerName' in msg)
        obj1.sendToServer("PlayerName=test;")
        msg = obj1.receiveFromServer(2)
        self.assertEqual(6, len(msg))
        self.assertTrue('ACK PlayerName=' in msg[0])
        self.assertTrue('ASK=READY' in msg[5])

        #start game
        obj1.sendToServer("START;")
        msg = obj1.receiveFromServer(2)
        self.assertEqual(2, len(msg))
        self.assertTrue(msg[0].startswith('MAP='))
        self.assertTrue('ASK=GAME' in msg[1])

        # wrong move
        obj1.sendToServer("CMD_DIR=N:1;")
        msg = obj1.receiveFromServer(2)
        self.assertEqual(2, len(msg))
        self.assertTrue(msg[0].startswith('ERROR='))
        self.assertTrue('ASK=GAME' in msg[1])

        # wrong move
        obj1.sendToServer("CMD_DIR=B:1;")
        msg = obj1.receiveFromServer(2)
        self.assertEqual(2, len(msg))
        self.assertTrue(msg[0].startswith('ERROR='))
        self.assertTrue('ASK=GAME' in msg[1])

        # wrong move
        obj1.sendToServer("CMD_DIR=A:A;")
        msg = obj1.receiveFromServer(2)
        self.assertEqual(2, len(msg))
        self.assertTrue(msg[0].startswith('ERROR='))
        self.assertTrue('ASK=GAME' in msg[1])

        # wrong move
        obj1.sendToServer("CMD_DIR=Z:123;")
        msg = obj1.receiveFromServer(2)
        self.assertEqual(2, len(msg))
        self.assertTrue(msg[0].startswith('ERROR='))
        self.assertTrue('ASK=GAME' in msg[1])

        # wrong move
        obj1.sendToServer("CMD_DIR=S:2;")
        msg = obj1.receiveFromServer(2)
        self.assertEqual(2, len(msg))
        self.assertTrue(msg[0].startswith('MAP='))
        self.assertTrue('ASK=GAME' in msg[1])

        obj1.close()
        del obj1





if __name__ == "__main__":
    unittest.main()