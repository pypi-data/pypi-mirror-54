import unittest
from sqlang.sql import SQL
import pymysql
import datetime

class BasicSQLTester(unittest.TestCase):

    def setUp(self):
        self.con = pymysql.connect(host='localhost', user='root', password='')
        self.cur = self.con.cursor()
        self.cur.execute("drop database if exists sqlang_test")
        self.cur.execute("create database sqlang_test")
        self.cur.execute("use sqlang_test;")
        self.cur.execute("create table meeting (uid char(36) not null, home char(3) not null, away char(3) not null, game_date date not null);")
        self.cur.execute("create table team (uid char(36) not null, name char(3) not null)")
        self.cur.execute("create table contacts (id char(36) not null, date_entered datetime not null, first_name char(50), last_name char(50))")
        self.cur.execute("create table contacts_cstm (id_c char(36) not null, a_unique_id_c char(15) not null)")

    def test_table(self):
        s = SQL()
        self.assertEqual(SQL.eval(SQL.TABLE('tbl')), 'tbl')

    def test_basic_select(self):
        s = SQL()
        expr = SQL.SELECT(
            SQL.FIELD('uid'),
            SQL.TABLE('meeting'),
            None, #joins
            SQL.WHERE(SQL.EQ(SQL.FIELD('home'), 'BOS')),
            None,
            None
        )
        self.cur.execute(s(expr))


        expr = SQL.SELECT(
            [SQL.FIELD('team.name'), SQL.COUNT(SQL.FIELD('meeting.uid'))],
            SQL.TABLE('meeting'),
            SQL.JOINS(
                SQL.JOIN(
                    SQL.TABLE('team'), 
                    SQL.AND(
                        SQL.EQ(SQL.FIELD('meeting.home'), SQL.FIELD('team.name')), 
                        SQL.GT('game_date', datetime.date(2014, 5, 10))
                    )
                )
            ),
            SQL.WHERE(SQL.NOT(SQL.LIKE(SQL.FIELD('team.uid'), '%PHI%'))),
            None,
            SQL.ORDER_BY(SQL.FIELD('meeting.uid'), 'desc')
        )

        self.cur.execute(s(expr))

    def test_access_of_table(self):
        s = SQL()
        t = SQL.ALIAS(SQL.TABLE('meeting'), 'm_tbl')

        expr = SQL.SELECT(
            t.uid,
            t,
            None, #joins
            SQL.WHERE(SQL.EQ(t.home, 'BOS')),
            None,
            None
        )
        self.cur.execute(s(expr))
        pass

    def test_multiplication_expansion(self):
        s = SQL()
        self.assertEqual(s.eval(SQL.FIELD('contacts.age')*45), "contacts.age * 45")

    def test_no_arg_items(self):
        s = SQL()
        self.assertEqual(s.eval(SQL.RAND()), 'RAND()')

    def test_advanced_update(self):
        s = SQL()
        c = SQL.TABLE('contacts')
        cc = SQL.TABLE('contacts_cstm')
        c2 = SQL.ALIAS(SQL.TABLE('contacts_cstm'), 'c2')
        expr = SQL.UPDATE(
                   c,
                   SQL.JOINS(
                           SQL.JOIN(cc, SQL.EQ(cc.id_c, c.id)),
                           SQL.LEFT_JOIN(c2, SQL.EQ(cc.id_c, c2.id_c))
                   ),
                   [SQL.EQ(
                       cc.a_unique_id_c, 
                       SQL.CONCAT(
                           SQL.UPPER(
                               SQL.IF(
                                   SQL.IN(SQL.SUBSTRING(c.last_name, 1, 3), ('', None, '.')),
                                   SQL.SUBSTRING(c.first_name, 1, 3),
                                   SQL.SUBSTRING(c.last_name, 1, 3)
                               ),
                            ),
                           SQL.IF(
                               SQL.NOT_NULL(c2.id_c),
                               SQL.UPPER(
                                   SQL.CONCAT(
                                       SQL.CHAR(SQL.ROUND((SQL.RAND()*25))+65),
                                       SQL.CHAR(SQL.ROUND((SQL.RAND()*25))+65),
                                       SQL.CHAR(SQL.ROUND((SQL.RAND()*25))+65)
                                   ),
                               ),
                               ''
                           ),
                           SQL.DATE_FORMAT(c.date_entered, '%m'),
                           SQL.DATE_FORMAT(c.date_entered, '%y')
                       )
                   )],
                   SQL.WHERE(
                       SQL.OR(
                           SQL.OR(
                               SQL.LIKE(cc.a_unique_id_c, '.0_/19'),
                               SQL.LIKE(cc.a_unique_id_c, '. 0_/19'),
                           ),
                           SQL.OR(
                               SQL.EQ(cc.a_unique_id_c, None),
                               SQL.EQ(SQL.LENGTH(SQL.TRIM(cc.a_unique_id_c)), 0)
                           )
                       )
                   ),
                   None,
                   None
        )
        self.cur.execute(s(expr))



                    
