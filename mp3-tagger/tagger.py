import os
from shutil import copyfile
from mutagen.easyid3 import EasyID3
import argparse
import sys


def get_all_files_in_dir(directory):
    files = [args.file + x for x in os.listdir(args.file)]
    return files


def spaces_to_kebab_case(name):
    return name.replace(' ', '-').lower()


def copy_file(directory, filepath):
    try:
        filename = os.path.basename(filepath)
        outputpath = os.path.join(directory, filename)
        copyfile(filepath, outputpath)
        return outputpath
    except Exception as e:
        print("copying failed! ", e)
        sys.exit(1)


def rename_file(filepath):
    try:
        # Get the info from audio file
        audiofile = EasyID3(filepath)
        currTitle = audiofile["title"]
        currArtist = audiofile["artist"]
        filename = os.path.basename(filepath)
        # Prepare the new name
        filename = spaces_to_kebab_case(
            "{0}-{1}.mp3".format(currTitle[0], currArtist[0]))
        dirname = os.path.dirname(filepath)
        # Rename
        os.rename(filepath, os.path.join(dirname, filename))
        print("Renamed file: ", filename)
    except Exception as e:
        print("Rename failed! ", e)
        sys.exit(1)


def tag(filepath):
    try:
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
        return True
    except:
        print("ERROR TAGGING! ", os.path.basename(filepath))
        copy_file(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "error"), filepath)
        return False


# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("file", help="specify the file you want to work with")
args = parser.parse_args()
# Program


def main():
    directory = get_all_files_in_dir(args.file)
    for filepath in directory:
        x = copy_file(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "output"), filepath)
        if tag(x):
            rename_file(x)


main()
print("SUCCESS!")
