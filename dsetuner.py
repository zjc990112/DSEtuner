#!/usr/bin/env python
# This is a simple testcase purely for testing the autotuner on permutations
#
# http://en.wikipedia.org/wiki/Travelling_salesman_problem
#

import argparse
import json
import sys
import math
import subprocess
import os
import opentuner
from opentuner.measurement import MeasurementInterface
from opentuner.search.manipulator import (ConfigurationManipulator, 
                                        EnumParameter, 
                                        IntegerParameter)
# from opentuner.search.objective import MaximizeAccuracy
from opentuner.search.objective import *
from opentuner.measurement.inputmanager import FixedInputManager


parser = argparse.ArgumentParser(parents=opentuner.argparsers())
parser.add_argument('-d', '--setting', dest='setting_file', default="setting.json", 
    help="a json contain the parameter file.\
        setting.json in the same directory by default" )
parser.add_argument('--simulator',  dest = 'simulator_file', default="./simulator.py",
    help="the executable file to calculate performace. \
        or the file \'simulator.py\' in the same directory by default" )

class DSE(MeasurementInterface):
    def __init__(self, args):
        super(DSE, self).__init__(args, 
            objective=MinimizeTime(),
            input_manager=FixedInputManager())
        self.setting = json.load(open(args.setting_file, "r"))
        self.simulator_file = args.simulator_file

    def run(self, desired_result, input, limit):
        cfg = desired_result.configuration.data
        
        data = self.construct_dict(cfg)
        performance = self.simulate_performance(data)
        return opentuner.resultsdb.models.Result(time=performance)

    def construct_dict(self, cfg, use_unit=False):
        data = {}
        for key, value in self.setting.items() :
            # print(f"getting parameter for {key}")
            data[key] = {}
            for setting_key, setting_value in self.setting[key].items() :
                # print(f"--getting parameter {setting_key}")
                if isinstance(setting_value,list):
                    data[key][setting_key] = cfg[setting_key]
                    # print(f"----get {cfg[setting_key]}")
                elif isinstance(setting_value, dict):
                    i = setting_value["initial value"]
                    s = setting_value["scale"]
                    number = cfg[setting_key]
                    res = 0
                    # print(f"----get number is {number}")
                    if setting_value["style"] == "linear":
                        res = i + s * number
                    elif setting_value["style"] == "exponential":
                        res= i * pow(s, number)
                        if res > setting_value["end value"]:
                            raise ValueError("opentuner give a wrong value?")
                    if use_unit :
                        if "unit" in setting_value.keys():
                            data[key][setting_key] = f"{res} {setting_value['unit']}"
                        else :
                            data[key][setting_key] = f"{res}"
                    else :
                        data[key][setting_key] = res
                    #print(f"----get {data[key][setting_key]}")
        return data
    def simulate_performance(self, data):
        """ run a simulator with a selected data by tunner """
        file_name = "temp.json"
        s = json.dumps(data, indent=4)
        jsonFile = open(file_name, "w")
        jsonFile.write(s)
        jsonFile.close()
        raw_data = subprocess.run([self.simulator_file, file_name], capture_output=True)
        #print(f"get err {raw_data.stderr}")
        #print(f"get raw data {raw_data.stdout}")
        performance = json.loads(raw_data.stdout)["performance"]
        
        # os.remove(file_name)
        #print(f"get a performance number of {performance}")
        return performance

    def manipulator(self):
        m = ConfigurationManipulator()
        for key, value in self.setting.items() :
            #print(f"setting parameter for {key}")
            for setting_key, setting_value in self.setting[key].items() :
                #print(f"--setting parameter {setting_key}")
                if isinstance(setting_value,list):
                    m.add_parameter(EnumParameter
                    (setting_key, setting_value))
                    #print(f"set a enumparameter {setting_key}, {setting_value}")
                elif isinstance(setting_value, dict):
                    i = setting_value["initial value"]
                    e = setting_value["end value"]
                    s = setting_value["scale"]
                    number = 0
                    if setting_value["style"] == "linear":
                        number = (e - i) // s
                    elif setting_value["style"] == "exponential":
                        number = int(math.log(e / i, s)) 
                    else:
                        raise ValueError("wrong value scaling style!")
                    m.add_parameter(IntegerParameter
                    (setting_key, 0, number))
                    #print(f"set a integerparameter {setting_key}, {number}")
                    
        # sys.exit(0)
        return m
    def save_final_config(self, configuration):
        data = self.construct_dict(configuration.data, use_unit = True)
        jsonFile = open("best_result.json", "w")
        jsonFile.write(json.dumps(data, indent=4))
        jsonFile.close()

if __name__ == '__main__':
    args = parser.parse_args()
    DSE.main(args)