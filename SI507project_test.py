import sqlite3
import unittest

class HW5SQLiteDBTests(unittest.TestCase):
  def setUp(self):
    self.conn = sqlite3.connect("college_majors.sqlite") # Connecting to database that should exist in autograder
    self.cur = self.conn.cursor()
    
  def test_for_majors_table(self):
    self.cur.execute("select majorcode, name, majorcategory, allunemployment, recentunemployment from majors where majorcode = '1100'")
    data = self.cur.fetchone()
    self.assertEqual(data,('1100', 'GENERAL AGRICULTURE', 'Agriculture & Natural Resources', 0.026147106, 0.019642463), "Testing data that results from selecting country 1100")
  
