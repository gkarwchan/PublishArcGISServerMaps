import logging
import arcpy
from CommonUtils import CustomException, printInfo
from basePublisher import basePublisher

class DataSourceValidator(basePublisher):
    def validateDatasource(self, environment):
            layers = arcpy.mapping.ListLayers(self.mapDocument)
            if not layers:
                logging.error('\t\tNo layers found in the document')
                raise CustomException('validateDatasource: no layers found')
            brokenDataSources = arcpy.mapping.ListBrokenDataSources(self.mapDocument)
            if brokenDataSources:
                for brokenItem in brokenDataSources:
                    logging.error('\t\tError data broken for layer: {0} is broken: {1}'.format(brokenItem.longName, brokenItem.dataSource))
                raise CustomException('validateDatasource: Broken layers')
            badWordsDict = { "dev": [ "tmes", "pmes"], "qual": [ "dmes", "pmes"], "prod": [ "dmes", "tmes"] }
            for layer in layers:
                if layer.supports('WORKSPACEPATH'):
                    workspacePath = layer.workspacePath
                    for badWord in badWordsDict[environment]:
                        if workspacePath.count(badWord):
                            logging.error('\t\tLayer {0} contain {1} in its workspace path {2}'.format(layer.longName, badWord, workspacePath))
                            raise CustomException('validateDatasource: UNC path contain wrong environment workspace')
            printInfo('\t\tvalidated data sources')
