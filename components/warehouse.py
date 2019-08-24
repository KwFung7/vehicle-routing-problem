#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import config


class Warehouse:
    added_warehouse_size = []
    additional_purchase_date = []
    last_loading_time = 0

    def __init__(self, warehouse_number, max_warehouse_size, purchase_date, inventory, initial_demand, demand_growth, size_limit, truck_size_limit, mapping):
        self.warehouse_number = warehouse_number
        self.max_warehouse_size = min(max_warehouse_size, size_limit)
        self.purchase_date = purchase_date
        self.inventory = min(inventory, self.max_warehouse_size)
        self.initial_demand = initial_demand
        self.demand_growth = demand_growth
        self.size_limit = size_limit
        self.truck_size_limit = truck_size_limit
        self.mapping = mapping
        self.path_score = mapping.fromkeys(mapping, 0)

    def load_product_from_truck(self, amount, timestamp):
        global_config = config.get_global_config()
        standard_unit = int(global_config['STANDARD_UNIT'])

        if self.inventory + amount > self.max_warehouse_size:
            self.purchase_additional_warehouse_size(standard_unit, timestamp)
        self.inventory += amount

    def load_product_to_truck(self, amount):
        if self.inventory - amount >= 0:
            self.inventory -= amount
        else:
            raise RuntimeError('Warehouse {} inventory dropped below zero: {}'.format(self.warehouse_number, self.inventory))

    # Calculate current inventory with given time
    # When inventory is below 0, program should throw error
    def update_current_inventory(self, timestamp):
        global_config = config.get_global_config()
        demand_growth_period = int(global_config['DEMAND_GROWTH_PERIOD'])

        # When both time are within same 30 days period
        if (self.last_loading_time / demand_growth_period) == (timestamp / demand_growth_period):
            current_demand = self.get_current_demand(self.last_loading_time)
            self.inventory = self.inventory - ((timestamp - self.last_loading_time) * current_demand)
        else:
            # If timestamp is 31.4, remaining value is 1.4
            # remaining value should calculate with growth demand
            remaining_val = timestamp % demand_growth_period
            current_demand = self.get_current_demand(timestamp)
            self.inventory = self.inventory - (remaining_val * current_demand)

            current_demand = self.get_current_demand(self.last_loading_time)
            self.inventory = self.inventory - ((timestamp - remaining_val - self.last_loading_time) * current_demand)

        self.last_loading_time = timestamp

        # If inventory dropped below 0, program terminated
        if self.inventory < 0:
            raise RuntimeError('Warehouse {} inventory dropped below zero: {}'.format(self.warehouse_number, self.inventory))

        return self.inventory

    # Calculate current demand with given timestamp
    def get_current_demand(self, timestamp):
        global_config = config.get_global_config()
        demand_growth_period = int(global_config['DEMAND_GROWTH_PERIOD'])

        if timestamp < demand_growth_period:
            return self.initial_demand
        else:
            current_demand = self.initial_demand
            for i in range(int(timestamp / demand_growth_period)):
                current_demand = current_demand * (1 + self.demand_growth)
            return current_demand

    # Purchase additional warehouse size, update the record
    def purchase_additional_warehouse_size(self, size, date):
        # Depot cant purchase more size
        if self.warehouse_number == 'D1':
            return

        if self.max_warehouse_size + size <= self.size_limit:
            self.max_warehouse_size += size
            self.added_warehouse_size.append(size)
            self.additional_purchase_date.append(date)
            print('Warehouse {} maximum size enhance to {}'.format(self.warehouse_number, self.max_warehouse_size))
        else:
            raise RuntimeError('Warehouse {} size cannot exceed size limit {}'.format(self.warehouse_number, self.size_limit))

    # Get warehouse purchase cost with warehouse maximum capacity and days used
    # def get_warehouse_purchase_cost(self):
    #     global_config = config.get_global_config()
    #     days_used = int(global_config['SIMULATION_DAYS']) - self.purchase_date
    #
    #     # Depot dont have purchase cost
    #     if self.warehouse_number == 'D1':
    #         return 0
    #
    #     # When warehouse has additional size
    #     if len(self.additional_purchase_date) > 0:
    #         days_used = self.additional_purchase_date[0] - self.purchase_date
    #         warehouse_purchase_cost = 29.725 * self.max_warehouse_size * days_used / int(global_config['SIMULATION_DAYS'])
    #         index = 0
    #         for new_purchase_date in self.additional_purchase_date:
    #             # For last additional purchase
    #             if index >= len(self.additional_purchase_date) - 1:
    #                 days_used = int(global_config['SIMULATION_DAYS']) - new_purchase_date
    #                 max_warehouse_size = self.max_warehouse_size + self.added_warehouse_size[index]
    #                 warehouse_purchase_cost = warehouse_purchase_cost + (29.725 * max_warehouse_size * days_used / int(global_config['SIMULATION_DAYS']))
    #             else:
    #                 days_used = self.additional_purchase_date[index + 1] - new_purchase_date
    #                 max_warehouse_size = self.max_warehouse_size + self.added_warehouse_size[index]
    #                 warehouse_purchase_cost = warehouse_purchase_cost + (29.725 * max_warehouse_size * days_used / int(global_config['SIMULATION_DAYS']))
    #             index = index + 1
    #         print('Warehouse {} purchase cost [ capacity: {}, days used: {} ]: {}'
    #               .format(self.warehouse_number, self.max_warehouse_size, int(global_config['SIMULATION_DAYS']) - self.purchase_date, warehouse_purchase_cost))
    #         return warehouse_purchase_cost
    #
    #     else:
    #         warehouse_purchase_cost = 29.725 * self.max_warehouse_size * days_used / int(global_config['SIMULATION_DAYS'])
    #         print('Warehouse {} purchase cost [ capacity: {}, days used: {} ]: {}'
    #               .format(self.warehouse_number, self.max_warehouse_size, days_used, warehouse_purchase_cost))
    #         return warehouse_purchase_cost
