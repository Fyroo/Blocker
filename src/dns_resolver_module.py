import socket
import dnslib
import threading
from datetime import datetime
import os
import json

class DNSServer:
    def __init__(self, upstream_dns="8.8.8.8", save_file="Blocker/data/block_counts.json"):
        self.upstream_dns = upstream_dns
        self.blocked_domains = set()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 53))
        self.blocklist_files = {}

        # Block counters
        self.daily_blocks = 0
        self.monthly_blocks = 0
        self.last_reset_date = datetime.now()

        # File to save block counts
        self.save_file = save_file
        self.blocking_enabled = False  # Initially, blocking is off

        # Load previous counts
        self.load_counts()

    def load_counts(self):
        """Load the daily and monthly block counts from a file."""
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
        """Save the daily and monthly block counts to a file."""
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
        """Update the blocked domains based on selected categories."""
        self.blocked_domains.clear()
        for category, file_path in self.blocklist_files.items():
            if category in categories:
                self.blocked_domains.update(self.load_blocklist(file_path))
        print(f"Blocking {len(self.blocked_domains)} domains.")

    def reset_counters_if_needed(self):
        """Reset daily and monthly counters if needed."""
        now = datetime.now()
        if now.date() != self.last_reset_date.date():
            self.daily_blocks = 0
        if now.month != self.last_reset_date.month:
            self.monthly_blocks = 0
        self.last_reset_date = now

    def resolve_dns(self, query):
        """Resolve DNS query or block it based on the blocklist."""
        self.reset_counters_if_needed()

        qname = str(query.q.qname).rstrip('.')
        qname = qname.removeprefix('www.')
        print(f"Received query: {qname}")
        if qname in self.blocked_domains and self.blocking_enabled:
            # Increment counters
            self.daily_blocks += 1
            self.monthly_blocks += 1
            print(f"Blocked domain: {qname}")

            # Save counts after blocking a domain
            self.save_counts()

            # Create response pointing to localhost
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
            return response

        # Resolve the DNS query via the upstream DNS (8.8.8.8)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(query.pack(), (self.upstream_dns, 53))
            data, _ = sock.recvfrom(4096)
            return dnslib.DNSRecord.parse(data)
        except Exception as e:
            print(f"Error resolving {qname}: {e}")
            return None
        finally:
            sock.close()

    def handle_request(self, data, addr):
        """Handle incoming DNS request."""
        try:
            query = dnslib.DNSRecord.parse(data)
            response = self.resolve_dns(query)
            if response:
                self.sock.sendto(response.pack(), addr)
        except Exception as e:
            print(f"Error handling request: {e}")

    def run(self):
        """Run the DNS server."""
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
