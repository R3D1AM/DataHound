import sqlite3
import hashlib , os

def save_hash_to_db(Song_name, Song_hash):


    ''' Creates a database if one does not exist, adds an unique user and public key'''
    db_file_name = 'music_md5.db'
    db_file_location = ''

    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    # Insert a row of data
    c.execute('''CREATE TABLE IF NOT EXISTS Songs_hash_md5 (ID INTEGER PRIMARY KEY , Song_name text, Song_hash text)''')

    # run all the dictionary entries and save data in the database
    Song_name = Song_name
    Song_hash   = Song_hash

    c.execute("INSERT INTO Songs_hash_md5( Song_name, Song_hash) VALUES (?,?)", ( Song_name, Song_hash))

    conn.commit()
    #close the connection 
    # make sure any changes have been committed or they will be lost.
    conn.close()   



file_in_directory = os.listdir('music')

def file_as_bytes(file):
     with file:
         return file.read()

for file in file_in_directory:
     song_hash = (hashlib.md5(file_as_bytes(open('music/'+ file, 'rb'))).hexdigest())

     print (song_hash)

     save_hash_to_db(file, song_hash)



# for i in dic:
#    save_hash_to_db(i, dic[i])





# Code to print out the database
# def read2():

#      db_file_name = 'music_md5.db'
#      db_file_location = ''
#      conn = sqlite3.connect(db_file_location + db_file_name )
#      # select user table
#      cursor = conn.execute(f"SELECT * from Songs_hash_md5")
#      # check all the user

#      for row in cursor:
#          #print (row)
#          print('\n')
#          print(row)
#      conn.close()

# read2()

