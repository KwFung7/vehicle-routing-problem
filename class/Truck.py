#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import math
import config


class Truck:
    truck_number = 1
    truck_size = 320
    purchase_date = 0
    products_inventory = 100
    operation_days = 0
    arrival_count = 0

    def __init__(self, truck_number, truck_size, purchase_date, products_inventory):
        global_config = config.get_global_config()
        self.truck_number = truck_number
        self.truck_size = truck_size
        self.purchase_date = purchase_date
        self.products_inventory = products_inventory
        self.days_used = global_config['SIMULATION_DAYS'] - purchase_date

    # Get truck purchase cost with truck maximum capacity and days used
    def get_truck_purchase_cost(self):
        global_config = config.get_global_config()
        truck_purchase_cost = (8350.6 * math.log(self.truck_size) - 14542.5) * self.days_used / global_config['SIMULATION_DAYS']
        print('Truck Purchase Cost [ capacity: {}, days used: {} ]: {}'
              .format(self.truck_size, self.days_used, truck_purchase_cost))
        return truck_purchase_cost

    # Get truck operating cost with truck maximum capacity, truck operation days and arrival count
    def get_truck_operating_cost(self):
        truck_operation_cost = (1.67012 * math.log(self.truck_size) - 2.9885) \
                               * self.operation_days + self.arrival_count * 2
        print('Truck Operating Cost [ capacity: {}, operation days: {}, arrival count: {} ]: {}'
              .format(self.truck_size, self.operation_days, self.arrival_count, truck_operation_cost))
        return truck_operation_cost
