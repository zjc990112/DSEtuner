#!/usr/bin/env python
import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', help="input a json file for design parameter")

def temporary_calculator(parameter):
    res = 0
    for key, value in parameter.items() :
            for setting_key, setting_value in value.items() :
                if isinstance(setting_value, int):
                    res += setting_value
    return res

if __name__ == '__main__':
    args = parser.parse_args()
    parameter = json.load(open(args.data,"r"))
    res = {
        "performance" : temporary_calculator(parameter)
    }
    jsonString = json.dumps(res, indent = 4)
    print(jsonString)

