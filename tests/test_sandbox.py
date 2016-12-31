import unittest
import os
from sandbox import Sandbox


class SandboxMethodTests(unittest.TestCase):

    def test_constructor_parameter_is_empty_validation1(self):
        with self.assertRaises(Exception):
            sandbox = Sandbox()

    def test_constructor(self):
        sandbox = Sandbox(54321)
        if sandbox is None:
            self.assertTrue(False)

    def test_exec_echo(self):
        sandbox = Sandbox(54321)
        test_str = "Hello World"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)
        del sandbox
        self.assertEqual(test_str, str(result.get('Output'),'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_exec_echo2(self):
        sandbox = Sandbox(54321)
        test_str = "World"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)
        del sandbox
        self.assertEqual(test_str, str(result.get('Output'), 'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_exec_echo3(self):
        sandbox = Sandbox(54321)
        test_str = "a1234567999918"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)
        del sandbox
        self.assertEqual(test_str, str(result.get('Output'), 'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_exec_echo4(self):
        sandbox = Sandbox(54321)
        test_str = "A-Judge Sandbox method test"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)
        del sandbox
        self.assertEqual(test_str, str(result.get('Output'), 'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_copy_file_to_container(self):
        sandbox = Sandbox(54321)
        sandbox.copy_file_to_container("../tests/resources/server.py", "/")
        result = sandbox.exec('[ -e "/server.py" ]')
        del sandbox
        self.assertEqual(0, result.get('ExitCode'))

    def test_copy_bytes_to_container(self):
        sandbox = Sandbox(54321)
        data = "data"
        data = str.encode(data)
        sandbox.copy_bytes_to_container(data, "/", "generated.dat")
        result = sandbox.exec('[ -e "/generated.dat" ]')
        del sandbox
        self.assertEqual(0, result.get('ExitCode'))

    def test_send_data_and_receive_data(self):
        sandbox = Sandbox(54321)
        snd = sandbox.copy_file_to_container("../tests/resources/server.py", "/")
        snd = snd["Bytes"]
        result = sandbox.exec("cat /server.py")
        del sandbox
        self.assertEqual(0, result.get('ExitCode'))
        rcv = result['Output']
        self.assertEqual(snd, rcv)
