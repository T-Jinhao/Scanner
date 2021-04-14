#!/usr/bin/python3
# -*- coding:utf8 -*-
#author:Jinhao

from interactive.run import common
from lib import func_ports

class port(common.Common):
    def run(self, Info):
        ports = self.getPorts(Info['Ports'][1])
        r = func_ports.Ports(
            host=Info['Ip'][1],
            name=Info['Taskname'][1],
            flag=0
        )
        r.load_config()
        report = r.run(port=ports)
        r.showReport(report)

    def getPorts(self, input):
        if input == 'Common':
            ports = func_ports.port_dict.keys()
        else:
            minus = input.split('-')
            interval = input.split(',')
            if len(minus) > 1:
                ports = [i for i in range(int(minus[0]), int(minus[1])+1)]
            else:
                ports = interval
        return ports
