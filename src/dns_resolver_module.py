import socket
import dnslib
import threading
from datetime import datetime
from configuration_module import ConfigHandler
import os
import json

class DNSServer:
    def __init__(self, config_handler: ConfigHandler, save_file="Blocker/data/block_counts.json"):
        self.config_handler = config_handler
        #self.upstream_dns = self.config_handler.config.get("upstream_dns.address", "8.8.8.8")
        #self.whitelist = set(self.config_handler.config.get("whitelist", []))
        #self.blacklist = set(self.config_handler.config.get("blacklist", []))
        self.lastqname = None

    
        self.config_file="Blocker/data/config.json"
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
                self.whitelist = set(self.config.get("whitelist", [])) 
                self.blacklist = set(self.config.get("blacklist", [])) 
                self.upstream_dns = self.config.get("upstream_dns", {}).get("address", "8.8.8.8")
                #self.dns_name = self.config.upstream_dns.get("name","Google")
                print(f"Loaded configuration: {self.config}")
        except Exception as e:
            print(f"Error loading configuration: {e}")
            self.config = {}



        self.blocked_domains = self.blacklist.copy()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 53))
        self.blocklist_files = {
        "ADS": "Blocker/data/ads_domains.txt",
        "NSFW": "Blocker/data/nsfw_domains.txt",
        }
        self.daily_blocks = 0
        self.monthly_blocks = 0
        self.last_reset_date = datetime.now()

        self.save_file = save_file
        self.blocking_enabled = False  

        self.load_counts()

    def load_counts(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.daily_blocks = data.get('daily_blocks', 0)
                    self.monthly_blocks = data.get('monthly_blocks', 0)
                    print(f"Loaded counts: Daily: {self.daily_blocks}, Monthly: {self.monthly_blocks}")
            except Exception as e:
                print(f"Error loading block counts: {e}")

    def save_counts(self):
        try:
            data = {
                'daily_blocks': self.daily_blocks,
                'monthly_blocks': self.monthly_blocks
            }
            with open(self.save_file, 'w') as f:
                json.dump(data, f)
            print(f"Saved counts: Daily: {self.daily_blocks}, Monthly: {self.monthly_blocks}")
        except Exception as e:
            print(f"Error saving block counts: {e}")

    def load_blocklist(self, file_path):
        """Load blocklist from a file."""
        blocklist = set()
        try:
            with open(file_path, "r") as f:
                for line in f:
                    domain = line.strip()
                    if domain:
                        blocklist.add(domain)
            print(f"Loaded {len(blocklist)} domains from {file_path}")
        except FileNotFoundError:
            print(f"Blocklist file not found: {file_path}")
        except Exception as e:
            print(f"Error loading blocklist: {e}")
        return blocklist

    def update_blocklist(self, categories):
        self.blocked_domains.clear()
        for category, file_path in self.blocklist_files.items():
            if category in categories:
                blocklist = self.load_blocklist(file_path)
                if blocklist:
                    self.blocked_domains.update(blocklist)
                else:
                    print(f"No domains loaded for category: {category}")
        print(f"Total domains to block: {len(self.blocked_domains)}")


    def reset_counters_if_needed(self):
        now = datetime.now()
        if now.date() != self.last_reset_date.date():
            self.daily_blocks = 0
        if now.month != self.last_reset_date.month:
            self.monthly_blocks = 0
        self.last_reset_date = now

    def resolve_dns(self, query):
        self.reset_counters_if_needed()

        qname = str(query.q.qname).rstrip('.')
        qname = qname.removeprefix('www.')
        print(f"Received query: {qname}")

        if qname in self.whitelist:
            print(f"Domain whitelisted: {qname}")
            return self.forward_query(query)    

        if qname in self.blocked_domains and self.blocking_enabled:
            if self.lastqname != qname:
                self.daily_blocks += 1
                self.monthly_blocks += 1
            print(f"Blocked domain: {qname}")
            self.save_counts()

            response = dnslib.DNSRecord(
                dnslib.DNSHeader(id=query.header.id, qr=1, aa=1, ra=1),
                q=query.q
            )
            response.add_answer(
                dnslib.RR(
                    qname,
                    rtype=dnslib.QTYPE.A,
                    rclass=dnslib.CLASS.IN,
                    ttl=300,
                    rdata=dnslib.A("127.0.0.1")
                )
            )
            self.lastqname = qname
            return response
        print(f"resloved domain with : {self.upstream_dns}")
        return self.forward_query(query)

    def forward_query(self, query):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(query.pack(), (self.upstream_dns, 53))
            data, _ = sock.recvfrom(4096)
            return dnslib.DNSRecord.parse(data)
        except Exception as e:
            print(f"Error forwarding query: {e}")
            return None
        finally:
            sock.close()

    def handle_request(self, data, addr):
        try:
            query = dnslib.DNSRecord.parse(data)
            response = self.resolve_dns(query)
            if response:
                self.sock.sendto(response.pack(), addr)
        except Exception as e:
            print(f"Error handling request: {e}")

    def run(self):
        print(f"DNS Server running on 127.0.0.1:53")
        print(f"Blocking {len(self.blocked_domains)} domains.")

        while True:
            try:
                data, addr = self.sock.recvfrom(4096)
                threading.Thread(
                    target=self.handle_request,
                    args=(data, addr)
                ).start()
            except Exception as e:
                print(f"Server error: {e}")