# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#

from __future__ import absolute_import, division, unicode_literals

from unittest import TestCase

from mo_parsing.debug import Debugger

from mo_sql_parsing import parse


class TestCreateSimple(TestCase):
    maxDiff = None

    def test_one_column(self):
        result = parse("create table student (name varchar2)")
        expected = {"create table": {
            "name": "student",
            "columns": {"name": "name", "type": {"varchar2": {}}},
        }}
        self.assertEqual(result, expected)

    def test_two_columns(self):
        result = parse("create table student (name varchar2, rollno int)")
        expected = {"create table": {
            "name": "student",
            "columns": [
                {"name": "name", "type": {"varchar2": {}}},
                {"name": "rollno", "type": {"int": {}}},
            ],
        }}
        self.assertEqual(result, expected)

    def test_three_columns(self):
        result = parse(
            "create table customers (id name, name varchar, salary decimal )"
        )
        expected = {"create table": {
            "name": "customers",
            "columns": [
                {"name": "id", "type": "name"},
                {"name": "name", "type": {"varchar": {}}},
                {"name": "salary", "type": {"decimal": {}}},
            ],
        }}
        self.assertEqual(result, expected)

    def test_four_columns(self):
        result = parse(
            "create table customers( id int, name varchar, address char, salary"
            " decimal)"
        )
        expected = {"create table": {
            "name": "customers",
            "columns": [
                {"name": "id", "type": {"int": {}}},
                {"name": "name", "type": {"varchar": {}}},
                {"name": "address", "type": {"char": {}}},
                {"name": "salary", "type": {"decimal": {}}},
            ],
        }}
        self.assertEqual(result, expected)

    def test_five_columns(self):
        result = parse(
            "create table persons ( PersonID int, LastName varchar, FirstName varchar,"
            " Address varchar, City varchar)"
        )
        expected = {"create table": {
            "name": "persons",
            "columns": [
                {"name": "PersonID", "type": {"int": {}}},
                {"name": "LastName", "type": {"varchar": {}}},
                {"name": "FirstName", "type": {"varchar": {}}},
                {"name": "Address", "type": {"varchar": {}}},
                {"name": "City", "type": {"varchar": {}}},
            ],
        }}
        self.assertEqual(result, expected)

    def test_two_columns_with_size(self):
        result = parse("create table student (name varchar2(25), rollno int(2))")
        expected = {"create table": {
            "name": "student",
            "columns": [
                {"name": "name", "type": {"varchar2": 25}},
                {"name": "rollno", "type": {"int": 2}},
            ],
        }}
        self.assertEqual(result, expected)

    def test_five_columns_with_size(self):
        result = parse(
            "create table persons ( PersonID int(2), LastName varchar(10), FirstName"
            " varchar(10), Address varchar(50), City varchar(10))"
        )
        expected = {"create table": {
            "name": "persons",
            "columns": [
                {"name": "PersonID", "type": {"int": 2}},
                {"name": "LastName", "type": {"varchar": 10}},
                {"name": "FirstName", "type": {"varchar": 10}},
                {"name": "Address", "type": {"varchar": 50}},
                {"name": "City", "type": {"varchar": 10}},
            ],
        }}
        self.assertEqual(result, expected)

    def test_one_columns_with_size(self):
        result = parse("create table student (name varchar not null)")
        expected = {"create table": {
            "columns": {"name": "name", "nullable": False, "type": {"varchar": {}}},
            "name": "student",
        }}
        self.assertEqual(result, expected)

    def test_one_columns_with_size2(self):
        result = parse("create table student (name decimal(2,3) not null)")
        expected = {"create table": {
            "columns": {"name": "name", "nullable": False, "type": {"decimal": [2, 3]}},
            "name": "student",
        }}
        self.assertEqual(result, expected)


