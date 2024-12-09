from scapy.all import *
import socket

def resolve_domain(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

def procPacket(p, queue):
    if p.haslayer(IP) and p.haslayer(UDP) and p.haslayer(DNS) and p.haslayer(DNSQR):
        ip_layer = p.getlayer(IP)
        dns_layer = p.getlayer(DNS)
        dns_query = dns_layer.qd.qname.decode('utf-8')  

        data = {
            "domain_ip": ip_layer.dst,  
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
