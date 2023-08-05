# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will test PyFunceble.http_code.

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
import unittest.mock as mock  # pylint: disable=useless-import-alias
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.http_code import HTTPCode


class TestHTTPCode(TestCase):
    """
    Test PyFunceble.http_code.
    """

    def setUp(self):
        """
        Setup everything needed for the tests.
        """
        PyFunceble.load_config(generate_directory_structure=False)

        self.subject = "google.com"
        self.subject_type = "domain"

    @mock.patch("PyFunceble.http_code.HTTPCode._access")
    def test_get_not_activated(self, _):
        """
        Test if HTTPCode().get() does not have a launch
        authorization.
        """

        PyFunceble.HTTP_CODE.active = False
        expected = PyFunceble.HTTP_CODE.not_found_default
        actual = HTTPCode(self.subject, self.subject_type).get()

        self.assertEqual(expected, actual)

    @mock.patch("PyFunceble.http_code.HTTPCode._access")
    def test_get_known_code(self, access):
        """
        Test of HTTPCode().get() for the case that
        it match a code which is in our list.
        """

        PyFunceble.HTTP_CODE.active = True

        access.return_value = 200
        expected = 200
        actual = HTTPCode(self.subject, self.subject_type).get()

        self.assertEqual(expected, actual)

    @mock.patch("PyFunceble.http_code.HTTPCode._access")
    def test_get_unknown_code(self, access):
        """
        Test of HTTPCode().get() for the case that
        it match a code which is not in our list.
        """

        PyFunceble.HTTP_CODE.active = True

        access.return_value = 859
        expected = PyFunceble.HTTP_CODE.not_found_default
        actual = HTTPCode(self.subject, self.subject_type).get()

        self.assertEqual(expected, actual)

    @mock.patch("PyFunceble.http_code.HTTPCode._access")
    def test_get_code_is_none(self, access):
        """
        Test of HTTPCode().get() for the case that
        it match a code which is not in our list.
        """

        PyFunceble.HTTP_CODE.active = True

        access.return_value = None
        expected = PyFunceble.HTTP_CODE.not_found_default
        actual = HTTPCode(self.subject, self.subject_type).get()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
