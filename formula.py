#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import math
import config


# Get warehouse purchase cost with warehouse maximum capacity and days used
def get_warehouse_purchase_cost(max_capacity, days):
    global_config = config.get_global_config()
    warehouse_purchase_cost = 29.725 * max_capacity * days / global_config['SIMULATION_DAYS']
    print('Warehouse Purchase Cost [ capacity: {}, days used: {} ]: {}'
          .format(max_capacity, days, warehouse_purchase_cost))
    return warehouse_purchase_cost


# Get equipment cost with truck and warehouse purchase cost
def get_equipment_cost(truck_max_capacity, truck_days_used, warehouse_max_capacity, warehouse_days_used):
    equipment_cost = get_truck_purchase_cost(truck_max_capacity, truck_days_used)\
                     + get_warehouse_purchase_cost(warehouse_max_capacity, warehouse_days_used)
    print('Equipment Cost: {}'.format(equipment_cost))


# Get normalized operating cost with truck operating cost, total demand, initial total products and end total products
def get_normalized_operating_cost(truck_max_capacity, truck_operation_day, truck_arrival_count, total_demand, total_product_start, total_product_end):
    truck_operating_cost = get_truck_operating_cost(truck_max_capacity, truck_operation_day, truck_arrival_count)
    normalized_operating_cost = truck_operating_cost * total_demand / (total_demand + total_product_start - total_product_end)
    print('Normalized Operating Cost [ operating cost: {}, total demand: {}, initial total product: {}, end total product: {} ]: {}'
          .format(truck_operating_cost, total_demand, total_product_start, total_product_end, normalized_operating_cost))


# Get total cost with equipment cost and normalized operating cost
def get_total_cost():
    total_cost = get_equipment_cost() + get_normalized_operating_cost()
    print('Total Cost: {}'.format(total_cost))
    return total_cost
