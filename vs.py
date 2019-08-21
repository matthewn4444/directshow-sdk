#!/usr/bin/env python

import subprocess, os, operator, fnmatch

def directory_sort(a, b):
    if a.startswith("Microsoft Visual Studio "):
        if b.startswith("Microsoft Visual Studio "):
            return int(float(b[23:]) - float(a[23:]))
        else:
            return -1
    elif b.startswith("Microsoft Visual Studio "):
        return 1
    else:
        return -1

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def get_devenv_path():
    # Check the progrom files location
    program_files = None
    if os.path.exists("c:\\Program Files (x86)\\"):
        program_files = "c:\\Program Files (x86)\\"
    elif os.path.exists("c:\\Program Files\\"):
        program_files = "c:\\Program Files\\"
    else:
        raise Exception('Cannot find program files, are you running this on windows?')

    subdirectories = os.listdir(program_files)
    subdirectories.sort(cmp=directory_sort)
    for dir in subdirectories:
        if "Microsoft Visual Studio" in dir:
            # Found newest Visual Studio Version by year
            subdirs2 = os.listdir(program_files + dir)
            subdirs2 = [s for s in subdirs2 if s.isdigit()]
            subdirs2.sort(reverse=True)
            if not subdirs2[0]:
                print "Failed to find Visual Studio on this machine"
                exit
            path = program_files + dir + "\\" + subdirs2[0]

            # Search for the devenv.exe in this folder
            file = None
            for filename in find_files(path, "devenv.exe"):
                file = filename
                break;
            if os.path.exists(file):
                return file
            break

    print "Failed to find Visual Studio on this machine"

def upgrade(devenv_path, vcproj):
    return subprocess.call("\"" + devenv_path + "\" -upgrade " + vcproj, shell=True, stdout=subprocess.PIPE)

def build(devenv_path, vcxproj, isRelease, is32Bit):
    args = ("Release" if isRelease else "Debug")
    if not is32Bit:
        args = args + "|x64"
    return subprocess.call("\"" + devenv_path + "\" " + vcxproj + " -build \"" + args + "\"", shell=True, stdout=subprocess.PIPE)
