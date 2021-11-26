# encoding: utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#

from __future__ import absolute_import, division, unicode_literals

import json
from unittest import TestCase

from mo_sql_parsing import parse


class TestBigSql(TestCase):
    def test_issue_103b(self):
        #        0         1         2         3         4         5         6         7         8         9
        #        012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
        sql = """SELECT G.ITEM_ID AS "ITEM_ID", fn_get_dimension_by_grcom (H.BU_COD, G.ITEM_ID) AS "DESCRIPTION", trim(G.EAN11) "EANCODE", trim(DECODE (G.MATNR_ORIG_B2F, NULL, DECODE (G.MATNR_ORIG, NULL, G.MATNR, G.MATNR_ORIG), G.MATNR_ORIG_B2F)) AS "CODICE_PRODOTTO", DECODE (H.BRAND, 'BF GOODRICH', 'BFGOODRICH', H.BRAND) AS "BRAND_ID", H.BRAND AS "XBRAND", H.MARKET5 AS "MKT_ID", m.MC_COUNTRY_CODE AS "COUNTRY_CODE", H.BU_COD AS "GRCOM", H.DATE_FROM AS "PRICELIST_DATE", H.CURRENCY AS "CURRENCY_ID", K.CR_DESCRIPTION AS "CURRENCY_DESC", K.CR_DESCRIPTION AS "CURRENCY_SHORT_DESC", G.PATTERN AS "BTS_ID", P.PATTERN AS "PATTERN_SHORT_DESC", trim(G.SERIES) AS "SERIE", trim(G.WIDTH) AS "CORDA", trim(G.RIM) AS "CALETTAMENTO", G.STRUTTURA AS "STRUTTURA", DECODE (IS_NUMBER (G.WIDTH), 0, 0, TO_NUMBER (G.WIDTH)) AS "CORDA_NOM", DECODE (IS_NUMBER (G.SERIES), 0, 0, TO_NUMBER (G.SERIES)) AS "SERIE_NOM", 0 AS "STRUTTURA_NOM", DECODE (IS_NUMBER (G.RIM), 0, 0, TO_NUMBER (G.RIM)) AS "CALETTAMENTO_NOM", trim(G.LOADIN1) AS "LOAD_INDEX", trim(DECODE (TRIM (G.LOADIN2), '', NULL, TRIM (G.LOADIN2))) AS "LOAD_INDEX_1", trim(G.EXTRA_LOAD_FLAG) AS "EXTRA_LOAD_INDEX", G.RUNFLAT_FLAG AS "RUNFLAT_ID", DECODE (TRIM (G.OEMARK), '', NULL, TRIM (G.OEMARK)) AS "OE_MARK", trim(G.SPEEDIN1) AS "SPEED_INDEX", trim(DECODE (TRIM (G.SPEEDIN2), '', NULL, TRIM (G.SPEEDIN2))) AS "SPEED_INDEX_1", trim(G.CODE_MKS) AS "CODE_MKS", G.DESCR_MKS AS "MKS", D.PRICE AS "GROSS_PRICE", trim(fn_get_dimension_loadindex (g.item_id)) AS "DESCR_LOADINDEX", trim(fn_get_dimension_speedindex (g.item_id)) AS "DESCR_SPEEDINDEX", DECODE (TRIM (G.LOADIN1DB), '', NULL, TRIM (G.LOADIN1DB)) AS "LOADINDEX1DOUBLEMOUNT", DECODE (TRIM (G.LOADIN2DB), '', NULL, TRIM (G.LOADIN2DB)) AS "LOADINDEX2DOUBLEMOUNT", DECODE (TRIM (G.NOISECLASS), '', NULL, TRIM (G.NOISECLASS)) AS "NOISECLASS", DECODE (G.ARTICLEGROUPCODE, '01', 'Tyre', '02', 'Rim', NULL) AS "ARTICLEGROUP", G.ARTICLEGROUPCODE AS "ARTICLEGROUPCODE", DECODE (IS_NUMBER (G.DEPTH), 1, G.DEPTH, NULL) AS "ORIGINALTREADDEPTH", DECODE (IS_NUMBER (G.WEIGHT), 1, TO_NUMBER (G.WEIGHT) * 1000, NULL) AS "WEIGHT", DECODE (g.pncs, 'Yes', 1, 'No', 0, NULL) AS "PNCS", DECODE (g.sealind, 'Yes', 1, 'No', 0, NULL) AS "SELFSEALING", DECODE (g.sealind, 'Yes', g.RUNFLAT_FLAG_SEALIND, NULL) AS "SELFSEALINGINDICATOR", DECODE (g.extra_load, 'Yes', 1, 'No', 0, NULL) AS "EXTRA_LOAD", g.application_code AS "APPLICATION_CODE", NULL AS "PRODUCTSEGMENT", DECODE (g.application_code, 'F1', 'FittedUnitCar', 'F2', 'FittedUnitVan', 'F9', 'FittedUnitSuv', '01', 'Car', '02', 'Van', '03', 'Truck', '04', 'EM', '05', 'AS', '06', 'Industry', '08', 'Moto', '09', 'SUV', NULL) AS "APPLICATION", DECODE (g.SNOWFLAG, 'Yes', 1, 'No', 0, NULL) AS "SNOWFLAG", DECODE (g.RUNFLAT, 'Yes', 1, 'No', 0, NULL) AS "RUNFLAT", DECODE (TRIM (g.NOISE_PERFORMANCE), '', NULL, TRIM (G.NOISE_PERFORMANCE)) AS "NOISE_PERFORMANCE", DECODE (TRIM (g.rollres), '', NULL, TRIM (G.rollres)) AS "ROLLRES", DECODE (TRIM (g.wetgrip), '', NULL, TRIM (G.wetgrip)) AS "WETGRIP", g.MANUFACTURER AS "MANUFACTURER", DECODE (DECODE (IS_NUMBER (g.season), 1, TO_NUMBER (g.season), 0), 1, 'summer', 2, 'winter', 10, 'allseasons', NULL) AS "SEASONALITY" FROM DIM_CURRENCY k, P2_PATTERN_ALL p, P2_MATERIAL_ALL g, DW.DIM_MARKET_CHANNEL m, PRLST_DETAIL d, (SELECT H1.PRICELIST_ID, H1.BRAND, H1.BU_COD, H1.MARKET5, H1.DATE_FROM, H1.CURRENCY FROM PRCLST_HEADER h1, LOOKUP_BRAND b1 WHERE H1.ENABLE_VIEWING_B2F = 1 AND (H1.BRAND, H1.BU_COD, H1.MARKET5, H1.DATE_FROM) IN ( SELECT H2.BRAND, H2.BU_COD, H2.MARKET5, MAX (H2.DATE_FROM) FROM PRCLST_HEADER h2 WHERE H2.BU_COD = 'CAR' AND H2.ENABLE_VIEWING_B2F = 1 GROUP BY H2.BRAND, H2.BU_COD, H2.MARKET5) AND H1.BRAND = B1.BRAND) h WHERE h.currency = K.CR_COD_CURRENCY_SAP AND h.pricelist_id = D.PRICELIST_ID AND H.BRAND = G.BRCONA AND D.IPCODE = G.MATNR AND P.BRAND = G.BRCONA AND upper(P.PATTERN) = upper(G.PATTERN) AND h.market5 = m.MARKET_CHANNEL_CODE AND G.IS_USER = 1 AND (G.BRCONA, G.MATNR) NOT IN (SELECT C.BRCONA, C.MATNR FROM P2_MAT_USER_CONFLICTS c WHERE C.LAST_ACTION IN (21)) ORDER BY G.ITEM_ID"""
        result = parse(sql)
        expected = json.loads(
            """{"select": [{"value": "G.ITEM_ID", "name": "ITEM_ID"}, {"value": {"fn_get_dimension_by_grcom": ["H.BU_COD", "G.ITEM_ID"]}, "name": "DESCRIPTION"}, {"value": {"trim": "G.EAN11"}, "name": "EANCODE"}, {"value": {"trim": {"decode": ["G.MATNR_ORIG_B2F", {"null":{}}, {"decode": ["G.MATNR_ORIG", {"null":{}}, "G.MATNR", "G.MATNR_ORIG"]}, "G.MATNR_ORIG_B2F"]}}, "name": "CODICE_PRODOTTO"}, {"value": {"decode": ["H.BRAND", {"literal": "BF GOODRICH"}, {"literal": "BFGOODRICH"}, "H.BRAND"]}, "name": "BRAND_ID"}, {"value": "H.BRAND", "name": "XBRAND"}, {"value": "H.MARKET5", "name": "MKT_ID"}, {"value": "m.MC_COUNTRY_CODE", "name": "COUNTRY_CODE"}, {"value": "H.BU_COD", "name": "GRCOM"}, {"value": "H.DATE_FROM", "name": "PRICELIST_DATE"}, {"value": "H.CURRENCY", "name": "CURRENCY_ID"}, {"value": "K.CR_DESCRIPTION", "name": "CURRENCY_DESC"}, {"value": "K.CR_DESCRIPTION", "name": "CURRENCY_SHORT_DESC"}, {"value": "G.PATTERN", "name": "BTS_ID"}, {"value": "P.PATTERN", "name": "PATTERN_SHORT_DESC"}, {"value": {"trim": "G.SERIES"}, "name": "SERIE"}, {"value": {"trim": "G.WIDTH"}, "name": "CORDA"}, {"value": {"trim": "G.RIM"}, "name": "CALETTAMENTO"}, {"value": "G.STRUTTURA", "name": "STRUTTURA"}, {"value": {"decode": [{"is_number": "G.WIDTH"}, 0, 0, {"to_number": "G.WIDTH"}]}, "name": "CORDA_NOM"}, {"value": {"decode": [{"is_number": "G.SERIES"}, 0, 0, {"to_number": "G.SERIES"}]}, "name": "SERIE_NOM"}, {"value": 0, "name": "STRUTTURA_NOM"}, {"value": {"decode": [{"is_number": "G.RIM"}, 0, 0, {"to_number": "G.RIM"}]}, "name": "CALETTAMENTO_NOM"}, {"value": {"trim": "G.LOADIN1"}, "name": "LOAD_INDEX"}, {"value": {"trim": {"decode": [{"trim": "G.LOADIN2"}, {"literal": ""}, {"null":{}}, {"trim": "G.LOADIN2"}]}}, "name": "LOAD_INDEX_1"}, {"value": {"trim": "G.EXTRA_LOAD_FLAG"}, "name": "EXTRA_LOAD_INDEX"}, {"value": "G.RUNFLAT_FLAG", "name": "RUNFLAT_ID"}, {"value": {"decode": [{"trim": "G.OEMARK"}, {"literal": ""}, {"null":{}}, {"trim": "G.OEMARK"}]}, "name": "OE_MARK"}, {"value": {"trim": "G.SPEEDIN1"}, "name": "SPEED_INDEX"}, {"value": {"trim": {"decode": [{"trim": "G.SPEEDIN2"}, {"literal": ""}, {"null":{}}, {"trim": "G.SPEEDIN2"}]}}, "name": "SPEED_INDEX_1"}, {"value": {"trim": "G.CODE_MKS"}, "name": "CODE_MKS"}, {"value": "G.DESCR_MKS", "name": "MKS"}, {"value": "D.PRICE", "name": "GROSS_PRICE"}, {"value": {"trim": {"fn_get_dimension_loadindex": "g.item_id"}}, "name": "DESCR_LOADINDEX"}, {"value": {"trim": {"fn_get_dimension_speedindex": "g.item_id"}}, "name": "DESCR_SPEEDINDEX"}, {"value": {"decode": [{"trim": "G.LOADIN1DB"}, {"literal": ""}, {"null":{}}, {"trim": "G.LOADIN1DB"}]}, "name": "LOADINDEX1DOUBLEMOUNT"}, {"value": {"decode": [{"trim": "G.LOADIN2DB"}, {"literal": ""}, {"null":{}}, {"trim": "G.LOADIN2DB"}]}, "name": "LOADINDEX2DOUBLEMOUNT"}, {"value": {"decode": [{"trim": "G.NOISECLASS"}, {"literal": ""}, {"null":{}}, {"trim": "G.NOISECLASS"}]}, "name": "NOISECLASS"}, {"value": {"decode": ["G.ARTICLEGROUPCODE", {"literal": "01"}, {"literal": "Tyre"}, {"literal": "02"}, {"literal": "Rim"}, {"null":{}}]}, "name": "ARTICLEGROUP"}, {"value": "G.ARTICLEGROUPCODE", "name": "ARTICLEGROUPCODE"}, {"value": {"decode": [{"is_number": "G.DEPTH"}, 1, "G.DEPTH", {"null":{}}]}, "name": "ORIGINALTREADDEPTH"}, {"value": {"decode": [{"is_number": "G.WEIGHT"}, 1, {"mul": [{"to_number": "G.WEIGHT"}, 1000]}, {"null":{}}]}, "name": "WEIGHT"}, {"value": {"decode": ["g.pncs", {"literal": "Yes"}, 1, {"literal": "No"}, 0, {"null":{}}]}, "name": "PNCS"}, {"value": {"decode": ["g.sealind", {"literal": "Yes"}, 1, {"literal": "No"}, 0, {"null":{}}]}, "name": "SELFSEALING"}, {"value": {"decode": ["g.sealind", {"literal": "Yes"}, "g.RUNFLAT_FLAG_SEALIND", {"null":{}}]}, "name": "SELFSEALINGINDICATOR"}, {"value": {"decode": ["g.extra_load", {"literal": "Yes"}, 1, {"literal": "No"}, 0, {"null":{}}]}, "name": "EXTRA_LOAD"}, {"value": "g.application_code", "name": "APPLICATION_CODE"}, {"name": "PRODUCTSEGMENT", "value":{"null":{}}}, {"value": {"decode": ["g.application_code", {"literal": "F1"}, {"literal": "FittedUnitCar"}, {"literal": "F2"}, {"literal": "FittedUnitVan"}, {"literal": "F9"}, {"literal": "FittedUnitSuv"}, {"literal": "01"}, {"literal": "Car"}, {"literal": "02"}, {"literal": "Van"}, {"literal": "03"}, {"literal": "Truck"}, {"literal": "04"}, {"literal": "EM"}, {"literal": "05"}, {"literal": "AS"}, {"literal": "06"}, {"literal": "Industry"}, {"literal": "08"}, {"literal": "Moto"}, {"literal": "09"}, {"literal": "SUV"}, {"null":{}}]}, "name": "APPLICATION"}, {"value": {"decode": ["g.SNOWFLAG", {"literal": "Yes"}, 1, {"literal": "No"}, 0, {"null":{}}]}, "name": "SNOWFLAG"}, {"value": {"decode": ["g.RUNFLAT", {"literal": "Yes"}, 1, {"literal": "No"}, 0, {"null":{}}]}, "name": "RUNFLAT"}, {"value": {"decode": [{"trim": "g.NOISE_PERFORMANCE"}, {"literal": ""}, {"null":{}}, {"trim": "G.NOISE_PERFORMANCE"}]}, "name": "NOISE_PERFORMANCE"}, {"value": {"decode": [{"trim": "g.rollres"}, {"literal": ""}, {"null":{}}, {"trim": "G.rollres"}]}, "name": "ROLLRES"}, {"value": {"decode": [{"trim": "g.wetgrip"}, {"literal": ""}, {"null":{}}, {"trim": "G.wetgrip"}]}, "name": "WETGRIP"}, {"value": "g.MANUFACTURER", "name": "MANUFACTURER"}, {"value": {"decode": [{"decode": [{"is_number": "g.season"}, 1, {"to_number": "g.season"}, 0]}, 1, {"literal": "summer"}, 2, {"literal": "winter"}, 10, {"literal": "allseasons"}, {"null":{}}]}, "name": "SEASONALITY"}], "from": [{"value": "DIM_CURRENCY", "name": "k"}, {"value": "P2_PATTERN_ALL", "name": "p"}, {"value": "P2_MATERIAL_ALL", "name": "g"}, {"value": "DW.DIM_MARKET_CHANNEL", "name": "m"}, {"value": "PRLST_DETAIL", "name": "d"}, {"value": {"select": [{"value": "H1.PRICELIST_ID"}, {"value": "H1.BRAND"}, {"value": "H1.BU_COD"}, {"value": "H1.MARKET5"}, {"value": "H1.DATE_FROM"}, {"value": "H1.CURRENCY"}], "from": [{"value": "PRCLST_HEADER", "name": "h1"}, {"value": "LOOKUP_BRAND", "name": "b1"}], "where": {"and": [{"eq": ["H1.ENABLE_VIEWING_B2F", 1]}, {"in": [["H1.BRAND", "H1.BU_COD", "H1.MARKET5", "H1.DATE_FROM"], {"select": [{"value": "H2.BRAND"}, {"value": "H2.BU_COD"}, {"value": "H2.MARKET5"}, {"value": {"max": "H2.DATE_FROM"}}], "from": {"value": "PRCLST_HEADER", "name": "h2"}, "where": {"and": [{"eq": ["H2.BU_COD", {"literal": "CAR"}]}, {"eq": ["H2.ENABLE_VIEWING_B2F", 1]}]}, "groupby": [{"value": "H2.BRAND"}, {"value": "H2.BU_COD"}, {"value": "H2.MARKET5"}]}]}, {"eq": ["H1.BRAND", "B1.BRAND"]}]}}, "name": "h"}], "where": {"and": [{"eq": ["h.currency", "K.CR_COD_CURRENCY_SAP"]}, {"eq": ["h.pricelist_id", "D.PRICELIST_ID"]}, {"eq": ["H.BRAND", "G.BRCONA"]}, {"eq": ["D.IPCODE", "G.MATNR"]}, {"eq": ["P.BRAND", "G.BRCONA"]}, {"eq": [{"upper": "P.PATTERN"}, {"upper": "G.PATTERN"}]}, {"eq": ["h.market5", "m.MARKET_CHANNEL_CODE"]}, {"eq": ["G.IS_USER", 1]}, {"nin": [["G.BRCONA", "G.MATNR"], {"select": [{"value": "C.BRCONA"}, {"value": "C.MATNR"}], "from": {"value": "P2_MAT_USER_CONFLICTS", "name": "c"}, "where": {"in": ["C.LAST_ACTION", 21]}}]}]}, "orderby": {"value": "G.ITEM_ID"}}"""
        )
        self.assertEqual(result, expected)

    def test_issue_21_many_with_clauses(self):
        sql = """
            WITH ssr
            AS (
                SELECT s_store_id
                    ,sum(sales_price) AS sales
                    ,sum(profit) AS profit
                    ,sum(return_amt) AS
                RETURNS
                    ,sum(net_loss) AS profit_loss
                FROM (
                    SELECT ss_store_sk AS store_sk
                        ,ss_sold_date_sk AS date_sk
                        ,ss_ext_sales_price AS sales_price
                        ,ss_net_profit AS profit
                        ,cast(0 AS DECIMAL(7, 2)) AS return_amt
                        ,cast(0 AS DECIMAL(7, 2)) AS net_loss
                    FROM store_sales
                    
                    UNION ALL
                    
                    SELECT sr_store_sk AS store_sk
                        ,sr_returned_date_sk AS date_sk
                        ,cast(0 AS DECIMAL(7, 2)) AS sales_price
                        ,cast(0 AS DECIMAL(7, 2)) AS profit
                        ,sr_return_amt AS return_amt
                        ,sr_net_loss AS net_loss
                    FROM store_returns
                    ) salesreturns
                    ,date_dim
                    ,store
                WHERE date_sk = d_date_sk
                    AND d_date BETWEEN cast('1998-08-18' AS DATE)
                        AND dateadd(day, 14, cast('1998-08-18' AS DATE))
                    AND store_sk = s_store_sk
                GROUP BY s_store_id
                )
                ,csr
            AS (
                SELECT cp_catalog_page_id
                    ,sum(sales_price) AS sales
                    ,sum(profit) AS profit
                    ,sum(return_amt) AS
                RETURNS
                    ,sum(net_loss) AS profit_loss
                FROM (
                    SELECT cs_catalog_page_sk AS page_sk
                        ,cs_sold_date_sk AS date_sk
                        ,cs_ext_sales_price AS sales_price
                        ,cs_net_profit AS profit
                        ,cast(0 AS DECIMAL(7, 2)) AS return_amt
                        ,cast(0 AS DECIMAL(7, 2)) AS net_loss
                    FROM catalog_sales
                    
                    UNION ALL
                    
                    SELECT cr_catalog_page_sk AS page_sk
                        ,cr_returned_date_sk AS date_sk
                        ,cast(0 AS DECIMAL(7, 2)) AS sales_price
                        ,cast(0 AS DECIMAL(7, 2)) AS profit
                        ,cr_return_amount AS return_amt
                        ,cr_net_loss AS net_loss
                    FROM catalog_returns
                    ) salesreturns
                    ,date_dim
                    ,catalog_page
                WHERE date_sk = d_date_sk
                    AND d_date BETWEEN cast('1998-08-18' AS DATE)
                        AND dateadd(day, 14, cast('1998-08-18' AS DATE))
                    AND page_sk = cp_catalog_page_sk
                GROUP BY cp_catalog_page_id
                )
                ,wsr
            AS (
                SELECT web_site_id
                    ,sum(sales_price) AS sales
                    ,sum(profit) AS profit
                    ,sum(return_amt) AS
                RETURNS
                    ,sum(net_loss) AS profit_loss
                FROM (
                    SELECT ws_web_site_sk AS wsr_web_site_sk
                        ,ws_sold_date_sk AS date_sk
                        ,ws_ext_sales_price AS sales_price
                        ,ws_net_profit AS profit
                        ,cast(0 AS DECIMAL(7, 2)) AS return_amt
                        ,cast(0 AS DECIMAL(7, 2)) AS net_loss
                    FROM web_sales
                    
                    UNION ALL
                    
                    SELECT ws_web_site_sk AS wsr_web_site_sk
                        ,wr_returned_date_sk AS date_sk
                        ,cast(0 AS DECIMAL(7, 2)) AS sales_price
                        ,cast(0 AS DECIMAL(7, 2)) AS profit
                        ,wr_return_amt AS return_amt
                        ,wr_net_loss AS net_loss
                    FROM web_returns
                    LEFT OUTER JOIN web_sales ON (
                            wr_item_sk = ws_item_sk
                            AND wr_order_number = ws_order_number
                            )
                    ) salesreturns
                    ,date_dim
                    ,web_site
                WHERE date_sk = d_date_sk
                    AND d_date BETWEEN cast('1998-08-18' AS DATE)
                        AND dateadd(day, 14, cast('1998-08-18' AS DATE))
                    AND wsr_web_site_sk = web_site_sk
                GROUP BY web_site_id
                )
            SELECT channel
                ,id
                ,sum(sales) AS sales
                ,sum(RETURNS) AS
            RETURNS
                ,sum(profit) AS profit
            FROM (
                SELECT 'store channel' AS channel
                    ,'store' || s_store_id AS id
                    ,sales
                    ,
                RETURNS
                    ,(profit - profit_loss) AS profit
                FROM ssr
                
                UNION ALL
                
                SELECT 'catalog channel' AS channel
                    ,'catalog_page' || cp_catalog_page_id AS id
                    ,sales
                    ,
                RETURNS
                    ,(profit - profit_loss) AS profit
                FROM csr
                
                UNION ALL
                
                SELECT 'web channel' AS channel
                    ,'web_site' || web_site_id AS id
                    ,sales
                    ,
                RETURNS
                    ,(profit - profit_loss) AS profit
                FROM wsr
                ) x
            GROUP BY rollup(channel, id)
            ORDER BY channel
                ,id limit 100;    
        """

        result = parse(sql)
        expected = {
            "from": {
                "name": "x",
                "value": {"union_all": [
                    {
                        "from": "ssr",
                        "select": [
                            {"name": "channel", "value": {"literal": "store channel"}},
                            {
                                "name": "id",
                                "value": {"concat": [
                                    {"literal": "store"},
                                    "s_store_id",
                                ]},
                            },
                            {"value": "sales"},
                            {"value": "RETURNS"},
                            {
                                "name": "profit",
                                "value": {"sub": ["profit", "profit_loss"]},
                            },
                        ],
                    },
                    {
                        "from": "csr",
                        "select": [
                            {
                                "name": "channel",
                                "value": {"literal": "catalog channel"},
                            },
                            {
                                "name": "id",
                                "value": {"concat": [
                                    {"literal": "catalog_page"},
                                    "cp_catalog_page_id",
                                ]},
                            },
                            {"value": "sales"},
                            {"value": "RETURNS"},
                            {
                                "name": "profit",
                                "value": {"sub": ["profit", "profit_loss"]},
                            },
                        ],
                    },
                    {
                        "from": "wsr",
                        "select": [
                            {"name": "channel", "value": {"literal": "web channel"}},
                            {
                                "name": "id",
                                "value": {"concat": [
                                    {"literal": "web_site"},
                                    "web_site_id",
                                ]},
                            },
                            {"value": "sales"},
                            {"value": "RETURNS"},
                            {
                                "name": "profit",
                                "value": {"sub": ["profit", "profit_loss"]},
                            },
                        ],
                    },
                ]},
            },
            "groupby": {"value": {"rollup": ["channel", "id"]}},
            "limit": 100,
            "orderby": [{"value": "channel"}, {"value": "id"}],
            "select": [
                {"value": "channel"},
                {"value": "id"},
                {"name": "sales", "value": {"sum": "sales"}},
                {"name": "RETURNS", "value": {"sum": "RETURNS"}},
                {"name": "profit", "value": {"sum": "profit"}},
            ],
            "with": [
                {
                    "name": "ssr",
                    "value": {
                        "from": [
                            {
                                "name": "salesreturns",
                                "value": {"union_all": [
                                    {
                                        "from": "store_sales",
                                        "select": [
                                            {
                                                "name": "store_sk",
                                                "value": "ss_store_sk",
                                            },
                                            {
                                                "name": "date_sk",
                                                "value": "ss_sold_date_sk",
                                            },
                                            {
                                                "name": "sales_price",
                                                "value": "ss_ext_sales_price",
                                            },
                                            {
                                                "name": "profit",
                                                "value": "ss_net_profit",
                                            },
                                            {
                                                "name": "return_amt",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                            {
                                                "name": "net_loss",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                        ],
                                    },
                                    {
                                        "from": "store_returns",
                                        "select": [
                                            {
                                                "name": "store_sk",
                                                "value": "sr_store_sk",
                                            },
                                            {
                                                "name": "date_sk",
                                                "value": "sr_returned_date_sk",
                                            },
                                            {
                                                "name": "sales_price",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                            {
                                                "name": "profit",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                            {
                                                "name": "return_amt",
                                                "value": "sr_return_amt",
                                            },
                                            {
                                                "name": "net_loss",
                                                "value": "sr_net_loss",
                                            },
                                        ],
                                    },
                                ]},
                            },
                            "date_dim",
                            "store",
                        ],
                        "groupby": {"value": "s_store_id"},
                        "select": [
                            {"value": "s_store_id"},
                            {"name": "sales", "value": {"sum": "sales_price"}},
                            {"name": "profit", "value": {"sum": "profit"}},
                            {"name": "RETURNS", "value": {"sum": "return_amt"}},
                            {"name": "profit_loss", "value": {"sum": "net_loss"}},
                        ],
                        "where": {"and": [
                            {"eq": ["date_sk", "d_date_sk"]},
                            {"between": [
                                "d_date",
                                {"cast": [{"literal": "1998-08-18"}, {"date": {}}]},
                                {"dateadd": [
                                    "day",
                                    14,
                                    {"cast": [{"literal": "1998-08-18"}, {"date": {}}]},
                                ]},
                            ]},
                            {"eq": ["store_sk", "s_store_sk"]},
                        ]},
                    },
                },
                {
                    "name": "csr",
                    "value": {
                        "from": [
                            {
                                "name": "salesreturns",
                                "value": {"union_all": [
                                    {
                                        "from": "catalog_sales",
                                        "select": [
                                            {
                                                "name": "page_sk",
                                                "value": "cs_catalog_page_sk",
                                            },
                                            {
                                                "name": "date_sk",
                                                "value": "cs_sold_date_sk",
                                            },
                                            {
                                                "name": "sales_price",
                                                "value": "cs_ext_sales_price",
                                            },
                                            {
                                                "name": "profit",
                                                "value": "cs_net_profit",
                                            },
                                            {
                                                "name": "return_amt",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                            {
                                                "name": "net_loss",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                        ],
                                    },
                                    {
                                        "from": "catalog_returns",
                                        "select": [
                                            {
                                                "name": "page_sk",
                                                "value": "cr_catalog_page_sk",
                                            },
                                            {
                                                "name": "date_sk",
                                                "value": "cr_returned_date_sk",
                                            },
                                            {
                                                "name": "sales_price",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                            {
                                                "name": "profit",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                            {
                                                "name": "return_amt",
                                                "value": "cr_return_amount",
                                            },
                                            {
                                                "name": "net_loss",
                                                "value": "cr_net_loss",
                                            },
                                        ],
                                    },
                                ]},
                            },
                            "date_dim",
                            "catalog_page",
                        ],
                        "groupby": {"value": "cp_catalog_page_id"},
                        "select": [
                            {"value": "cp_catalog_page_id"},
                            {"name": "sales", "value": {"sum": "sales_price"}},
                            {"name": "profit", "value": {"sum": "profit"}},
                            {"name": "RETURNS", "value": {"sum": "return_amt"}},
                            {"name": "profit_loss", "value": {"sum": "net_loss"}},
                        ],
                        "where": {"and": [
                            {"eq": ["date_sk", "d_date_sk"]},
                            {"between": [
                                "d_date",
                                {"cast": [{"literal": "1998-08-18"}, {"date": {}}]},
                                {"dateadd": [
                                    "day",
                                    14,
                                    {"cast": [{"literal": "1998-08-18"}, {"date": {}}]},
                                ]},
                            ]},
                            {"eq": ["page_sk", "cp_catalog_page_sk"]},
                        ]},
                    },
                },
                {
                    "name": "wsr",
                    "value": {
                        "from": [
                            {
                                "name": "salesreturns",
                                "value": {"union_all": [
                                    {
                                        "from": "web_sales",
                                        "select": [
                                            {
                                                "name": "wsr_web_site_sk",
                                                "value": "ws_web_site_sk",
                                            },
                                            {
                                                "name": "date_sk",
                                                "value": "ws_sold_date_sk",
                                            },
                                            {
                                                "name": "sales_price",
                                                "value": "ws_ext_sales_price",
                                            },
                                            {
                                                "name": "profit",
                                                "value": "ws_net_profit",
                                            },
                                            {
                                                "name": "return_amt",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                            {
                                                "name": "net_loss",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                        ],
                                    },
                                    {
                                        "from": [
                                            "web_returns",
                                            {
                                                "left outer join": "web_sales",
                                                "on": {"and": [
                                                    {"eq": [
                                                        "wr_item_sk",
                                                        "ws_item_sk",
                                                    ]},
                                                    {"eq": [
                                                        "wr_order_number",
                                                        "ws_order_number",
                                                    ]},
                                                ]},
                                            },
                                        ],
                                        "select": [
                                            {
                                                "name": "wsr_web_site_sk",
                                                "value": "ws_web_site_sk",
                                            },
                                            {
                                                "name": "date_sk",
                                                "value": "wr_returned_date_sk",
                                            },
                                            {
                                                "name": "sales_price",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                            {
                                                "name": "profit",
                                                "value": {"cast": [
                                                    0,
                                                    {"decimal": [7, 2]},
                                                ]},
                                            },
                                            {
                                                "name": "return_amt",
                                                "value": "wr_return_amt",
                                            },
                                            {
                                                "name": "net_loss",
                                                "value": "wr_net_loss",
                                            },
                                        ],
                                    },
                                ]},
                            },
                            "date_dim",
                            "web_site",
                        ],
                        "groupby": {"value": "web_site_id"},
                        "select": [
                            {"value": "web_site_id"},
                            {"name": "sales", "value": {"sum": "sales_price"}},
                            {"name": "profit", "value": {"sum": "profit"}},
                            {"name": "RETURNS", "value": {"sum": "return_amt"}},
                            {"name": "profit_loss", "value": {"sum": "net_loss"}},
                        ],
                        "where": {"and": [
                            {"eq": ["date_sk", "d_date_sk"]},
                            {"between": [
                                "d_date",
                                {"cast": [{"literal": "1998-08-18"}, {"date": {}}]},
                                {"dateadd": [
                                    "day",
                                    14,
                                    {"cast": [{"literal": "1998-08-18"}, {"date": {}}]},
                                ]},
                            ]},
                            {"eq": ["wsr_web_site_sk", "web_site_sk"]},
                        ]},
                    },
                },
            ],
        }

        self.assertEqual(result, expected)
