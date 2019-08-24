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
        self.products_inventory = min(products_inventory, self.truck_size)

    # Set actual days took that truck was moving
    def add_operation_day(self, days):
        if days > 0:
            self.operation_days = self.operation_days + days

    # Increment count when truck stops at depot or warehouse
    def increment_arrival_count(self):
        self.arrival_count = self.arrival_count + 1

    # Load product from depot or relay warehouse
    def load_product(self, warehouse, amount):
        if self.truck_size > warehouse.truck_size_limit:
            raise RuntimeError('Truck {} size {} is larger than warehouse {} limit {}'.format(
                self.truck_number, self.truck_size, warehouse.warehouse_number, warehouse.truck_size_limit))

        if warehouse.warehouse_number == 'D1':
            load_amount = self.truck_size - self.products_inventory
            self.products_inventory = self.truck_size
            return load_amount
        else:
            warehouse.load_product_to_truck(amount)
            return amount

    # Unload product and update warehouse inventory,
    # truck inventory cannot drop below zero
    def unload_product(self, warehouse, amount, timestamp):
        if self.truck_size > warehouse.truck_size_limit:
            raise RuntimeError('Truck {} size {} is larger than warehouse {} limit {}'.format(
                self.truck_number, self.truck_size, warehouse.warehouse_number, warehouse.truck_size_limit))

        if warehouse.warehouse_number == 'D1':
            return 0

        if self.products_inventory - amount >= 0:
            self.products_inventory -= amount
            warehouse.load_product_from_truck(amount, timestamp)
            return -amount
        else:
            raise RuntimeError('Truck {} inventory dropped below zero: {}'.format(
                self.truck_number, self.products_inventory - amount))

    # Get truck purchase cost with truck maximum capacity and days used
    def get_truck_purchase_cost(self):
        global_config = config.get_global_config()
        days_used = int(global_config['SIMULATION_DAYS']) - self.purchase_date
        truck_purchase_cost = (8350.6 * math.log(self.truck_size) - 14542.5) * days_used / int(global_config['SIMULATION_DAYS'])
        print('Truck {} purchase cost [ capacity: {}, days used: {} ]: {}'
              .format(self.truck_number, self.truck_size, days_used, truck_purchase_cost))
        return truck_purchase_cost

    # Get truck operating cost with truck maximum capacity, truck operation days and arrival count
    def get_truck_operating_cost(self):
        truck_operation_cost = (1.67012 * math.log(self.truck_size) - 2.9885) \
                               * self.operation_days + self.arrival_count * 2
        print('Truck {} operating cost [ capacity: {}, operation days: {}, arrival count: {} ]: {}'
              .format(self.truck_number, self.truck_size, self.operation_days, self.arrival_count, truck_operation_cost))
        return truck_operation_cost

