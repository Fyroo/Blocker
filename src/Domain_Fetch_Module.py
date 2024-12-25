import requests
import os

def fetch_domains():
    url_ads = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/domains/multi.txt"
    url_nsfw = "https://nsfw.oisd.nl/simplednsplusdblpi"
    
    try:
        data_directory = os.path.join("Blocker", "data") 
        os.makedirs(data_directory, exist_ok=True)  

        response_ads = requests.get(url_ads)
        response_ads.raise_for_status()  
        response_nsfw = requests.get(url_nsfw)
        response_nsfw.raise_for_status()  

        ads_ads = response_ads.text.splitlines()                        
        nsfw_list = response_nsfw.text.splitlines()

        ads_ads = [line for line in ads_ads if line and not line.startswith("#")]
        nsfw_list = [line.split(" ", 1)[1] for line in nsfw_list if line.startswith("E ") and not line.startswith("#")]

        ads_domains_file = os.path.join(data_directory, "ads_domains.txt")
        nsfw_list_file = os.path.join(data_directory, "nsfw_domains.txt")
        
        with open(nsfw_list_file, "w") as file:
            for domain in nsfw_list:
                file.write(f"{domain}\n")
        
        with open(ads_domains_file, "w") as file:
            for domain in ads_ads:
                file.write(f"{domain}\n")
        
    except requests.RequestException as e:
        print(f"Error fetching domain list: {e}")


fetch_domains()