#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import configparser


def get_global_config():
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    global_config = parser['GLOBAL']
    return global_config
