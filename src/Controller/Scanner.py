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
        print('start')
        self.list_of_devices = []
        self.done = False
    
    def device_discovered(self, address, device_class,rssi,name):
        print ("%s - %s - %s" % (address, name, rssi))
        self.list_of_devices.append([address, name, rssi])

    def inquiry_complete(self):
        print("inquiry_complete")
        self.done = True

d = None
# function to scann bluetooth
def run_scanner(dur):
    global d
    d = MyDiscoverer()
    d.find_devices(lookup_names=True,duration=2, flush_cache=True)
    
    readfiles = [ d, ]
    
    while True:
        rfds = select.select( readfiles, [], [] )[0]
        if d in rfds:
            d.process_event()
        if d.done:
            break
    print('end scan')
    return d.list_of_devices

def run_scanner_alive():
    
    d = MyDiscoverer()
    d.find_devices(lookup_names = True, flush_cache=True)
    
    readfiles = [ d, ]
    
    while True:
        print("running")
        rfds = select.select( readfiles, [], [] )[0]
        
        if d in rfds:
            d.process_event()
            
        if d.done:
            status = True
            break
    print("return count")
    return d.list_of_devices

def end_inquiry():
    d.cancel_inquiry()

'''
print("run")
devices = run_scanner(2)
print("found {}".format(len(devices)))
''' 
    