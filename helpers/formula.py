#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


# Get equipment cost with total truck and warehouse purchase cost
def get_equipment_cost(truck_list, warehouse_list):
    total_truck_purchase_cost = truck_list.get_total_truck_purchase_cost()
    total_warehouse_purchase_cost = warehouse_list.get_total_warehouse_purchase_cost()
    equipment_cost = total_truck_purchase_cost + total_warehouse_purchase_cost
    print('Equipment Cost: {}'.format(equipment_cost))


# Get normalized operating cost with total truck operating cost, total demand, initial total products and end total products
def get_normalized_operating_cost(truck_list, total_demand, total_product_start, total_product_end):
    total_truck_operating_cost = truck_list.get_total_truck_operating_cost()
    normalized_operating_cost = total_truck_operating_cost * total_demand / (total_demand + total_product_start - total_product_end)
    print('Normalized Operating Cost [ operating cost: {}, total demand: {}, initial total product: {}, end total product: {} ]: {}'
          .format(total_truck_operating_cost, total_demand, total_product_start, total_product_end, normalized_operating_cost))


# Get total cost with equipment cost and normalized operating cost
def get_total_cost():
    total_cost = get_equipment_cost() + get_normalized_operating_cost()
    print('Total Cost: {}'.format(total_cost))
    return total_cost
