#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


class TruckList:
    truck_list = []
    total_truck_purchase_cost = 0
    total_truck_operating_cost = 0

    # Create record in truck list after purchased new truck
    def purchase_new_truck(self, truck):
        self.truck_list.append(truck)

    # Get total truck purchase cost from all truck object
    def get_total_truck_purchase_cost(self):
        for truck in self.truck_list:
            self.total_truck_purchase_cost = self.total_truck_purchase_cost + truck.get_truck_purchase_cost()
        print('All Truck Purchase Cost: {}'.format(self.total_truck_purchase_cost))

    # Get total truck operating cost from all truck object
    def get_total_truck_operating_cost(self):
        for truck in self.truck_list:
            self.total_truck_operating_cost = self.total_truck_operating_cost + truck.get_truck_operating_cost()
        print('All Truck Operating Cost: {}'.format(self.total_truck_operating_cost))