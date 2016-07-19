import ConfigParser, logging, argparse, fnmatch, os, logging.config, getpass
from CommonUtils import *
from mapPublishingUtils.FolderUtils import FolderUtils
from mapPublishingUtils.TCServicePublisher import TCServicePublisher

args = getArguments()
logging.config.fileConfig('logging.conf')
config = ConfigParser.SafeConfigParser()
config.read('settings.conf')
workingFolder = config.get('DEFAULT', 'workingFolder')
FolderUtils.creteEmptyDir(workingFolder)
print ('Enter the password for the user: ' + config.get(args.environment + '-ActiveMaps', 'adminUser'))
password = getpass.getpass()

print '.........................................'
basedir = os.path.abspath(config.get('DEFAULT', 'basedir'))
os.chdir(basedir)
folders, mapFilter = parseMapArgument(args.map)
for folder in folders:
    os.chdir(basedir)
    configSection = "{0}-{1}".format(args.environment, folder)
    mapFolder = config.get(configSection, 'mapFolder')
    printInfo('processing maps in the folder: {0}'.format(mapFolder))
    print '-----------------------------------------------------------------------'
    for root, dirnames, filenames in os.walk(mapFolder):
        for filename in fnmatch.filter(filenames, mapFilter):
            try:
                os.chdir(basedir)
                publisher = TCServicePublisher(os.path.join(root, filename), os.path.splitext(filename)[0], os.path.split(root)[1],
                                           config.get(configSection, 'host') ,  config.get(configSection, 'serverPort'),
                                           config.get(configSection, 'adminUser'), password, workingFolder)
                publisher.replaceDataSource(config.get(configSection, 'connection'))
                publisher.validateDatasource(args.environment)
                publisher.createDraft(config.get(configSection, 'serverConnection'))
                publisher.analyzeForSD()
                publisher.createServiceDefintion()
                publisher.uploadServiceDefinition(config.get(configSection, 'serverConnection'))
            except CustomException as e:
                print ('\t\tError processing map: {0}'.format(e.message))
               #  *************   N O T I C E *************************************************
               # if you encounter problem with one of the maps and you want to continue processing other maps
               #        then uncomment the line below <continue> and comment <raise>
               # to stop processing on the first error you found
               #         then comment <continue> and uncomment <rasie>
                raise
                # continue
            except Exception as e:
                print e.message
                raise

