#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import config


class Warehouse:
    added_warehouse_size = []
    additional_purchase_date = []

    def __init__(self, warehouse_number, max_warehouse_size, purchase_date, inventory, demand, demand_growth, size_limit, truck_size_limit, mapping):
        self.warehouse_number = warehouse_number
        self.max_warehouse_size = min(max_warehouse_size, size_limit)
        self.purchase_date = purchase_date
        self.inventory = min(inventory, self.max_warehouse_size)
        self.demand = demand
        self.demand_growth = demand_growth
        self.size_limit = size_limit
        self.truck_size_limit = truck_size_limit
        self.mapping = mapping
        # Apply in dijkstra method, origin set to 0, other nodes set to infinity
        self.smallest_distance_to_depot = 0 if warehouse_number == 'D1' else float('inf')

    # Purchase additional warehouse size, update the record
    def purchase_additional_warehouse_size(self, size, date):
        # Depot cant purchase more size
        if self.warehouse_number == 'D1':
            return

        if self.max_warehouse_size + size <= self.size_limit:
            self.added_warehouse_size.append(size)
            self.additional_purchase_date.append(date)
        else:
            raise RuntimeError('Warehouse {} size cannot exceed size limit {}'.format(self.warehouse_number, self.size_limit))

    # Get warehouse purchase cost with warehouse maximum capacity and days used
    def get_warehouse_purchase_cost(self):
        global_config = config.get_global_config()
        days_used = int(global_config['SIMULATION_DAYS']) - self.purchase_date

        # Depot dont have purchase cost
        if self.warehouse_number == 'D1':
            return 0

        # When warehouse has additional size
        if len(self.additional_purchase_date) > 0:
            days_used = self.additional_purchase_date[0] - self.purchase_date
            warehouse_purchase_cost = 29.725 * self.max_warehouse_size * days_used / int(global_config['SIMULATION_DAYS'])
            index = 0
            for new_purchase_date in self.additional_purchase_date:
                # For last additional purchase
                if index >= len(self.additional_purchase_date) - 1:
                    days_used = int(global_config['SIMULATION_DAYS']) - new_purchase_date
                    self.max_warehouse_size = self.max_warehouse_size + self.added_warehouse_size[index]
                    warehouse_purchase_cost = warehouse_purchase_cost + (29.725 * self.max_warehouse_size * days_used / int(global_config['SIMULATION_DAYS']))
                else:
                    days_used = self.additional_purchase_date[index + 1] - new_purchase_date
                    self.max_warehouse_size = self.max_warehouse_size + self.added_warehouse_size[index]
                    warehouse_purchase_cost = warehouse_purchase_cost + (29.725 * self.max_warehouse_size * days_used / int(global_config['SIMULATION_DAYS']))
                index = index + 1
            print('Warehouse {} Purchase Cost [ capacity: {}, days used: {} ]: {}'
                  .format(self.warehouse_number, self.max_warehouse_size, int(global_config['SIMULATION_DAYS']) - self.purchase_date, warehouse_purchase_cost))
            return warehouse_purchase_cost

        else:
            warehouse_purchase_cost = 29.725 * self.max_warehouse_size * days_used / int(global_config['SIMULATION_DAYS'])
            print('Warehouse {} Purchase Cost [ capacity: {}, days used: {} ]: {}'
                  .format(self.warehouse_number, self.max_warehouse_size, days_used, warehouse_purchase_cost))
            return warehouse_purchase_cost
