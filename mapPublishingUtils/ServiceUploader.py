import logging, urllib, urllib2, json
import arcpy
import time
from CommonUtils import CustomException
from mapPublishingUtils.basePublisher import basePublisher

class ServiceUploader(basePublisher):
    def uploadServiceDefinition(self, serverConnection):
        try:
            self.initToken()
            self.createFolderWhenNotExist(self.host, self.port)
            arcpy.UploadServiceDefinition_server(self.definitionPath, serverConnection, self.serviceName, '',
                                                 in_folder_type='EXISTING', in_folder=self.serviceFolder, in_startupType='STARTED')
            print ('\t\tpublished the service')
        except Exception as e:
            logging.info("\t\tfailed to publish. Trying Second Time... ")
            time.sleep(60)
            try:
                arcpy.UploadServiceDefinition_server(self.definitionPath, serverConnection, self.serviceName, '',
                                                 in_folder_type='EXISTING', in_folder=self.serviceFolder, in_startupType='STARTED')
            except Exception as e:
                raise CustomException('publishServiceDefinition: ' + e.message)
            print ('\t\tpublished the service')
    def createFolderWhenNotExist(self, server, port):
        URL = "http://{}:{}/arcgis/admin/services/{}?f=pjson&token={}".format(server, port, self.serviceFolder, self.token)
        serviceList = json.loads(urllib2.urlopen(URL).read())
        folderExist = 'folderName' in serviceList
        if not folderExist:
            folderProp_dict = { "folderName": self.serviceFolder,"description": self.serviceFolder }
            folder_encode = urllib.urlencode(folderProp_dict)
            createUrl = "http://{}:{}/arcgis/admin/services/createFolder?token={}&f=json".format(server, port, self.token)
            status = urllib2.urlopen(createUrl, folder_encode).read()
            logging.debug('\t\tcreate folder: ' + self.serviceFolder)
            if not 'success' in status:
                raise CustomException('uploadServiceDefinition: create new service folder')
