import sqlite3

class WriteToDb():
   def __init__(self,database):
      self.cursore = sqlite3.connect(database).cursor()

   def write_events_to_db(self,events):
      # self.cursore.execute("CREATE TABLE Events(id INT, summary TEXT, start_date TEXT, end_date TEXT, location TEXT);")
      i=0
      for event in events:
         i+=1
         self.cursore.execute("INSERT INTO Events VALUES(?,?,?,?,?);",(i,str(event['summary']),str(event['start']),str(event['end']),str(event['location'])))

   def print_db(self):
      self.cursore.execute("SELECT * FROM Events")
      rows = self.cursore.fetchall()
      for row in rows:
         print row

# db = WriteToDb("test.db")
# db.write_events_to_db(CalendarEvents().get_events())
# db.print_db()
