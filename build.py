#!/usr/bin/env python

import vs, os, sys

def main():
    # Parse the arguments
    use_static = False
    for x in sys.argv[1:]:
        if x[0] == '-':
            switch = x[1:]
            if switch == 'static':
                use_static = True

    print 'Finding Visual Studio folder'
    path = vs.get_devenv_path()
    if path != None:
        # Change the output folder
        content = None
        with open("baseclasses\\baseclasses.vcxproj", "r") as f:
            content = f.read()
            content = content.replace("<OutDir>Debug\\</OutDir>", "<OutDir>..\\lib</OutDir>")
            content = content.replace("<OutDir>Release\\</OutDir>", "<OutDir>..\\lib</OutDir>")
            content = content.replace("<OutDir>$(Platform)\\$(Configuration)\\</OutDir>", "<OutDir>..\\lib\\$(Platform)\\</OutDir>")

            # Add static/dynamic to build
            if use_static == True:
                content = content.replace("<RuntimeLibrary>MultiThreadedDLL</RuntimeLibrary>", "<RuntimeLibrary>MultiThreaded</RuntimeLibrary>")
                content = content.replace("<RuntimeLibrary>MultiThreadedDebugDLL</RuntimeLibrary>", "<RuntimeLibrary>MultiThreadedDebug</RuntimeLibrary>")
            else:
                content = content.replace("<RuntimeLibrary>MultiThreaded</RuntimeLibrary>", "<RuntimeLibrary>MultiThreadedDLL</RuntimeLibrary>")
                content = content.replace("<RuntimeLibrary>MultiThreadedDebug</RuntimeLibrary>", "<RuntimeLibrary>MultiThreadedDebugDLL</RuntimeLibrary>")
        with open("baseclasses\\baseclasses.vcxproj", "w") as w:
            w.write(content)

        # Build all configurations
        print "\tBuilding release x86"
        res = vs.build(path, "baseclasses\\baseclasses.vcxproj", True, True)
        if res != 0:
            print "\tFailure to build release x86, open Visual Studio to see the issue"
            return

        print "\tBuilding release x64"
        res = vs.build(path, "baseclasses\\baseclasses.vcxproj", True, False)
        if res != 0:
            print "\tFailure to build release x64, open Visual Studio to see the issue"
            return

        print "\tBuilding debug x86"
        res = vs.build(path, "baseclasses\\baseclasses.vcxproj", False, True)
        if res != 0:
            print "\tFailure to build release x86, open Visual Studio to see the issue"
            return

        print "\tBuilding debug x64"
        res = vs.build(path, "baseclasses\\baseclasses.vcxproj", False, False)
        if res != 0:
            print "\tFailure to build release x86, open Visual Studio to see the issue"
            return

        print "\tSuccessfully built directshow"
    else:
        print "\tFailed to find Visual Studio path, cannot build"

if __name__ == "__main__":
    main()
