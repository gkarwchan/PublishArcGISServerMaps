import logging, os, shutil, arcpy
from basePublisher import *
from FolderUtils import *

class MapDataSourceSetter(basePublisher):
    def replaceDataSource(self, targetDataSource):
        logging.debug('\t\treplacing data source with: {0}'.format(targetDataSource))
        layers = arcpy.mapping.ListLayers(self.mapDocument)
        count = 0
        while not layers[count].supports('WORKSPACEPATH'):
            count = count + 1
        layerData = arcpy.mapping.ListLayers(self.mapDocument)[count].workspacePath
        self.mapDocument.findAndReplaceWorkspacePaths(layerData, targetDataSource, False)
        self.mapDocument.saveACopy(self.tempFileName)
        del self.mapDocument
        backupFile = FolderUtils.makeBackup(self.workingFileName)
        shutil.move(self.tempFileName, self.workingFileName)
        os.chmod(backupFile, stat.S_IWRITE)
        os.remove(backupFile)
        self.mapDocument = arcpy.mapping.MapDocument(self.workingFileName)
        printInfo('\t\tchanged data source')