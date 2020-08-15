import os
from shutil import copyfile
from mutagen.easyid3 import EasyID3
import argparse
import sys

def spaces_to_kebab_case(name):
    return name.replace(' ', '-').lower()

def copy_file(filepath):
    for retry in range(100):
        try:
            filename = os.path.basename(filepath)
            outputpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output", filename)
            copyfile(filepath, outputpath)
            return outputpath
        except:
            print("copying failed!")
    sys.exit(1)

def rename_file(filepath):
    for retry in range(100):
        try:
            # Get the info from audio file
            audiofile = EasyID3(filepath)
            currTitle = audiofile["title"]
            currArtist = audiofile["artist"]
            # Prepare the new name
            filename = spaces_to_kebab_case("{0}-{1}.mp3".format(currTitle[0], currArtist[0]))
            dirname = os.path.dirname(filepath)
            # Rename
            console.log(filename)
            console.log(os.join(dirname, filename))
            os.rename(filepath, os.join(dirname, filename))
            break
        except:
            print("rename failed!")
    sys.exit(1)

def tag(filepath):
    # Load file and store required information
    audiofile = EasyID3(filepath)
    currTitle = audiofile["title"]
    currArtist = audiofile["artist"]
    currAlbum = audiofile["album"]
    # Remove tags
    audiofile.delete()
    # Clean tags
    audiofile["title"] = currTitle
    audiofile["artist"] = currArtist
    audiofile["album"] = currAlbum
    # Save file
    audiofile.save()

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("file", help="specify the file you want to work with")
args = parser.parse_args()

# The program
filepath = copy_file(args.file)
print(filepath)
tag(filepath)
rename_file(filepath)