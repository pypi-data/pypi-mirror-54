# pylint:disable=line-too-long, protected-access
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.helpers.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.helpers import Command, Dict, Directory, File, Hash, Merge, Regex


class TestHash(TestCase):
    """
    Test PyFunceble.helpers.Hash
    """

    def setUp(self):
        """
        Setup everything needed for the tests.
        """

        self.file = "this_file_should_be_deleted"
        self.data_to_write = ["Hello World!", "Thanks for using PyFunceble"]

        self.expected_hashed = {
            "md5": "ba2e0e1774c2e60e2327f263402facd4",
            "sha1": "b5c8520cd2c422019997dc6fdbc9cb9d7002356e",
            "sha224": "863c46d5ed52b439da8f62a791e77c0cbbfb7d92af7c5549279f580d",
            "sha384": "6492f4b5732e0af4b9edf2c29ee4622c62ee418e5d6e0f34b13cb80560a28256c6e21e949119872d26d2327fc112a63b",  # pylint: disable=line-too-long
            "sha512": "f193ad6ee2cfbecd580225d8e6bfb9df1910e5ca6135b21b03ae208a007f71e9b57b55e299d27157551a18ef4dfdde23c96aaea796064846edc6cd25ac7eaf7f",  # pylint: disable=line-too-long
        }

    def testhash_data(self):
        """
       Test Hash._hash_data().
        """

        to_test = "\n".join(self.data_to_write)

        for algo, result in self.expected_hashed.items():
            self.assertEqual(
                result,
                Hash(algo=algo.upper()).data(to_test.encode()),
                msg="%s did not passed the test" % repr(algo),
            )

    def testhash_file(self):
        """
        Test Hash._hash_file().
        """

        expected = False
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)

        File(self.file).write("\n".join(self.data_to_write))
        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        for algo, result in self.expected_hashed.items():
            self.assertEqual(
                result,
                Hash(algo=algo.upper()).file(self.file),
                msg="%s did not passed the test" % repr(algo),
            )

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_get_path_not_exist(self):
        """
        Test Hash.get() for the case that the given file does
        not exist.
        """

        expected = False
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)

        expected = None
        actual = Hash().file(self.file)
        self.assertEqual(expected, actual)

    def test_get_specific_algo(self):
        """
        Test Hash.get() for the case that we want a specifig
        algorithm.
        """

        expected = False
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)

        File(self.file).write("\n".join(self.data_to_write))
        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        expected = self.expected_hashed["sha512"]
        actual = Hash(algo="sha512").file(self.file)
        self.assertEqual(expected, actual)

        expected = self.expected_hashed["sha512"]
        actual = Hash(algo="sha512").data("\n".join(self.data_to_write).encode())
        self.assertEqual(expected, actual)

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)


class TestCommand(TestCase):
    """
    Test PyFunceble.helpers.Command().
    """

    def test_command(self):
        """
        Test Command().execute().
        """

        expected = "PyFunceble has been written by Fun Ilrys."
        actual = Command("echo '%s'" % expected).execute()

        if PyFunceble.abstracts.Platform.is_windows():  # pragma: no cover
            self.assertEqual("'{}'\r\n".format(expected), actual)
        else:
            self.assertEqual("{}\n".format(expected), actual)

    def test_run(self):
        """
        Test Command().run().
        """

        expected = ["PyFunceble has been written by Fun Ilrys."]
        actual = list(Command("echo '%s'" % expected[0]).run())

        self.assertEqual(expected, actual)


class TestList(TestCase):
    """
    Test PyFunceble.helpers.List()
    """

    def setUp(self):
        """
        Setup everything needed for the tests.
        """

        self.main_list = ["hello", "world", 5, {"hello": "world"}, [1, 2, 3]]

    def test_merge(self):
        """
        Test List().merge().
        """

        to_merge = ["hello", "world", 5, {"world": "hello"}]
        expected = ["hello", "world", 5, {"hello": "world", "world": "hello"}]

        actual = Merge(to_merge).into(self.main_list)
        self.assertEqual(expected, actual)

        to_merge = ["hello", "world", 5, {"world": "hello"}]
        expected = [
            "hello",
            "world",
            5,
            {"hello": "world"},
            [1, 2, 3],
            {"world": "hello"},
        ]

        actual = Merge(to_merge).into(self.main_list, strict=False)
        self.assertEqual(expected, actual)

        to_merge = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]
        expected = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]

        actual = Merge(to_merge).into(self.main_list)
        self.assertEqual(expected, actual)

        to_merge = ["hello", "world", 5, {"hello": "you!"}, [1, 2, 4, 5]]
        expected = [
            "hello",
            "world",
            5,
            {"hello": "world"},
            [1, 2, 3],
            {"hello": "you!"},
            [1, 2, 4, 5],
        ]

        actual = Merge(to_merge).into(self.main_list, strict=False)
        self.assertEqual(expected, actual)


