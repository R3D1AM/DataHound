```
██████╗  █████╗ ████████╗ █████╗     ██╗  ██╗ ██████╗ ██╗   ██╗███╗   ██╗██████╗ 
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██║  ██║██╔═══██╗██║   ██║████╗  ██║██╔══██╗
██║  ██║███████║   ██║   ███████║    ███████║██║   ██║██║   ██║██╔██╗ ██║██║  ██║
██║  ██║██╔══██║   ██║   ██╔══██║    ██╔══██║██║   ██║██║   ██║██║╚██╗██║██║  ██║
██████╔╝██║  ██║   ██║   ██║  ██║    ██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝
``` 
> Maider | 22nd March 2021
-----------------
# Data Hound - Toolkit
-----------------

This toolkit attempts to offer code and material to automate identification of hidden data and extraction of any found data items. It is meant to act as a utility to help an individual find things they might otherwise miss.

Data Hound is written in Python 3.

-----------------

# Contents
- [Structure](#STRUCTURE)
- [Usage](#USAGE)
- [Requirements and Modules](#REQUIREMENTS AND MODULES)
	- [Packages](#Packages)
	- [Modules](#Modules)
	- [Installation](#Installation)
- [Running](#RUNNING)
	- [Audio Files](#Audio Files)
	- [Step 1: Original source Hash](#Step 1: Original source Hash)
- [Manual](#Manual)
- [ Automated](#Automated)
	- [Step 2: Creating the Database](#Step 2: Creating the Database)
	- [Step 3: Running Data Hound](#Step 3: Running Data Hound)
- [Data_Hound.py -  further details](#Data_Hound.py -  further details)
- [Customise](#CUSTOMISE)
- [Disclaimer](#DISCLAIMER)

-----------------

### STRUCTURE
System architecture of Data Hound is based on a standardised "module" structure. Modules are used to integrate all of the toolkit's functionality into separate scripts and units within them.

<p align="center">
<img align="middle" width="600" src="https://github.com/R3D1AM/DataHound/blob/main/screenshots/DataHound_Structure.PNG"/>
<img align="middle" width="600" src="https://github.com/R3D1AM/DataHound/blob/main/screenshots/DataHound_StructurePopulated.PNG"/>
</p>

-----------------

### USAGE
Whenever Data Hound runs, it creates an output directory and places extracted artifcats within it.

Data Hound will not run if the contents of the output directory already exist. It is recommended that any artifacts stored within the output folder are removed before running Data Hound again.

-----------------

### REQUIREMENTS AND MODULES

### Packages
- [py7zr](https://pypi.org/project/py7zr/)	Library utility that allows the handling of 7zip files.
- [tabulate](https://pypi.org/project/tabulate/)	Library, command line utility that allows tables to be printed.

### Modules
- **getopt**	`Analysis for command-line options.`
- **zipfile**	`Allows the creation and amendment of ZIP files.`
- **shutil** `Automation of processes on files, such as copying from source to destination.`
- **sys**	`Allows functions to interact with the runtime environment.`
- **sqlite3**	`C Library that is a lightweight database package not requiring a server.`
- **struct** `Converts C bytes to native Python bytes as objects.`
- **hashlib**	`Allows the creation of hash algorithms: MD5, SHA1, SHA224, SHA256, SHA384, and SHA512.`
- **wave** `Allows Python to interact with WAV audio format.`
- **math** `Contains methods for mathematical functions.`
- **os** `Allows Python to interact with the operating system it is currently being used on via inbuilt functions.`
- **copyfile** `From the shutil module, allows the copying of files.`

### Installation
Installation of the required modules is simple command line instruction: 
`python3 -m pip install “name_of_the_module”`

-----------------

### RUNNING
***Audio Files***

***Step 1: Original source Hash***

### Manual
To manually test the hash function on the files, the `create_md5_of_music.py` script must be run, found in the `extra` folder, therefore the source music folder should be moved to `extra/music`. the output is printed and can then either be copied into the script`db_creator.py` as a dictionary:
example:
```
dic = {'01 Realize.wav' : 'c0828afd3fe91f3e36340cca9318b57f',
"02 Rejection.wav" : '02574c21a9b8b62b74116339df345e03',
"03 Shot In The Dark.wav" : 'e201983e68b0bbd4fce2c59d6593d959',
"04 Through The Mists Of Time.wav" : 'cb0f0aa9abd0a268c322b3597d53d143',
"05 Kick You When You're Down.wav" : 'a585c9192f7e302cf00294b228ae78fc',
"06 Witch's Spell.wav" : '182241d9646a309eb9e3c4d7cad40a67',
"07 Demon Fire.wav" : 'becbb149ab3b55bf33b39156876ddd81',
"08 Wild Reputation.wav" :  '0155251fdb711a4e6103e8b31cfe073f',
"09 No Man's Land.wav" : 'd1309d31a9108345c6320c7bcf8bc3d4',
"10 Systems Down.wav": '8c0e8d564a87213b2a4c6ecb1e8f1075',
"11 Money Shot.wav" : '8c0e8d564a87213b2a4c6ecb1e8f1075',
"12 Code Red.wav" : '3fdd3c5840d363d44033ccf58032f363'}
```
### Automated
The original source files must be loaded into `db/music` folder, to create a comparable hash database for verification of file integrity. 

***Step 2: Creating the Database***

The next step is simply running the `db_creator.py` script. This script creates an SQLite3 database, that houses the MD5 hash digests of the source audio files, that can later be used in file comparison.
Dependant on the number of audio files to check, various tables per album could be created and stored in the one database.
MD5 was used over SHA-256 due to the nature of the project requiring speed, and the checksums created only being used for file integrity, however, the use of SHA-256 could be an optional implementation for users requiring an extra level of security.

***Step 3: Running Data Hound***

Now it is time to run your audio files through Data Hound. The audio files that you want to check for hidden data, should be placed in the folder `/original`, Data Hound will then make copies of these files and output them to `/original_copy` and from now on, will only use the copied files for analysis.

The copied files will be hashed and run against the hash of the original files in the database, if there is a discrepancy between the files, Data Hound will let you know - this is the first indication of file tampering.

Data Hound will then scan the audio file for any hidden files within it, using magic numbers. The hidden file type will be identified and any hidden data will be extracted and placed in the `/extracted` folder. If an audio file has an encrypted zip file hidden within it, Data Hound will, if prompted complete a brute force attack on the password and then extract the decrypted file and place in the `/extracted` folder. 

# **Data_Hound.py -  further details**
This is the main script of the Data Hound Toolkit. The script contains 300 lines of code and consists of 8 functions.
The main function (we shall call it: **function 8**) starts with an intro message and then proceeds to print the database, with the ID, song title and MD5 checksum. The checksums are then checked against the hash of the files in the **/original** folder whilst also copying the original files into the **/original_copy** folder by completing a loop of all files. Lastly, data is attempted to be recovered from the copied file.

The next function (**function 7**) is to compare the hash checksums of the files in the database and the files in the **/original_copy** folder for a match. There are 3 possible outcomes of this check: Firstly, either the song is found in the database or not, leading to the comments “song title present in the database” or “song not present in the database” which determines which of the following comments will be encountered: 1. An exact match is found and the comment “MD5 Hash match (File unmodified)” is printed, or 2. No match is found between the checksums and the comment “MD5 Hash do not match (possible hidden file)”.

**Function 6**, is simply a function to print the contents of the database. The database is checked, and the table is read, using the keys variable to print “N”, “Title”, “MD5” or in layman’s terms: ID number, Song Title and MD5 Checksum as the three columns.

**Function 5 & 6** are for the extraction of an encrypted zip file. The script attempts to extract and read the file, however an exception occurs if the file is password protected and a comment is printed to signify as much. If the file is not password protected, it is simply opened, extracted and placed in **/extracted** folder. However, if there is evidence of encryption, the user is prompted to choose to brute force the password using the rockyou.txt wordlist. Once the password is cracked, again the file and its contents are placed in **/extracted**.

**Function 4** is a tiny function to read the hash file using ‘rb’ command. The command allows the bytes to be read as they are and will return a byte string instead of a text string.

**Function 3** is long, but focuses mainly on data recovery. This section of the script can be split into 2; the first focuses on where to physically find and extract data from, using the sound_path, bits_to_recover and bit_depth the script can be determined as to how to extract the Least Significant Bit of the file and in what pattern, for example: “bit_depth = 2” would determine every other bit that needs scanning for data. This part of the script also sets the rule that if there is more than a byte in the buffer, it should be added to data and the remaining bytes to recover should be decreased by 1. Finally, data should be decoded in UTF-8.

**Function 2**, also the second section sets the rules for identifying and extracting further file types. The file signatures are checked against their magic numbers, as a first step in file identification. The file is then extracted as the file type that the signature identifies it as, and the bytes are written to the output file, using ‘wb+’ which will override any existing file of the same name. The script checks for the most commonly used file types such as: PNG, DOCX, 7Zip, Zip and also includes a printed comment when no file signature matches. This can of course be added to, and is in no way definitive confirmation that a new file type is in use.

**Function 1**, is the part of the script that directs the toolkit on how to read the LSB of an audio file via the size of the file in combination with the number of bits used, with the smallest possible sample size being an 8 bit integer depth and a parameter of 1 << 15 – 1 << LSB. Anything higher results in an error with an unsupported bit-depth due to the use of Python’s wave module.

-----------------

### CUSTOMISE
There are a couple of customisable sections in `data_hound.py`

- `signature` : Magic number signatures can be added or removed as the user requires.
`NOTE: If a new magic number is added, the sound_path and file type descriptor must also be amended.`
- `extract` : The extract function can also be altered to the user requirements.
- `wordlist` : The current wordlist in use is rockyou.txt, this can be replaced with another wordlist, just remember to replace the text file in the `/wordlist` folder as well as in the script.
- `database` : The database to read and compare hash can be changed by the user.
- `directories` : Data Hound comes with pre-set folders, however folder names can be changed.
- `file size` : File size when comparing hash can be changed, dependant on file type.

There are customisable sections in `db_creator.py`

- `database name` : The database name can be changed.
- `database table` : The table columns can be amended as needed, just add new colum to `c.execute` list.
- `Table name` : The table name is also customisable.
- `music folder` : The folder containing original source code (in this case audio files) can be replaced.

-----------------

### DISCLAIMER
Data Hound will automatically process items loaded into the scripts. Due to the automated nature of the toolkit, it is advised running Data Hound with the latest version of Python and inside of a virtual environment.

