#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


class Event:
    def __init__(self, timestamp, action, truck_number, point, load_amount):
        self.timestamp = timestamp
        self.action = action
        self.truck_number = truck_number
        self.point = point
        self.load_amount = load_amount
