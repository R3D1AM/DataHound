
import os
import sys
import math
import wave
import py7zr 
import struct
import getopt
import hashlib 
import sqlite3
import zipfile
from shutil import copyfile
from tabulate import tabulate



def file_finder(sound_path, bits_to_recover):

    audio_file  	= wave.open( 'original_copy/' + sound_path , "r" )    
    channel_number 	= audio_file.getnchannels()
    bit_depth	 	= audio_file.getsampwidth()
    frames_number   = audio_file.getnframes()
    samples_number 	= frames_number * channel_number

    if ( bit_depth	== 1 ):  
    	# When audio files are 8-bit integers (unsigned)
        fmt = "{}B".format(samples_number)
        # Sets the least significant bits_to_recover bits of an integer to zero
        mask = (1 << 8) - (1 << 2)
        smallest_byte = -(1 << 8)
    elif (bit_depth	 == 2):  
        # When audio files are 16-bit integers (signed)
        fmt = "{}h".format(samples_number)
        # Sets the least significant bits_to_recover bits of an integer to zero
        mask = (1 << 15) - (1 << 2)
        # The least possible value for an audio
        smallest_byte = -(1 << 15)
    else:
        # Python's wave module doesn't support higher sample widths
        raise ValueError("File has an unsupported bit-depth")


    # Creats a list of all audio files
    raw_data = list(struct.unpack(fmt, audio_file.readframes(frames_number)))
    # Extracts the least significant bits_to_recover bits of an integer
    mask = (1 << 2) - 1
    
    data = bytearray()
    sound_index = 0 
    buffer = 0
    buffer_length = 0
    audio_file.close()

    while (bits_to_recover > 0):
        
        next_sample = raw_data[sound_index]
        if (next_sample != smallest_byte):
            buffer += (abs(next_sample) & mask) << buffer_length
            buffer_length += 2
        sound_index += 1
        
        while (buffer_length >= 8 and bits_to_recover > 0):
            # If there is more than a byte in the buffer, add it to data
            # and decrease the number of bytes left to recover.
            current_data = buffer % (1 << 8)
            buffer >>= 8
            buffer_length -= 8
            data += struct.pack('1B', current_data)
            bits_to_recover -= 1

    header = data.decode('utf-8',  errors="ignore")
    

    a =  (data.hex())
    signature = '' 

    #print (c)
    n =0
    for i in a:
        signature += i

        if n == 6:
            break
        n+= 1

    print (signature)

    if signature == '89504e4':

        with open(f'extracted/{sound_path}.png', "wb+") as file:
            file.write(bytes(data))

        print ('\tPNG document?')

        file = 'png'

    elif signature == '377abca':

        with open(f'extracted/{sound_path}.7z', "wb+") as file:
            file.write(bytes(data))

        print ('\t7z document?')

        file = '7z'

        print ('\n\tArchive file found, trying extraction')
        extract(f'extracted/{sound_path}.7z')

    elif signature == '504b030' :

        if 'word' in header:
            with open(f'extracted/{sound_path}.docx', "wb+") as file:
                file.write(bytes(data))

            print ('\tWord document?')

            file = 'docx'
          
        else:
            with open(f'extracted/{sound_path}.zip', "wb+") as file:
                file.write(bytes(data))

            print ('\tZip document?')

            file = 'zip'

            extract_zip(f'extracted/{sound_path}.zip')

    else:
        file = '??'

        print ( '\n\tNo match')
        return

    print(f"\tData recovered as '{sound_path}.{file}' File")


def hash_md5(file):

    with open(file, 'rb') as f:
        a = f.read()
        
        a = hashlib.md5(a)
        a = a.hexdigest()
        return (a)


