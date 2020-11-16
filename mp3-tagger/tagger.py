import os
from shutil import copyfile
from mutagen.easyid3 import EasyID3
import argparse
import sys

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("file",
                    help="specify the file/directory you want to work with")
parser.add_argument("-d", "--directory",
                    help="specify that you are providing a directory to be auto tagged",
                    action="store_true")
parser.add_argument("-c", "--cleantag",
                    help="remove current tags",
                    action="store_true")
parser.add_argument("-m", "--modifytags",
                    help="modify existing tags",
                    action="store_true")
parser.add_argument("-a", "--autorename",
                    help="automatically rename files after tagging to kebab case",
                    action="store_true")
parser.add_argument("-r", "--rename",
                    help="rename files manually after tagging",
                    action="store_true")
args = parser.parse_args()


def create_director_if_does_not_exist(name):
    if not os.path.exists(name):
        os.makedirs(name)


def get_all_files_in_dir(directory):
    files = [os.path.join(args.file, x) for x in os.listdir(args.file)]
    return files


def clean_name(name):
    name = name.replace(' ', '-').lower()
    special_chars = [';', ':', '^', '@', '!', '$', '%', '&', '*', '(', ')', '<', '>', '?', '/', '+', '_', '\"', '\'']
    for i in special_chars:
        name = name.replace(i, '')
    return name


def copy_file(directory, filepath):
    try:
        filename = os.path.basename(filepath)
        outputpath = os.path.join(directory, filename)
        copyfile(filepath, outputpath)
        return outputpath
    except Exception as e:
        print("Copying failed! ", e)
        sys.exit(1)


def rename_file(filepath):
    if args.autorename or args.rename:
        try:
            # Get the info from audio file
            audiofile = EasyID3(filepath)
            currTitle = audiofile["title"]
            currArtist = audiofile["artist"]
            filename = os.path.basename(filepath)
            # Prepare the new name
            if args.autorename:
                filename = clean_name(
                    "{0}-{1}.mp3".format(currTitle[0], currArtist[0]))
            elif args.rename:
                filename = input("Filename: ")
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
        if not args.cleantag:
            currTitle = audiofile["title"]
            currArtist = audiofile["artist"]
            currAlbum = audiofile["album"]
        # Remove tags
        if args.cleantag:
            audiofile.delete()
        # Change tags
        if args.cleantag:
            print("New Info ", os.path.basename(filepath))
            newTitle = input("Title: ")
            newArtist = input("Artist: ")
            newAlbum = input("Album: ")
            audiofile["title"] = newTitle
            audiofile["artist"] = newArtist
            audiofile["album"] = newAlbum
        elif args.modifytags:
            print("Current info")
            print("Title: ", currTitle)
            print("Artist: ", currArtist)
            print("Album: ", currAlbum)
            print("New Info")
            newTitle = input("Title: ")
            newArtist = input("Artist: ")
            newAlbum = input("Album: ")
            audiofile["title"] = newTitle
            audiofile["artist"] = newArtist
            audiofile["album"] = newAlbum
        # Save file
        audiofile.save()
        return True
    except Exception as e:
        print("ERROR TAGGING! ", os.path.basename(filepath))
        print(e)
        create_director_if_does_not_exist("errors")
        copy_file(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "errors"), filepath)
        return False


if __name__ == "__main__":
    if args.directory:
        directory = get_all_files_in_dir(args.file)
        for filepath in directory:
            create_director_if_does_not_exist("output")
            x = copy_file(os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "output"), filepath)
            if tag(x):
                rename_file(x)
    else:
        create_director_if_does_not_exist("output")
        x = copy_file(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "output"), filepath)
        if tag(x):
            rename_file(x)
