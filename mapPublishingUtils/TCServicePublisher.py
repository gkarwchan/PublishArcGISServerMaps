import json, urllib, logging
from CommonUtils import CustomException
from DataSourceValidator import DataSourceValidator
from basePublisher import basePublisher
from MapDataSourceSetter import MapDataSourceSetter
from DraftCreator import DraftCreator
from ServiceDefinitionCreator import ServiceDefinitionCreator
from ServiceUploader import ServiceUploader

class TCServicePublisher(ServiceUploader, ServiceDefinitionCreator, DraftCreator, MapDataSourceSetter, DataSourceValidator, basePublisher):
    pass