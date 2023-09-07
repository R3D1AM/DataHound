import hashlib , os

# using data from the folder "music"
file_in_directory = os.listdir('music')

def file_as_bytes(file):
    with file:
        return file.read()

for file in file_in_directory:
    print (file, hashlib.md5(file_as_bytes(open('music/'+ file, 'rb'))).hexdigest())
