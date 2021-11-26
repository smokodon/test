# encoding: utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#

from __future__ import absolute_import, division, unicode_literals

from unittest import TestCase

from mo_sql_parsing import parse_sqlserver as parse


class TestSqlServer(TestCase):
    def test_select_top_5(self):
        sql = """
        select	TOP (5)
            country_code,
            impact_code,
            impact_description,
            number_sites
        from	EUNIS.v1.BISE_Country_Threats_Pressures_Number_Sites
        order by number_sites desc
        """
        result = parse(sql)

        self.assertEqual(
            result,
            {
                "top": 5,
                "select": [
                    {"value": "country_code"},
                    {"value": "impact_code"},
                    {"value": "impact_description"},
                    {"value": "number_sites"},
                ],
                "from": "EUNIS.v1.BISE_Country_Threats_Pressures_Number_Sites",
                "orderby": {"value": "number_sites", "sort": "desc"},
            },
        )

    def test_issue13_top(self):
        # https://docs.microsoft.com/en-us/sql/t-sql/queries/top-transact-sql?view=sql-server-ver15
        sql = "SELECT TOP 3 * FROM Customers"
        result = parse(sql)
        self.assertEqual(result, {"top": 3, "select": "*", "from": "Customers",})

        sql = "SELECT TOP func(value) WITH TIES *"
        result = parse(sql)
        self.assertEqual(
            result, {"top": {"value": {"func": "value"}, "ties": True}, "select": "*"},
        )

        sql = "SELECT TOP 1 PERCENT WITH TIES *"
        result = parse(sql)
        self.assertEqual(
            result, {"top": {"percent": 1, "ties": True}, "select": "*"},
        )

        sql = "SELECT TOP a(b) PERCENT item"
        result = parse(sql)
        self.assertEqual(
            result, {"top": {"percent": {"a": "b"}}, "select": {"value": "item"}},
        )

        sql = "SELECT TOP a(b) PERCENT"
        with self.assertRaises(Exception):
            parse(sql)  # MISSING ANY COLUMN

    def test_issue143a(self):
        sql = "Select [A] from dual"
        result = parse(sql)
        expected = {"select": {"value": "A"}, "from": "dual"}
        self.assertEqual(result, expected)

    def test_issue143b(self):
        sql = "Select [A] from [dual]"
        result = parse(sql)
        expected = {"select": {"value": "A"}, "from": "dual"}
        self.assertEqual(result, expected)

    def test_issue143c(self):
        sql = "Select [A] from dual [T1]"
        result = parse(sql)
        expected = {"select": {"value": "A"}, "from": {"value": "dual", "name": "T1"}}
        self.assertEqual(result, expected)

    def test_issue143d_quote(self):
        sql = 'Select ["]'
        result = parse(sql)
        expected = {"select": {"value": '"'}}
        self.assertEqual(result, expected)

    def test_issue143e_close(self):
        sql = "Select []]]"
        result = parse(sql)
        expected = {"select": {"value": "]"}}
        self.assertEqual(result, expected)

