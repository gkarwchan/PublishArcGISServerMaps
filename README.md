# PublishArcGISServerMaps
Scripts written in Python 2.7 to publish ArcGIS Server Maps.

### Dependencies
The program written for python 2.7.
The progroam requires ArcGIS Desktop 10.2 Python library.
To use different version of ArcGIS, or if the python library is not installed in its default location,
 change the python executable in the file *__publish.bat__* from :
 __"c:\Python27\ArcGIS10.2\python.exe"__ to where the actual library is.  

### Usage
The program can deploy to three environments: dev, qual, prod.  
Run the batch file *__publish.bat__* specifying the environment you want to publish to, where
 the environment is one of these values [dev, qual, prod]. In case you didn't specify environment, the batch will let you know.  
The program uses the username stored in the settings.conf file, and it will prompt you to enter the password.  
The program distinguish between basemaps, and activemaps, and gives you the possibility to have different settings for both. The settings are all stored in settings.conf, and
 the program assumes you run it from different file structure. The file structure can be changed in the config file settings.conf.  

##### File structure:
You run the program from a folder where the following subfolders exists:

1. NewMpas  
constains the new maps which has the following sub-folders:  
2. NewMaps\Basemap  
the basemaps to publish  
3. NewMaps\ActiveMaps
the active maps to publish  
4. workingFolder  
is a temporary folder  
5. resources  
a folder stores the connection files to the servers
6. resources\dev_connections
7. resources\qual_connections
8. resources\prod_connections


### Settings.conf
You see the config file structured based on environment and basemap vs. activemaps.  

* basedir: the basefolder where the above folder structure exists.  
* baseMapFolder: where new maps to be published exists in side the base folder  
* workingFolder: a temporary folder to store temporary working files  
* serverPosrt  
* adminUser: the admin user to publish maps  
* host: the host to publish to  
* serverConnectionFileName  
* serverConnection  
* connection: the connection to the file
