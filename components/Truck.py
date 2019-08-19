#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import math
import config


class Truck:
    operation_days = 0
    arrival_count = 0

    def __init__(self, truck_number, truck_size, purchase_date, products_inventory):
        self.truck_number = truck_number
        self.truck_size = truck_size
        self.purchase_date = purchase_date
        self.products_inventory = products_inventory if products_inventory <= self.truck_size else self.truck_size

    # Set actual days took that truck was moving
    def add_operation_day(self, days):
        if days > 0:
            self.operation_days = self.operation_days + days

    # Increment count when truck stops at depot or warehouse
    def increment_arrival_count(self):
        self.arrival_count = self.arrival_count + 1

    # Get truck purchase cost with truck maximum capacity and days used
    def get_truck_purchase_cost(self):
        global_config = config.get_global_config()
        days_used = int(global_config['SIMULATION_DAYS']) - self.purchase_date
        truck_purchase_cost = (8350.6 * math.log(self.truck_size) - 14542.5) * days_used / int(global_config['SIMULATION_DAYS'])
        print('Truck {} Purchase Cost [ capacity: {}, days used: {} ]: {}'
              .format(self.truck_number, self.truck_size, days_used, truck_purchase_cost))
        return truck_purchase_cost

    # Get truck operating cost with truck maximum capacity, truck operation days and arrival count
    def get_truck_operating_cost(self):
        truck_operation_cost = (1.67012 * math.log(self.truck_size) - 2.9885) \
                               * self.operation_days + self.arrival_count * 2
        print('Truck {} Operating Cost [ capacity: {}, operation days: {}, arrival count: {} ]: {}'
              .format(self.truck_number, self.truck_size, self.operation_days, self.arrival_count, truck_operation_cost))
        return truck_operation_cost

