import os
import ConfigParser as cfg # In python 3, this module is changed to configparser
from Platforms import LINUX as platform

def create_default_configuration():
    configuration = cfg.ConfigParser()
    configuration.add_section('SYSTEM')
    configuration.set('System','Python','#!/usr/bin/env python')
    return configuration

def read_config():
    configFile = os.environ['HOME'] + '/.paropt/paropt.cfg'
    if not os.path.exists(configFile):
        return create_default_configuration()
    configuration = cfg.ConfigParser()
    configuration.read(configFile)
    return configuration

configuration = read_config()
python = configuration.get('SYSTEM','Python')
#paroptRootPackage = 'dev.paropt'
