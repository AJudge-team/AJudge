import unittest
import os
from pathlib import Path
from sandbox import Sandbox


class SandboxMethodTests(unittest.TestCase):
    def setUp(self):
        self.PROJECT_ROOT = (Path(__file__).parents[1]).resolve() # path to project root

    def test_constructor_parameter_is_empty_validation(self):
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

        self.assertEqual(test_str, str(result.get('Output'), 'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_exec_echo2(self):
        sandbox = Sandbox(54321)
        test_str = "World"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)

        self.assertEqual(test_str, str(result.get('Output'), 'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_exec_echo3(self):
        sandbox = Sandbox(54321)
        test_str = "a1234567999918"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)

        self.assertEqual(test_str, str(result.get('Output'), 'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_exec_echo4(self):
        sandbox = Sandbox(54321)
        test_str = "A-Judge Sandbox method test"
        test_cmd = "echo -n " + test_str
        result = sandbox.exec(test_cmd)

        self.assertEqual(test_str, str(result.get('Output'), 'utf-8'))
        self.assertEqual(0, result.get('ExitCode'))

    def test_copy_file_to_container_with_relative_path(self):
        sandbox = Sandbox(54321)

        with self.assertRaises(FileNotFoundError): # FIXME It's not proper exception
            sandbox.copy_file_to_sandbox('../tests/resources/server.py','/')

    def test_host_file_not_found(self):
        sandbox = Sandbox(54321)
        file_path = self.PROJECT_ROOT.joinpath('./resources/app.py')

        with self.assertRaises(FileNotFoundError):
            sandbox.copy_file_to_sandbox(file_path, '/')

    def test_copy_file_to_sandbox(self):
        sandbox = Sandbox(54321)
        file_path = self.PROJECT_ROOT.joinpath('./tests/resources/server.py')

        # copy
        result = sandbox.copy_file_to_sandbox(file_path, '/')
        self.assertTrue(result)

        # check existence
        result = sandbox.exec('[ -e "/server.py" ]')
        self.assertEqual(0, result.get('ExitCode'))

        # cehck contents
        result = sandbox.exec('cat /server.py')
        fileobj = open(file_path, "rb")
        file_contents = fileobj.read()
        fileobj.close()
        self.assertEqual(file_contents, result.get('Output'))


    def test_write_a_file_in_sandbox(self):
        sandbox = Sandbox(54321)
        file_contents = b"I want to write a file in sandbox"
        file_name = "write_file_test.txt"
        files = [(file_name, file_contents)]

        # copy
        result = sandbox.write_files_in_sandbox(files, '/')
        self.assertTrue(result)

        # check existence
        result = sandbox.exec('[ -e "/write_file_test.txt" ]')
        self.assertEqual(0, result.get('ExitCode'))

        # check contents
        result = sandbox.exec('cat /write_file_test.txt')
        self.assertEqual(file_contents, result.get('Output'))

    def test_get_files_from_sandbox(self):
        sandbox = Sandbox(54321)

        # get .py files under tests/resources/
        files = []
        resources_path = self.PROJECT_ROOT.joinpath('./tests/resources')
        for path in resources_path.glob('*.py'):
            file_obj = open(path, 'rb')
            files.append((path.name, file_obj.read()))
            file_obj.close()

        # make directory for them
        res = sandbox.exec('mkdir /workdir/test_copy')
        self.assertEqual(0, res.get('ExitCode'))

        # send them all
        res = sandbox.write_files_in_sandbox(files, '/workdir/test_copy')
        self.assertTrue(res)

        # get and check
        res = sandbox.get_files_from_sandbox('/workdir/test_copy/.')
        self.assertListEqual(files, res)
