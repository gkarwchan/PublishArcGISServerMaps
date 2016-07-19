import logging
import ntpath
import os, argparse

def printInfo(message):
    print (message)
    logging.info(message)


class CustomException(Exception):
    def __init__(self, value):
        self.message = value
    def __str__(self):
        return repr(self.message)

def removeWhenExist(file):
    if ntpath.exists(file):
        os.remove(file)


def parseMapArgument(mapArgument):
    if mapArgument is not None:
        args = mapArgument.split('\\')
        folderNames = ['pods' if args[0] == 'profiles' else args[0]]
        if len(args) == 1:
            mapNameFilter = '*.mxd'
        else:
            mapNameFilter = args[1].replace('.mxd', '') + '.mxd'
    else:
        folderNames = ['pods', 'basemap']
        mapNameFilter = '*.mxd'
    return folderNames, mapNameFilter


def getArguments():
#************* parse the arguments and set default arguments
#************* the default arguments are : dev
    parser = argparse.ArgumentParser(description='e.g.: publish dev [--map profiles\general] ')
    parser.add_argument('environment', nargs='?', help=': should be one of these [dev|qual|prod]', default='dev')
    parser.add_argument('--map', help=': (optional) specify the map and the folder using the syntax {folder}\{map}. folder can be either: basemap|profiles.to process all maps in folder enter just folder name.')
    args = parser.parse_args()
    return args
