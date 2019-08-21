#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


def create_distance_mapping(warehouse_data):
    mapping = {}
    for key in warehouse_data:
        if 'W' in key or 'D' in key:
            mapping[key] = warehouse_data[key]
    return mapping
