# encoding: utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#

from __future__ import absolute_import, division, unicode_literals

from unittest import TestCase

from mo_sql_parsing import parse_mysql


class TestMySql(TestCase):
    def test_issue_22(self):
        sql = 'SELECT "fred"'
        result = parse_mysql(sql)
        expected = {"select": {"value": {"literal": "fred"}}}
        self.assertEqual(result, expected)