class TestDict(TestCase):
    """
    Test PyFunceble.helpers.Dict().
    """

    def setUp(self):
        """
        Setup everything needed for the tests.
        """

        self.to_test = {
            "Hello": "world",
            "World": {"world", "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
        }

    def test_has_same_keys_ask(self):
        """
        Test Dict().has_same_keys_as().
        """

        # This is a.
        origin = {"a": 1, "b": 1}

        # This is b.
        target = {"a": 1, "b": 2, "c": {"a": 1, "b": 3, "c": {"x": "x"}}}

        # We want to test that all keys of a are into b.
        self.assertEqual(True, Dict(target).has_same_keys_as(origin))
        # We want to test that all keys of b are into a.
        self.assertEqual(False, Dict(origin).has_same_keys_as(target))

        origin["c"] = {"a": 1, "b": 3, "c": {"x": "x"}}

        # We want to test that all keys of a are in b.
        self.assertEqual(True, Dict(target).has_same_keys_as(origin))
        # We want to test that all keys of b are in a.
        self.assertEqual(True, Dict(origin).has_same_keys_as(target))

        del origin["c"]["c"]
        # We want to test that all keys of b are in a.
        self.assertEqual(False, Dict(origin).has_same_keys_as(target))

    def test_remove_key_not_dict(self):
        """
        Test Dict().remove_key() for the case that a dict is not given.
        """

        expected = None
        actual = Dict(["Hello", "World!"]).remove_key("Py")

        self.assertEqual(expected, actual)

    def test_remove_key(self):
        """
        Test Dict().remove_key().
        """

        expected = {
            "Hello": "world",
            "World": {"world", "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "pyfunceble": ["funilrys"],
        }

        actual = Dict(self.to_test).remove_key("Py")

        self.assertEqual(expected, actual)

    def test_remove_keys(self):
        """
        Test Dict().remove_key().
        """

        expected = {"Hello": "world", "World": {"world", "hello"}}

        actual = Dict(self.to_test).remove_key(["pyfunceble", "Py", "funilrys"])

        self.assertEqual(expected, actual)

    def test_remove_key_not_found(self):
        """
        Test Dict().remove_key() for the case that
        the given key does not exist.
        """

        expected = {
            "Hello": "world",
            "World": {"world", "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
        }

        actual = Dict(self.to_test).remove_key("xxx")

        self.assertEqual(expected, actual)

    def test_rename_key_not_dict(self):
        """
        Test Dict().rename_key() for the case that no dict is
        given.
        """

        expected = None
        actual = Dict(self.to_test).rename_key(["Fun", "Ilrys"])

        self.assertEqual(expected, actual)

    def test_rename_key_single_strict(self):
        """
        Test Dict().rename_key() for the case that we want to
        rename only one key strictly.
        """

        expected = {
            "Hello": "world",
            "World": {"world", "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "PyFunceble": "Funceble",
            "pyfunceble": ["funilrys"],
        }

        actual = Dict(self.to_test).rename_key({"Py": "PyFunceble"})

        self.assertEqual(expected, actual)

    def test_rename_key_single_non_strict(self):
        """
        Test Dict().rename_key() for the case that we want to
        rename only one key insensitivly.
        """

        expected = {
            "Hello": "world",
            "World": {"world", "hello"},
            "nuilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "nuceble": ["funilrys"],
        }
        actual = Dict(self.to_test).rename_key({"fun": "nuf"}, strict=False)

        self.assertEqual(expected, actual)

    def test_to_yaml(self):
        """
        Test Dict().to_yaml.
        """

        file_to_read = "this_yaml_is_a_ghost.yaml"

        expected = False
        actual = PyFunceble.path.isfile(file_to_read)

        self.assertEqual(expected, actual)

        to_write = {"hello": ["This is PyFunceble!", "Uhh!"], "world": "Fun Ilrys"}

        expected = "{hello: [This is PyFunceble!, Uhh!], world: Fun Ilrys}\n"

        Dict(to_write).to_yaml_file(file_to_read, default_flow_style=True)

        expected = """hello:
- This is PyFunceble!
- Uhh!
world: Fun Ilrys
"""

        Dict(to_write).to_yaml_file(file_to_read, default_flow_style=False)

        actual = File(file_to_read).read()
        self.assertEqual(expected, actual)

        File(file_to_read).delete()

        expected = False
        actual = PyFunceble.path.isfile(file_to_read)

        self.assertEqual(expected, actual)

    def test_merge(self):
        """
        Test of Dict().merge().
        """

        origin = {
            "hello": ["This is PyFunceble!", "Uhh!"],
            "world": "Fun Ilrys",
            "hello_world": {"author": "funilrys", "name": "Fun"},
        }
        to_merge = {
            "hello": ["hello", "Uhh"],
            "hello_world": {"author": "nobody", "surname": "body"},
        }

        expected = {
            "hello": ["hello", "Uhh"],
            "world": "Fun Ilrys",
            "hello_world": {"author": "nobody", "name": "Fun", "surname": "body"},
        }
        actual = Merge(to_merge).into(origin, strict=True)

        self.assertEqual(expected, actual)

        expected = {
            "hello": ["This is PyFunceble!", "Uhh!", "hello", "Uhh"],
            "world": "Fun Ilrys",
            "hello_world": {"author": "nobody", "name": "Fun", "surname": "body"},
        }
        actual = Merge(to_merge).into(origin, strict=False)

        self.assertEqual(expected, actual)

    def test_merge_multilevel(self):
        """
        Test of Dict().merge() for the case that we have a multi level dict/list.
        """

        origin = {
            "hello": {"world": ["This is PyFunceble!", "Uhh!"]},
            "world": "Fun Ilrys",
            "hello_world": {"author": "funilrys", "name": "Fun"},
        }
        to_merge = {
            "hello": {"world": ["hello", "Uhh"]},
            "hello_world": {"author": "nobody", "surname": "body"},
        }

        expected = {
            "hello": {"world": ["hello", "Uhh"]},
            "world": "Fun Ilrys",
            "hello_world": {"author": "nobody", "name": "Fun", "surname": "body"},
        }
        actual = Merge(to_merge).into(origin, strict=True)

        self.assertEqual(expected, actual)

        expected = {
            "hello": {"world": ["This is PyFunceble!", "Uhh!", "hello", "Uhh"]},
            "world": "Fun Ilrys",
            "hello_world": {"author": "nobody", "name": "Fun", "surname": "body"},
        }
        actual = Merge(to_merge).into(origin, strict=False)

        self.assertEqual(expected, actual)


class TestDirectory(TestCase):
    """
    Test PyFunceble.helpers.Directory().
    """

    def test_fix_path(self):
        """
        Test Directory.fix_path().
        """

        expected = (
            "hello"
            + PyFunceble.directory_separator
            + "world"
            + PyFunceble.directory_separator
        )  # pylint: disable=line-too-long
        actual = Directory("/hello/world").fix_path()

        self.assertEqual(expected, actual)

        actual = Directory("\\hello\\world").fix_path()
        self.assertEqual(expected, actual)

        actual = Directory("hello\\world").fix_path()
        self.assertEqual(expected, actual)

        actual = Directory(r"hello\world").fix_path()
        self.assertEqual(expected, actual)

        actual = Directory(r"hello/world/").fix_path()
        self.assertEqual(expected, actual)

        to_test = ["", None, []]

        for element in to_test:
            actual = Directory(element).fix_path()
            self.assertEqual(element, actual)


class TestFile(TestCase):
    """
    Test PyFunceble.helpers.File()
    """

    def test_write_delete(self):
        """
        Test File.write() along with File.delete().
        """

        expected = "Hello, World! I'm domain2idna"
        File("hi").write(expected)

        with open("hi") as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = False
        File("hi").delete()
        actual = PyFunceble.path.isfile("hi")

        self.assertEqual(expected, actual)

    def test_write_overwrite_delete(self):
        """
        Test File.write() along with File.write() for the case that
        we want to overwrite the content of a file.
        """

        expected = "Hello, World! I'm domain2idna"
        File("hi").write(expected)

        with open("hi") as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = "Hello, World! Python is great, you should consider learning it!"
        File("hi").write(expected, overwrite=True)

        with open("hi") as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = False
        File("hi").delete()
        actual = PyFunceble.path.isfile("hi")

        self.assertEqual(expected, actual)

    def test_copy(self):
        """
        Test File.copy().
        """

        file_to_write = "hello_world"
        copy_destination = "world_hello"

        expected = False
        actual = PyFunceble.path.isfile(file_to_write)

        self.assertEqual(expected, actual)

        expected = "Hello, World! Python is great, you should consider learning it!"
        File(file_to_write).write(expected)

        with open(file_to_write) as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = False
        actual = PyFunceble.path.isfile(copy_destination)

        self.assertEqual(expected, actual)

        File(file_to_write).copy(copy_destination)

        expected = True
        actual = PyFunceble.path.isfile(copy_destination)

        self.assertEqual(expected, actual)

        expected = "Hello, World! Python is great, you should consider learning it!"

        with open(copy_destination) as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        File(copy_destination).delete()
        File(file_to_write).delete()
        expected = False
        actual = PyFunceble.path.isfile(copy_destination)

        self.assertEqual(expected, actual)

        actual = PyFunceble.path.isfile(file_to_write)

        self.assertEqual(expected, actual)

    def test_read_delete(self):
        """
        Test File.read() along with helpers.File.delete.
        """

        expected = "Hello, World! This has been written by Fun Ilrys."
        File("hi").write(expected)
        actual = File("hi").read()

        self.assertEqual(expected, actual)

        expected = False
        File("hi").delete()
        actual = PyFunceble.path.isfile("hi")

        self.assertEqual(expected, actual)


class TestRegex(TestCase):
    """
    Test Regex().
    """

    def setUp(self):
        """
        Setup everything needed for the tests.
        """

        self.data_list = [
            "hello",
            "world",
            "funilrys",
            "funceble",
            "PyFunceble",
            "pyfunceble",
        ]
        self.data = "Hello, this is Fun Ilrys. I just wanted to know how things goes around the tests."  # pylint: disable=line-too-long

    def test_not_matching_list(self):
        """
        Test Regex.not_matching_list().
        """

        regex = "fun"
        expected = ["hello", "world", "PyFunceble"]
        actual = Regex(regex).get_not_matching_list(self.data_list)

        self.assertEqual(expected, actual)

    def test_matching_list(self):
        """
        Test Regex.match_list().
        """

        regex = "fun"
        expected = ["funilrys", "funceble", "pyfunceble"]
        actual = Regex(regex).get_matching_list(self.data_list)

        self.assertEqual(expected, actual)

    def test_match_rematch(self):
        """
        Test Regex.match() for the case that we want to rematch the
        different groups.
        """

        regex = r"([a-z]{1,})\s([a-z]{1,})\s"
        expected = "is"
        actual = Regex(regex).match(self.data, rematch=True, group=1)

        self.assertEqual(expected, actual)

    def test_match_group(self):
        """
        Test Regex.match() for the case that we want a specific
        group.
        """

        regex = "e"
        expected = "e"
        actual = Regex(regex).match(self.data, group=0)

        self.assertEqual(expected, actual)

    def test_replace_no_replace_with(self):
        """
        Test Regex.replace() for the case than no replace
        with is given.
        """

        regex = "th"
        expected = self.data
        actual = Regex(regex).replace_match(self.data, None)

        self.assertEqual(expected, actual)

    def test_replace(self):
        """
        Test Regex.replace().
        """

        regex = "th"
        expected = "Hello, htis is Fun Ilrys. I just wanted to know how htings goes around hte tests."  # pylint: disable=line-too-long
        actual = Regex(regex).replace_match(self.data, "ht")

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
