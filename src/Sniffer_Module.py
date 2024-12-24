from scapy.all import *

def procPacket(p, queue):
    if p.haslayer(DNS) and p.haslayer(DNSRR):  
        dns_layer = p.getlayer(DNS)
        if dns_layer.an:  
            resolved_ip = dns_layer.an.rdata  
            dns_query = dns_layer.qd.qname.decode('utf-8') 
            
            data = {
                "domain_ip": resolved_ip,
                "domain_name": dns_query,
            }
            queue.put(data)  

def start_sniffing(queue, stop_event, selected_interface):
    sniff(
        iface=selected_interface,
        filter="udp port 53",
        prn=lambda p: procPacket(p, queue),
        stop_filter=lambda x: stop_event.is_set()
    )
