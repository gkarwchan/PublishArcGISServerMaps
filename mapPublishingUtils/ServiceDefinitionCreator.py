import logging
from CommonUtils import CustomException, printInfo
from mapPublishingUtils.basePublisher import basePublisher
import arcpy

class ServiceDefinitionCreator(basePublisher):
    def analyzeForSD(self):
        analysis = arcpy.mapping.AnalyzeForSD(self.draftPath)
        errors = analysis['errors']
        if errors != {}:
            raise CustomException('analysingForSD: analyzing draft for service definition')
        printInfo ('\t\tvalidated for service defintion')

    def createServiceDefintion(self):
        try:
            stageAnalysis = arcpy.StageService_server(self.draftPath, self.definitionPath)
        except Exception as e:
            logging.error('error creating service definition: ' + e.message)
            raise CustomException('createServiceDefinition: staging service')
        print ('\t\tcreated service definition')
