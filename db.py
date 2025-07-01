import sqlite3

def create_table():
  conn = sqlite3.connect('photo.db')
  cursor = conn.cursor()
  cursor.execute('''
CREATE TABLE IF NOT EXISTS photo(
  tshirt TEXT    
)
''')
  conn.commit()
  conn.close()

def save_photo(file_id):
  conn = sqlite3.connect('photo.db')
  cursor = conn.cursor()
  cursor.execute('INSERT INTO photo VALUES (?)', (file_id,))
  conn.commit()
  conn.close()

def exist_photo(thirt):
  conn= sqlite3.connect('photo.db')
  cursor = conn.cursor()
  cursor.execute('''SELECT tshirt FROM photo WHERE tshirt = ?''', (thirt,))
  th = cursor.fetchall()
  conn.close()
  if th is None:
    return 'Не добавлено фото'
  else:
    return th[0]

def get_photo():
  conn = sqlite3.connect('photo.db')
  cursor = conn.cursor()
  cursor.execute('''SELECT tshirt FROM photo''')
  tshirt = cursor.fetchall()
  return tshirt 
  