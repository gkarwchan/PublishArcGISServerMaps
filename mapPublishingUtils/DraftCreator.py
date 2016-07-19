import logging, arcpy, ntpath
from CommonUtils import CustomException, removeWhenExist, printInfo
from mapPublishingUtils.basePublisher import basePublisher
import xml.dom.minidom as DOM

__author__ = 'ghassan_karwchan'
class DraftCreator(basePublisher):
    def createDraft(self, connectionFile):
        try:
            removeWhenExist(self.draftPath)
            analysis = arcpy.mapping.CreateMapSDDraft(self.mapDocument, self.draftPath, self.serviceName, 'ARCGIS_SERVER', connectionFile, False, self.serviceFolder)
            if analysis['errors'] != {}:
                raise CustomException('createDraft: creating draft')
            logging.debug('\t\tcreated initial draft')
            self.xmlDocument = DOM.parse(self.draftPath)
            if self.serviceExist(self.serviceName, self.serviceFolder):
                self.__setPublishToOverwrite()
                logging.debug('\t\tchanged draft definition to overwrite')
            self.__disableKml()
            if self.serviceFolder.upper() == 'BASEMAP':
                self.__setServiceProperty('textAntialiasingMode', 'None')
            else:
                self.__setServiceProperty('antialiasingMode', 'Best')
            logging.debug('\t\tchanged draft definition to not publish kml')
            fileWriter = open(self.draftPath, 'w')
            self.xmlDocument.writexml(fileWriter)
            fileWriter.close()
            printInfo ('\t\tcreated draft')
        except Exception as e:
            logging.error('error creating draft: ' + e.message)
            raise CustomException('createDraft: creating draft')
    def __setPublishToOverwrite(self):
        descriptions = self.xmlDocument.getElementsByTagName('Type')
        for desc in descriptions:
            if desc.parentNode.tagName == 'SVCManifest':
                if desc.hasChildNodes():
                    desc.firstChild.data = 'esriServiceDefinitionType_Replacement'
    def __disableKml(self):
        typeNames = self.xmlDocument.getElementsByTagName('TypeName')
        for typeName in typeNames:
            if typeName.firstChild.data == 'KmlServer':
                extension = typeName.parentNode
                for extElement in extension.childNodes:
                    if extElement.tagName == 'Enabled':
                        extElement.firstChild.data = 'false'
    def __setServiceProperty(self, key, value):
        configuration = self.xmlDocument.getElementsByTagName('ConfigurationProperties').item(0)
        properties = configuration.getElementsByTagName('PropertySetProperty')
        for property in properties:
            if property.getElementsByTagName('Key').item(0).firstChild.nodeValue == key:
                property.getElementsByTagName('Value').item(0).firstChild.data = value
                logging.debug('\t\tchanged service property {0} to {1}'.format(key, value))


