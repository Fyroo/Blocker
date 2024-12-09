from scapy.all import *

def list_interfaces():
    interfaces = []
    for iface_id, iface_data in conf.ifaces.items():
        interfaces.append(iface_data.name) 
    return interfaces
