#!/usr/bin/env python

import subprocess, os

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
            # Found newest Visual Studio Version
            file = program_files + dir + "\\Common7\\IDE\\devenv.exe"
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
