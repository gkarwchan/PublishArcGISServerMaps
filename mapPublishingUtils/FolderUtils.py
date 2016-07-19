import ntpath, shutil, tempfile, uuid, os, logging
import stat

class FolderUtils:
    @staticmethod
    def getCorrespondingPath(targetFolder, fileName, extension):
        return ntpath.join(targetFolder, fileName + extension)
    @staticmethod
    def makeBackup(fileName):
        originalFileName = fileName.replace('.mxd', '_original.mxd')
        shutil.move(fileName, originalFileName)
        return originalFileName
    @staticmethod
    def getTempFile():
        file = r"{0}\{1}{2}".format(tempfile.gettempdir(), str(uuid.uuid1()), '.mxd')
        return file
    @staticmethod
    def removeWhenExist(file):
        if ntpath.exists(file):
            os.remove(file)
    @staticmethod
    def creteEmptyDir(folder):
        if ntpath.exists(folder):
            for file in os.listdir(folder):
                os.chmod(ntpath.join(folder, file), stat.S_IWRITE)
                os.remove(ntpath.join(folder, file))
            os.chmod(folder, stat.S_IWRITE)
            shutil.rmtree(folder)
            logging.debug('delete: {0}'.format(folder))
        os.makedirs(folder)
        logging.debug('create: {0}'.format(folder))
