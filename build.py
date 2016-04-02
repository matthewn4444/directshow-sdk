#!/usr/bin/env python

import vs, os

def main():
    print 'Finding Visual Studio folder'
    path = vs.get_devenv_path()
    if path != None:
        print "Upgrade Visual Studio project"
        res = vs.upgrade(path, "baseclasses\\baseclasses.vcproj")
        if res != 0:
            print "\tFailure to upgrade project"
            return

        # Change the output folder
        content = None
        with open("baseclasses\\baseclasses.vcxproj", "r") as f:
            content = f.read()
            content = content.replace("<OutDir>Debug\\</OutDir>", "<OutDir>..\\lib</OutDir>")
            content = content.replace("<OutDir>Release\\</OutDir>", "<OutDir>..\\lib</OutDir>")
            content = content.replace("<OutDir>$(Platform)\\$(Configuration)\\</OutDir>", "<OutDir>..\\lib\\$(Platform)\\</OutDir>")
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
