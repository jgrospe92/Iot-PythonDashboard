"""
PyBluez simple example asyncronous-inquiry.py
Demonstration of how to do asynchronous device discovery by subclassing
the DeviceDiscoverer class
Linux only (5/5/2006)
Author: Albert Huang <albert@csail.mit.edu>
Last Updated By: Jeffrey Grospe
Date-Modified: April 28 2023
$Id: asynchronous-inquiry.py 405 2006-05-06 00:39:50Z albert $
"""

import bluetooth
import select
 
class MyDiscoverer(bluetooth.DeviceDiscoverer):
    
    def pre_inquiry(self):
        self.list_of_devices = []
        self.done = False
    
    def device_discovered(self, address, device_class,rssi, name):
        print ("%s - %s - %s" % (address, name, rssi))
        self.list_of_devices.append([address, name, rssi])

    def inquiry_complete(self):
        self.done = True


# function to scann bluetooth
def run_scanner(dur, status):
    
    d = MyDiscoverer()
    d.find_devices(lookup_names = True, duration=dur, flush_cache=True)
    
    readfiles = [ d, ]
    
    while True:
        print("running")
        rfds = select.select( readfiles, [], [] )[0]
        
        if d in rfds:
            d.process_event()
            
        if d.done:
            status = True
            break
    
    return d.list_of_devices


if __name__ == "main":
    devices = run_scanner(8,True)
    print("found {}".format(len(devices)))
    


