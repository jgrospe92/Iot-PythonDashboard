import bluetooth

d = bluetooth.DeviceDiscoverer()
devices = d.find_devices(lookup_names=True, duration=4)

print(devices)