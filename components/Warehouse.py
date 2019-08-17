#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import config


class Warehouse:
    added_warehouse_size = []
    additional_purchase_date = []

    def __init__(self, warehouse_number, initial_warehouse_size, purchase_data, inventory):
        global_config = config.get_global_config()
        self.warehouse_number = warehouse_number
        self.max_warehouse_size = initial_warehouse_size
        self.purchase_date = purchase_data
        self.inventory = inventory
        self.days_used = int(global_config['SIMULATION_DAYS']) - purchase_data

    # Purchase additional warehouse size, update the record
    def purchase_additional_warehouse_size(self, size, date):
        self.added_warehouse_size.append(size)
        self.additional_purchase_date.append(date)

    # Get warehouse purchase cost with warehouse maximum capacity and days used
    def get_warehouse_purchase_cost(self):
        global_config = config.get_global_config()

        # When warehouse has additional size
        if len(self.additional_purchase_date) > 0:
            self.days_used = self.additional_purchase_date[0] - self.purchase_date
            warehouse_purchase_cost = 29.725 * self.max_warehouse_size * self.days_used / int(global_config['SIMULATION_DAYS'])
            index = 0
            for new_purchase_date in self.additional_purchase_date:
                # For last additional purchase
                if index >= len(self.additional_purchase_date) - 1:
                    self.days_used = int(global_config['SIMULATION_DAYS']) - new_purchase_date
                    self.max_warehouse_size = self.max_warehouse_size + self.added_warehouse_size[index]
                    warehouse_purchase_cost = warehouse_purchase_cost + (29.725 * self.max_warehouse_size * self.days_used / int(global_config['SIMULATION_DAYS']))
                else:
                    self.days_used = self.additional_purchase_date[index + 1] - new_purchase_date
                    self.max_warehouse_size = self.max_warehouse_size + self.added_warehouse_size[index]
                    warehouse_purchase_cost = warehouse_purchase_cost + (29.725 * self.max_warehouse_size * self.days_used / int(global_config['SIMULATION_DAYS']))
                index = index + 1
            print('Warehouse {} Purchase Cost [ capacity: {}, days used: {} ]: {}'
                  .format(self.warehouse_number, self.max_warehouse_size, int(global_config['SIMULATION_DAYS']) - self.purchase_date, warehouse_purchase_cost))
            return warehouse_purchase_cost

        else:
            warehouse_purchase_cost = 29.725 * self.max_warehouse_size * self.days_used / int(global_config['SIMULATION_DAYS'])
            print('Warehouse {} Purchase Cost [ capacity: {}, days used: {} ]: {}'
                  .format(self.warehouse_number, self.max_warehouse_size, self.days_used, warehouse_purchase_cost))
            return warehouse_purchase_cost
