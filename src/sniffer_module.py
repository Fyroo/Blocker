import os
from scapy.all import *

class PacketSniffer:
    def __init__(self, queue, stop_event, selected_interface):
        self.queue = queue
        self.stop_event = stop_event
        self.selected_interface = selected_interface
        self.blocklist_files = {
            "ADS": "Blocker/data/ads_domains.txt",
            "NSFW": "Blocker/data/nsfw_domains.txt",
        }
        self.blocklists = self.load_blocklists()

    def load_blocklists(self):
        blocklists = {}
        for category, filepath in self.blocklist_files.items():
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    blocklists[category] = set(line.strip() for line in file)
            else:
                print(f"Blocklist file not found: {filepath}")
                blocklists[category] = set()
        return blocklists

    def flag_domain(self, domain_name):
        for category, domains in self.blocklists.items():
            if domain_name in domains:
                return category
        return "SAFE"

    def proc_packet(self, p):
        if p.haslayer(DNS) and p.haslayer(DNSRR):
            dns_layer = p.getlayer(DNS)
            if dns_layer.an:
                resolved_ip = dns_layer.an.rdata
                dns_query = dns_layer.qd.qname.decode("utf-8").rstrip(".")

                flag = self.flag_domain(dns_query)

                data = {
                    "domain_ip": resolved_ip,
                    "domain_name": dns_query,
                    "flag": flag,
                }
                self.queue.put(data)

    def start_sniffing(self):
        sniff(
            iface=self.selected_interface,
            filter="udp port 53",
            prn=lambda p: self.proc_packet(p),
            stop_filter=lambda x: self.stop_event.is_set(),
        )
