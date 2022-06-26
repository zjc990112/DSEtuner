#!/usr/bin/env python
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', help="input a json file for design parameter")

# noc_bw = 32
noc_bw = 240

def temporary_calculator(parameter):
    res = 0
    for key, value in parameter.items() :
            for setting_key, setting_value in value.items() :
                if isinstance(setting_value, int):
                    res += setting_value
    return res


''
def get_performance(parameter):
    core_buffer_size = parameter["Core"]["buffer size"]
    core_buffer_bandwidth = parameter["Core"]["buffer bandwidth"]
    core_MAC_number = parameter["Core"]["MAC number"]
    core_NoC_bandwidth = parameter["Core"]["NoC bandwidth"]
    
    os.chdir("../focus_scheduler")
    os.system(f"python3 interface.py -bm benchmark/16_16.yaml -d 8 -b 8 -fr {noc_bw}-{noc_bw}-4 tesd --buffersize {core_buffer_size} --bufferbw {core_buffer_bandwidth} --macnum {core_MAC_number} --nocbw {noc_bw} > simulation.log")
    # os.system(f"python3 interface.py -bm benchmark/8_8.yaml -d 8 -b 8 -fr 1024-1024-512 tesd --buffersize {core_buffer_size} --bufferbw {core_buffer_bandwidth} --macnum {core_MAC_number} --nocbw {core_NoC_bandwidth} > simulation.log")
    # os.system(f"python3 interface.py -bm benchmark/small_test.yaml -d 4 -b 8 -fr {noc_bw}-{noc_bw}-4 tesd --buffersize {core_buffer_size} --bufferbw {core_buffer_bandwidth} --macnum {core_MAC_number} --nocbw {core_NoC_bandwidth} > simulation.log")
    os.chdir("../DSEtuner")
    f = open("../focus_scheduler/DSE_result.temp", "r")
    lines = f.readlines()
    return int(lines[0])

if __name__ == '__main__':
    args = parser.parse_args()
    parameter = json.load(open(args.data,"r"))

# for NoC bandwidth evaluation
    while noc_bw < 256:
        noc_bw += 16
        print("NoC bandwidth:", noc_bw, "Performance:", get_performance(parameter))

# for DSE
    # res = {
    #     # "performance" : temporary_calculator(parameter)
    #     "performance" : get_performance(parameter)
    # }
    # jsonString = json.dumps(res, indent = 4)
    # print(jsonString)
