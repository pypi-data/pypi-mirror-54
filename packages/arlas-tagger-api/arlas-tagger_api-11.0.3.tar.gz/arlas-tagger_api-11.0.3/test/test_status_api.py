# coding: utf-8

"""
    ARLAS Tagger API

    (Un)Tag fields of ARLAS collections

    OpenAPI spec version: 11.0.3
    Contact: contact@gisaia.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest

import arlas_tagger_api_python
from arlas_tagger_api_python.rest import ApiException
from arlas_tagger_api_python.apis.status_api import StatusApi


class TestStatusApi(unittest.TestCase):
    """ StatusApi unit test stubs """

    def setUp(self):
        self.api = arlas_tagger_api_python.apis.status_api.StatusApi()

    def tearDown(self):
        pass

    def test_tagging_get(self):
        """
        Test case for tagging_get

        TagStatus
        """
        pass


if __name__ == '__main__':
    unittest.main()
