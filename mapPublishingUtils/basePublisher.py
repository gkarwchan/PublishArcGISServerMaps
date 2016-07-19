import json, os
import logging, tempfile
import stat
import urllib, shutil
import arcpy, ntpath
from CommonUtils import printInfo, CustomException
from FolderUtils import FolderUtils

__author__ = 'ghassan_karwchan'

class basePublisher:
    def __init__(self, filename, service, serviceFolder, host, port, user, password, workingDir):
        self.serviceName = service
        self.serviceFolder = serviceFolder
        self.fileName = filename
        self.workingDir = workingDir
        self.token = None
        self.workingFileName = ntpath.join(self.workingDir, self.serviceName + ".mxd")
        self.tempFileName = ntpath.join(self.workingDir, self.serviceName + "_temp.mxd")
        FolderUtils.removeWhenExist(self.workingFileName)
        shutil.copy(self.fileName, self.workingFileName)
        os.chmod(self.workingFileName, stat.S_IWRITE)
        logging.debug('\tcopied: {0} to {1}'.format(self.fileName, self.workingFileName))
        self.mapDocument = arcpy.mapping.MapDocument(self.workingFileName)
        self.draftPath = ntpath.join(self.workingDir, self.serviceName + ".sddraft")
        self.definitionPath = ntpath.join(self.workingDir, self.serviceName + ".sd")
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        printInfo ('\tmap: {0}'.format(self.fileName))
    def initToken(self):
        if self.token is None:
            logging.debug('\t\tcreating token')
            queryDict = { 'username': self.user, 'password': self.password, 'expiration':'60', 'client':'requestip'}
            queryString = urllib.urlencode(queryDict)
            url = "http://{}:6080/arcgis/admin/generateToken".format(self.host)
            myToken = json.loads(urllib.urlopen(url + "?f=json", queryString).read())
            if "token" not in myToken:
                raise CustomException('getToken: token could not be established')
            printInfo ('\t\tcreated token')
            self.token = myToken['token']

    def serviceExist(self, service, folder):
        self.initToken()
        url = "http://{}:{}/arcgis/admin/services/{}/{}.MapServer?f=pjson&token={}".format(self.host, self.port, folder, service, self.token)
        serviceInfo = json.loads(urllib.urlopen(url).read())
        return 'serviceName' in serviceInfo
    def destroy(self):
        del self.mapDocument