def extract(file_name, password=''):    
    try:
        with py7zr.SevenZipFile(file_name , mode='r',password=password) as z: 
            z.extractall('extracted/') 
            print ('\n\tFile extracted')

    except Exception as e :
        #print (f'Error -> {e}')

        if str(e) == 'Password is required for extracting given archive.':
            print ('\n\tFile password protected')
            print ('\n\tBrute force it?')

        elif str(e) == 'invalid block data':
            print ('\n\tFile password protected')
            print ('\n\tBrute force it?')

        user_choose = ''

        while user_choose not in ('n','y','quit'):
            user_choose = input('\n\tTry to brute force it? (y/n/quit)\n')
            if user_choose == 'quit':
                exit()
            elif user_choose == 'n':
                return
            elif user_choose == 'y':
                with open("wordlist/rockyou.txt") as file_in:
                    print
                    lines = []
                    for line in file_in:
                        print (f'\tTrying password -> {line.strip()}') 
                        try:
                            with py7zr.SevenZipFile(file_name , mode='r',password=line.strip()) as z: 
                                z.extractall('extracted/') 
                                
                                print (f'\n\tPassword Found\n\n\t{line.strip()}')

                                print ('\n\tFile extracted')

                                return

                        except :
                            pass


def extract_zip(file, pwd=''):
    print
    print (file)
    print
    try:
        with zipfile.ZipFile(file, 'r') as zip_ref:

            zip_ref.extractall( pwd = bytes(pwd,'utf-8'))
    except Exception as e:
        print (e)

        if str(e) == "File <ZipInfo filename='asdasdasd.pub' compress_type=deflate external_attr=0x2020 file_size=59904 compress_size=4482> is encrypted, password required for extraction":
            print ('the zip file is password protected')


def read_song_hash_db():

	try:

	    db_file_name = 'db/music_md5.db'
	    db_file_location = ''
	    conn = sqlite3.connect(db_file_location + db_file_name )
	    # select user table
	    cursor = conn.execute(f"SELECT * from Songs_hash_md5")
	    print('\tSong database:\n')

	    keys = 'N', 'Title', 'md5'
	    pdtabulate=lambda df:tabulate(df,headers=keys,tablefmt='grid',numalign="center",stralign='center')

	    lista = []
	    for row in cursor:
	        lista.append(row)
	    conn.close()

	    print (pdtabulate(lista))

	    return True

	except Exception as e :

		
		

		if str(e) == 'unable to open database file' :
			print ('Hashes databases not found')
		else:
			print (e)


		return False



def compare_songs_in_the_db(song_title, song_hash):

    db_file_name = 'db/music_md5.db'
    db_file_location = ''
    conn = sqlite3.connect(db_file_location + db_file_name )
    # select user table
    cursor = conn.execute(f"SELECT * from Songs_hash_md5")
    # check all the users
   
    for row in cursor:
        if song_title == row[1] :
            print ('\tSong title present in the database')

            if song_hash == row[2]:
                    print ('\n\tMD5 hash match (File unmodified)')

                    return True

            print ('\n\tMD5 hash do not match (possible hidden file)')
            return False

    conn.close()
    print ('\n\tSong not present in the database')
    return None


if __name__ == '__main__':  

    
    # intro message
    print ('\n\nWelcome to the Data Hound....\n\n')

    # Print the database
    if read_song_hash_db() :
	    # loading the file in the original directory
	    file_in_directory = os.listdir('original')
	    print (f'\n\t{len(file_in_directory)} Files found in the original directory\n')
	    # loop through the files
	    print ('\n\tCreating a copy of the files')
	    for file in file_in_directory:
	        # copy the file in original copy folder
	        copyfile('original/'+ file, 'original_copy/' + file)

	    print ('\tFiles Copied to original_copy directory')

	    print ('\n\tStarting analysis on copied versions of the files')

	    # load the file in the original copy folder
	    file_in_directory = os.listdir('original_copy')
	    # List the present files
	    # print ( file_in_directory)
	    # loop throught the file in the original copy folder
	    file_n = 0
	    for file in file_in_directory:

	        print ('-' * 75)
	        file_n+=1
	        # display the name of the file
	        print(f'\n\tFile {file_n}) {file}\n')
	        # print the hash of the file

	        
	        song_hash = hash_md5("original_copy/" + file )

	        result = compare_songs_in_the_db(file, song_hash)

	        if result != True:

	            print (f'\thash : {song_hash}' )
	            
	            # Try to recover data from the file
	            file_finder( file, 171553 )

print ('\n\n\tData Hound has finished analysing the files\n\n')

