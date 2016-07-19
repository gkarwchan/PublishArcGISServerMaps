@echo off
cls
if [%1]==[] goto usage
c:\Python27\ArcGIS10.2\python.exe publish.py %*
goto eof

:usage
c:\Python27\ArcGIS10.2\python.exe publish.py --help

:eof
pause