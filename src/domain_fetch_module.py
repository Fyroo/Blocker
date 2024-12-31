import requests
import os
import time

class DomainUpdater:
    def __init__(self, auto_update=True):
        self.auto_update = auto_update
        self.data_directory = os.path.join("Blocker", "data")
        os.makedirs(self.data_directory, exist_ok=True)

        self.ads_url = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/domains/multi.txt"
        self.nsfw_url = "https://nsfw.oisd.nl/simplednsplusdblpi"

    def fetch_domains(self):
        """Fetch and save domain block lists."""
        try:
            # Fetch Ads blocklist
            response_ads = requests.get(self.ads_url, timeout=10)
            response_ads.raise_for_status()

            # Fetch NSFW blocklist
            response_nsfw = requests.get(self.nsfw_url, timeout=10)
            response_nsfw.raise_for_status()

            ads_list = response_ads.text.splitlines()
            nsfw_list = [line.split(" ", 1)[1] for line in response_nsfw.text.splitlines()
                         if line.startswith("E ") and not line.startswith("#")]

            # Save Ads domains
            ads_file = os.path.join(self.data_directory, "ads_domains.txt")
            with open(ads_file, "w") as file:
                file.writelines(f"{domain}\n" for domain in ads_list if domain and not domain.startswith("#"))

            # Save NSFW domains
            nsfw_file = os.path.join(self.data_directory, "nsfw_domains.txt")
            with open(nsfw_file, "w") as file:
                file.writelines(f"{domain}\n" for domain in nsfw_list)

            print("Domain lists updated successfully.")

        except requests.RequestException as e:
            print(f"Error fetching domain lists: {e}")

    def update_loop(self):
        """Run update loop every 2 hours."""
        while self.auto_update:
            print("Updating domain lists...")
            self.fetch_domains()
            time.sleep(60*60*2)  
