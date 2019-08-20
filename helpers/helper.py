#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


def create_distance_mapping(warehouse_data):
    mapping = {}
    for key in warehouse_data:
        if '_distance' in key:
            mapping[key] = warehouse_data[key]
    return mapping


def convert_name_to_distance_string(name):
    if name == 'D1':
        return 'depo_distance'
    else:
        return name.replace('W', 'wh') + '_distance'
