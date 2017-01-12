# DirectShow SDK

This is an unofficial mirror for Microsoft's directshow. This only has a build script to build with Python.

You can get the official source from [http://www.microsoft.com/en-us/download/details.aspx?id=8279](http://www.microsoft.com/en-us/download/details.aspx?id=8279).

## Building

Open /baseclasses/baseclasses.sln and build. You can build x64 and x86 in debug and release by running

```
./build.py
```

This will build with [dynamic runtime library (/MD)](https://msdn.microsoft.com/en-us/library/2kzt1wy3.aspx). If you want to use static (/MT) then do:

```
./build.py -static
```
