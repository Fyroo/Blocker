import socket
import dnslib
import threading
import os 

class DNSServer:
    def __init__(self, upstream_dns="8.8.8.8", blocklist_file=None):
        self.upstream_dns = upstream_dns
        self.blocked_domains = self.load_blocklist(blocklist_file)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 53))

    def load_blocklist(self, file_path):
        blocklist = set()
        try:
            with open(file_path, "r") as f:
                for line in f:
                    domain = line.strip()
                    if domain:
                        blocklist.add(domain)
            print(f"Loaded {len(blocklist)} blocked domains:")
        except FileNotFoundError:
            print(f"Blocklist file not found: {file_path}")
        except Exception as e:
            print(f"Error loading blocklist: {e}")
        return blocklist

    def resolve_dns(self, query):
        """Resolve DNS query or block it based on the blocklist."""
        qname = str(query.q.qname).rstrip('.')
        print(f"Received query: {qname}")
        if qname in self.blocked_domains:
            # Create response pointing to localhost
            print(f"Blocked domain: {qname}")
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

if __name__ == "__main__":
    
    data = os.path.join("Blocker", "data", "ads_domains.txt") 

    server = DNSServer(blocklist_file=data)
    server.run()
