#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


class Timeline:
    event_list = []

    def record_truck_event(self, event):
        self.event_list.append(event)

    def get_output(self):
        print()

