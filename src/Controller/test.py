from Scanner import *


devices = [device for device in run_scanner(10,True) if abs(int(device[2])) > 40]
print("found {}".format(len(devices)))