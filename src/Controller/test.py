'''
from Scanner import *


devices = [device for device in run_scanner(8) if abs(int(device[2])) > 40]
#devices = [device for device in run_scanner_alive() if abs(int(device[2])) > 40]
print("found {}".format(len(devices)))
'''

import bluetooth
import select

class MyDiscoverer(bluetooth.DeviceDiscoverer):
    
    def pre_inquiry(self):
        self.done = False
    
    def device_discovered(self, address, device_class, rssi, name):
        print ("%s - %s -%s" % (address, name, rssi))
        

    def inquiry_complete(self):
        self.done = True

d = MyDiscoverer()
d.find_devices(lookup_names = True, duration=2,flush_cache=True)

readfiles = [ d, ]

while True:
    rfds = select.select( readfiles, [], [] )[0]

    if d in rfds:
        d.process_event()

    if d.done: break