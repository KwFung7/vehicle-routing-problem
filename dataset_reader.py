#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import configparser
import csv


def get_global_config():
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    global_config = parser['GLOBAL']
    return global_config


# Get specific node that represents either depot or warehouse
def get_node(name='depo'):
    global_config = get_global_config()
    with open(global_config['DATASET_PATH'], newline='') as dataset:
        # Read csv dataset
        datadict = csv.DictReader(dataset)

        for row in datadict:
            # Return node with specific name
            if row['depot_warehouse_name'] == name:
                return row