class TestWithOption(TestCase):
    def test_not_null(self):
        result = parse(
            "create table student (name varchar not null, sunny int primary key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {"name": "name", "type": {"varchar": {}}, "nullable": False},
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_null(self):
        # NULL mean ＮULLABLE in MySQL
        result = parse(
            "create table student (name varchar null, sunny int primary key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {"name": "name", "type": {"varchar": {}}, "nullable": True},
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_unique(self):
        result = parse(
            "create table student (name varchar unique, sunny int primary key)"
        )
        expected = {"create table": {
            "columns": [
                {"name": "name", "type": {"varchar": {}}, "unique": True},
                {"name": "sunny", "primary_key": True, "type": {"int": {}}},
            ],
            "name": "student",
        }}
        self.assertEqual(result, expected)

    def test_primary_key(self):
        result = parse(
            "create table student (name varchar primary key, sunny int primary key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {"name": "name", "type": {"varchar": {}}, "primary_key": True},
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_reference(self):
        result = parse(
            "create table student (name varchar REFERENCES person (colname), sunny int"
            " primary key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {
                    "name": "name",
                    "type": {"varchar": {}},
                    "references": {"table": "person", "columns": "colname"},
                },
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_reference_composite(self):
        result = parse(
            "create table student (name varchar REFERENCES person(colname, colname2),"
            " sunny int primary key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {
                    "name": "name",
                    "type": {"varchar": {}},
                    "references": {
                        "table": "person",
                        "columns": ["colname", "colname2"],
                    },
                },
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_check(self):
        result = parse(
            "create table student (name varchar check ( length(name)<10 ) , sunny int"
            " primary key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {
                    "name": "name",
                    "type": {"varchar": {}},
                    "check": {"lt": [{"length": "name"}, 10]},
                },
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_default_null_value(self):
        result = parse(
            "create table student (name varchar default null, sunny int primary key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {"name": "name", "type": {"varchar": {}}, "default": {"null": {}},},
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_default_null_literal(self):
        result = parse(
            "create table student (name varchar default 'null', sunny int primary key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {
                    "name": "name",
                    "type": {"varchar": {}},
                    "default": {"literal": "null"},
                },
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_default_value(self):
        result = parse(
            "create table student (name varchar default 'text', sunny int primary key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {
                    "name": "name",
                    "type": {"varchar": {}},
                    "default": {"literal": "text"},
                },
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_default_expr(self):
        result = parse(
            "create table student (name varchar default (ex * 2) , sunny int primary"
            " key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {
                    "name": "name",
                    "type": {"varchar": {}},
                    "default": {"mul": ["ex", 2]},
                },
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_index(self):
        result = parse(
            "create table student (name varchar default (ex * 2) , sunny int primary"
            " key)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {
                    "name": "name",
                    "type": {"varchar": {}},
                    "default": {"mul": ["ex", 2]},
                },
                {"name": "sunny", "type": {"int": {}}, "primary_key": True},
            ],
        }}
        self.assertEqual(result, expected)

    def test_complexy(self):
        result = parse(
            "create table student (name varchar not null primary key default (ex * 2) ,"
            " sunny int primary key)"
        )
        expected = {"create table": {
            "columns": [
                {
                    "default": {"mul": ["ex", 2]},
                    "name": "name",
                    "nullable": False,
                    "primary_key": True,
                    "type": {"varchar": {}},
                },
                {"name": "sunny", "primary_key": True, "type": {"int": {}}},
            ],
            "name": "student",
        }}
        self.assertEqual(result, expected)


class TestTableConstraint(TestCase):
    def test_primary_key(self):
        result = parse(
            "create table student (name varchar not null, primary key( name ) )"
        )
        expected = {"create table": {
            "name": "student",
            "columns": {"name": "name", "type": {"varchar": {}}, "nullable": False},
            "constraint": {"primary_key": {"columns": "name"}},
        }}
        self.assertEqual(result, expected)

    def test_primary_key_composite(self):
        result = parse(
            "create table student (name varchar not null, id varchar not null, primary"
            " key( name, id ) )"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {"name": "name", "type": {"varchar": {}}, "nullable": False},
                {"name": "id", "type": {"varchar": {}}, "nullable": False},
            ],
            "constraint": {"primary_key": {"columns": ["name", "id"]}},
        }}
        self.assertEqual(result, expected)

    def test_constraint(self):
        result = parse(
            "create table student (name varchar null, constraint c_00 primary"
            " key(name))"
        )
        expected = {"create table": {
            "name": "student",
            "columns": {"name": "name", "type": {"varchar": {}}, "nullable": True},
            "constraint": {"name": "c_00", "primary_key": {"columns": "name"}},
        }}
        self.assertEqual(result, expected)

    def test_unique(self):
        result = parse(
            "create table student (name varchar, unique unique_student(name) )"
        )
        expected = {"create table": {
            "name": "student",
            "columns": {"name": "name", "type": {"varchar": {}}},
            "constraint": {"index": {
                "name": "unique_student",
                "columns": "name",
                "unique": True,
            }},
        }}
        self.assertEqual(result, expected)

    def test_unique_composite(self):
        result = parse(
            "create table student (name varchar not null, id varchar not null, unique"
            " key unique_student(name, id) )"
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {"name": "name", "type": {"varchar": {}}, "nullable": False},
                {"name": "id", "type": {"varchar": {}}, "nullable": False},
            ],
            "constraint": {"index": {
                "name": "unique_student",
                "columns": ["name", "id"],
                "unique": True,
            }},
        }}
        self.assertEqual(result, expected)

    def test_reference(self):
        result = parse(
            "create table student (name varchar, "
            "foreign key frn_student(name) references person (colname) )"
        )
        expected = {"create table": {
            "name": "student",
            "columns": {"name": "name", "type": {"varchar": {}}},
            "constraint": {"foreign_key": {
                "index_name": "frn_student",
                "columns": "name",
                "references": {"table": "person", "columns": "colname"},
            }},
        }}
        self.assertEqual(result, expected)

    def test_reference_composite(self):
        result = parse(
            """
            create table student (
                name varchar not null, 
                id varchar not null, 
                foreign key frn_student(name, id) references person (colname, pid)  
            )
        """
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {"name": "name", "type": {"varchar": {}}, "nullable": False},
                {"name": "id", "type": {"varchar": {}}, "nullable": False},
            ],
            "constraint": {"foreign_key": {
                "index_name": "frn_student",
                "columns": ["name", "id"],
                "references": {"table": "person", "columns": ["colname", "pid"]},
            }},
        }}
        self.assertEqual(result, expected)

    def test_2_foreign_key(self):
        result = parse(
            """
            create table student (
                name varchar not null, 
                id varchar not null, 
                foreign key frn_student(name, id) references person (colname, pid),
                foreign key Z(name, id) references B(colname, pid)  
            )
        """
        )
        expected = {"create table": {
            "name": "student",
            "columns": [
                {"name": "name", "type": {"varchar": {}}, "nullable": False},
                {"name": "id", "type": {"varchar": {}}, "nullable": False},
            ],
            "constraint": [
                {"foreign_key": {
                    "index_name": "frn_student",
                    "columns": ["name", "id"],
                    "references": {"table": "person", "columns": ["colname", "pid"]},
                }},
                {"foreign_key": {
                    "index_name": "Z",
                    "columns": ["name", "id"],
                    "references": {"table": "B", "columns": ["colname", "pid"]},
                }},
            ],
        }}
        self.assertEqual(result, expected)

    def test_check(self):
        result = parse(
            "create table student (name varchar, "
            "constraint chk_01 check (name like '%Doe') )"
        )
        expected = {"create table": {
            "name": "student",
            "columns": {"name": "name", "type": {"varchar": {}}},
            "constraint": {
                "name": "chk_01",
                "check": {"like": ["name", {"literal": "%Doe"}]},
            },
        }}
        self.assertEqual(result, expected)

    def test_2_constraints(self):
        result = parse(
            """create table student (
            name varchar, 
            constraint chk_01 check (name like '%Doe'), 
            constraint chk_02 check (A = 0) 
            )
        """
        )
        expected = {"create table": {
            "name": "student",
            "columns": {"name": "name", "type": {"varchar": {}}},
            "constraint": [
                {"name": "chk_01", "check": {"like": ["name", {"literal": "%Doe"}]},},
                {"name": "chk_02", "check": {"eq": ["A", 0]},},
            ],
        }}
        self.assertEqual(result, expected)


