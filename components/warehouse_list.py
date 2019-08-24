#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


class WarehouseList:
    warehouse_list = []
    total_warehouse_purchase_cost = 0

    def set_warehouse_list(self, warehouse_list):
        self.warehouse_list = warehouse_list

    # Create record in warehouse list
    def append_warehouse_record(self, warehouse):
        self.warehouse_list.append(warehouse)

    # Check inventory in all warehouse
    def update_all_warehouse_inventory(self, timestamp):
        for warehouse in self.warehouse_list:
            warehouse.update_current_inventory(timestamp)

    # Get total warehouse purchase cost from all warehouse object
    def get_total_warehouse_purchase_cost(self):
        for warehouse in self.warehouse_list:
            self.total_warehouse_purchase_cost = self.total_warehouse_purchase_cost + warehouse.get_warehouse_purchase_cost()
        print('All warehouse purchase cost: {}'.format(self.total_warehouse_purchase_cost))
        return self.total_warehouse_purchase_cost
