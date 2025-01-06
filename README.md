````markdown
# 🛑 Blocker - DNS Blocker Server

## Overview

**Blocker** is a DNS server designed to block specific domains (e.g., ads, malware, adult content) by redirecting them to a local address (e.g., `127.0.0.1`). The server allows you to maintain a custom blocklist and provides fallback resolution via upstream DNS servers like Google DNS when the domain is not blocked. This is particularly useful for network filtering, parental control, and privacy enhancement.

## Prerequisites

Before you start, ensure that your environment is ready:

- **Python**: Python 3.x is required.
- **Virtual Environment**: It is recommended to use a virtual environment for dependency management.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Fyroo/Blocker.git
cd blocker
```
````

### 2. Set Up a Virtual Environment

Create and activate a virtual environment to manage your dependencies:

```bash
python -m venv venv
```

- For Linux/macOS:

```bash
source venv/bin/activate
```

- For Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required libraries using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configure the Blocklist

The server uses a `nsfw_domains.txt` file to maintain the list of domains to block. You can find this file under the `data` directory.

Each domain should be listed on a separate line. The server will check incoming DNS queries against this list and block matching domains.

### 5. Run the DNS Server

Start the DNS server by running the following command:

```bash
python blocker/dns_server.py
```

The server will start listening on `127.0.0.1:53` and will block any domains listed in `domains.txt`. Any other domains will be forwarded to the configured upstream DNS server (Google DNS by default: `8.8.8.8`).

## Project Structure

```
└── 📂 Blocker/
│  └── 📂 data/
│    ├── 📄 ads_domains.txt
│    ├── 📄 config.json
│    ├── 📄 nsfw_domains.txt
├── 📄 README.md
└── 📂 data/
├── 📄 requirements.txt
└── 📂 src/
│  ├── 📄 __main__.py
│  ├── 📄 configuration_interface.py
│  ├── 📄 configuration_module.py
│  ├── 📄 dashboard_interface.py
│  ├── 📄 dns_resolver_interface.py
│  ├── 📄 dns_resolver_module.py
│  ├── 📄 domain_fetch_module.py
│  ├── 📄 interface_list_module.py
│  ├── 📄 sniffer_interface.py
│  └── 📄 sniffer_module.py
```

## How It Works

1. **Domain Query**: When a DNS query is received, the server checks if the requested domain matches any in the blocklist (`*_domains.txt`).
2. **Block Domain**: If the domain is found in the blocklist, the server responds with the IP `127.0.0.1`, effectively blocking the domain.
3. **Forward to Upstream DNS**: If the domain is not in the blocklist, the server forwards the query to the configured upstream DNS server (e.g., `8.8.8.8`).

## Known Issues

### **Chrome Secure DNS Issue**

If the server is not capturing DNS queries from Chrome, it may be due to Chrome's Secure DNS feature. To fix this:

1. Open Chrome settings (`chrome://settings/`).
2. Scroll to **Privacy and security**.
3. Under **Security**, toggle off **Use secure DNS**.

Disabling Secure DNS will allow the packet sniffer to capture packets properly.