class TestCreateSelect(TestCase):
    def test_select(self):
        result = parse("create table student as select * from XYZZY, ABC")
        expected = {"create table": {
            "name": "student",
            "query": {"select": "*", "from": ["XYZZY", "ABC"]},
        }}
        self.assertEqual(result, expected)

    def test_paren_select(self):
        result = parse("create table student as ( select * from XYZZY )")
        expected = {"create table": {
            "name": "student",
            "query": {"select": "*", "from": "XYZZY"},
        }}
        self.assertEqual(result, expected)

    def test_with_select(self):
        result = parse(
            "create table student as with t as ( select * from XYZZY ) select * from t"
        )
        expected = {"create table": {
            "name": "student",
            "query": {
                "select": "*",
                "from": "t",
                "with": {"name": "t", "value": {"select": "*", "from": "XYZZY"}},
            },
        }}
        self.assertEqual(result, expected)


class TestCreateForBigQuery(TestCase):
    def test_struct_nested_one_column(self):
        result = parse("create table student (name struct<first_name varchar>)")
        expected = {"create table": {
            "name": "student",
            "columns": {
                "name": "name",
                "type": {"struct": {"name": "first_name", "type": {"varchar": {}}}},
            },
        }}

        self.assertEqual(result, expected)

    def test_struct_nested_many_column(self):
        result = parse(
            "create table student (name struct<first_name varchar, middle_name char(1),"
            " last_name varchar>)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": {
                "name": "name",
                "type": {"struct": [
                    {"name": "first_name", "type": {"varchar": {}}},
                    {"name": "middle_name", "type": {"char": 1}},
                    {"name": "last_name", "type": {"varchar": {}}},
                ]},
            },
        }}

        self.assertEqual(result, expected)

    def test_array_nested(self):
        result = parse("create table student (name array<varchar>)")
        expected = {"create table": {
            "name": "student",
            "columns": {"name": "name", "type": {"array": {"varchar": {}}}},
        }}
        self.assertEqual(result, expected)

    def test_array_nested_array(self):
        # Not supported this case in BigQuery. but, allow.
        result = parse("create table student (name array<array<int>>)")
        expected = {"create table": {
            "name": "student",
            "columns": {"name": "name", "type": {"array": {"array": {"int": {}}}}},
        }}
        self.assertEqual(result, expected)

    def test_array_nested_struct_array(self):
        # Not supported this case in BigQuery. but, allow.
        result = parse("create table student (name array<struct<child array<int>>>)")
        expected = {"create table": {
            "name": "student",
            "columns": {
                "name": "name",
                "type": {"array": {"struct": {
                    "name": "child",
                    "type": {"array": {"int": {}}},
                }}},
            },
        }}
        self.assertEqual(result, expected)

    def test_array_nested_struct(self):
        result = parse(
            "create table student (name array<struct<chr nchar, is_valid boolean>>)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": {
                "name": "name",
                "type": {"array": {"struct": [
                    {"name": "chr", "type": {"nchar": {}}},
                    {"name": "is_valid", "type": {"boolean": {}}},
                ]}},
            },
        }}
        self.assertEqual(result, expected)

    def test_struct_nested_array(self):
        result = parse(
            "create table student (name struct<chr array<nchar>, is_valid"
            " array<boolean>>)"
        )
        expected = {"create table": {
            "name": "student",
            "columns": {
                "name": "name",
                "type": {"struct": [
                    {"name": "chr", "type": {"array": {"nchar": {}}}},
                    {"name": "is_valid", "type": {"array": {"boolean": {}}}},
                ]},
            },
        }}
        self.assertEqual(result, expected)

    def test_timestamp_column(self):
        sql = """        
            CREATE TABLE u (
                id UUID DEFAULT uuid_generate_v4(),
                email VARCHAR(256) UNIQUE NOT NULL,
                is_boolean BOOLEAN DEFAULT False,
                t TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id)
            )
        """
        result = parse(sql)
        expected = {"create table": {
            "columns": [
                {
                    "default": {"uuid_generate_v4": {}},
                    "name": "id",
                    "type": {"uuid": {}},
                },
                {
                    "name": "email",
                    "nullable": False,
                    "type": {"varchar": 256},
                    "unique": True,
                },
                {"default": False, "name": "is_boolean", "type": {"boolean": {}}},
                {
                    "default": "CURRENT_TIMESTAMP",
                    "name": "t",
                    "type": {"timestamp_with_time_zone": {}},
                },
            ],
            "constraint": {"primary_key": {"columns": "id"}},
            "name": "u",
        }}

        self.assertEqual(result, expected)

    def test_create_index(self):
        sql = """
            CREATE INDEX a ON u USING btree (e);
        """
        result = parse(sql)
        expected = {"create index": {
            "columns": "e",
            "name": "a",
            "table": "u",
            "using": "btree",
        }}
        self.assertEqual(result, expected)
