import unittest
from sandbox import Sandbox

class SandboxMethodTests(unittest.TestCase):

    def test_exec_echo(self):
        sandbox = Sandbox()
        test_str = "Hello World"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)
        del sandbox
        self.assertEqual(test_str, str(result.get('Output'),'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_exec_echo2(self):
        sandbox = Sandbox()
        test_str = "World"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)
        del sandbox
        self.assertEqual(test_str, str(result.get('Output'), 'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_exec_echo3(self):
        sandbox = Sandbox()
        test_str = "a1234567999918"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)
        del sandbox
        self.assertEqual(test_str, str(result.get('Output'), 'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_exec_echo4(self):
        sandbox = Sandbox()
        test_str = "A-Judge Sandbox method test"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)
        del sandbox
        self.assertEqual(test_str, str(result.get('Output'), 'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))
