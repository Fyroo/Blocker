# 🔴 Blocker - DNS Blocker Server

## Overview

**Blocker** is a Python-based DNS server designed to block specific domains (e.g., ads, malware, adult content) by redirecting them to a local address (`127.0.0.1`). The program provides:

- **Custom Blocklist Management**: Easily add or update blocked domains.
- **Platform Support**: Works on Linux and Windows.
- **DNS Fallback**: Forwards unresolved domains to upstream DNS servers like Google DNS (`8.8.8.8`).
- **Network Packet Sniffer**: Monitors DNS queries for improved diagnostics.

## Features

- **Customizable Blocklists**
- **Logs for Debugging**
- **Platform-Specific DNS Setup**
- **Configurable via GUI**

## Prerequisites

Ensure your system meets the following requirements:

- **Python**: Version 3.x.
- **Privileges**: Administrative/root access for DNS configuration.
- **Npcap**: latest version(for Windows only)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Fyroo/Blocker.git
cd Blocker
```

### 2. Start the Program

**Linux**:

```bash
bash run_linux.sh
```

**Windows**:

```cmd
run_windows.bat
```

If setup hasn’t been completed, the `run` scripts will automatically invoke the appropriate `setup` script.

## Configuration

### Blocklist Management

The blocklist files are located in the `data/` directory:

- `nsfw_domains.txt`: Block adult content.
- `ads_domains.txt`: Block ads and trackers.

To add a domain, simply append it to the relevant file, one domain per line.

### Logs

Logs are stored in the `logs/` directory. These can be reviewed to troubleshoot issues or monitor activity.

### GUI Configuration

The GUI provides options to:

- View and update blocklists.
- view live dns traffic on disered interface
- Adjust auto-update settings for blocklists.
- Monitor DNS query activity.

## How It Works

1. **DNS Query Interception**: Captures incoming DNS queries.
2. **Domain Filtering**: Checks the queried domain against the blocklist.
3. **Blocking**: Returns `127.0.0.1` for blocked domains.
4. **Forwarding**: Unblocked domains are forwarded to the upstream DNS server (`8.8.8.8` by default).

## DNS Configuration

### Linux

The script modifies `/etc/resolv.conf` to use `127.0.0.1` as the primary DNS server:

```bash
nameserver 127.0.0.1
```

**Note**: If `NetworkManager` or `systemd-resolved` overwrites this file, you may need to disable automatic DNS updates.

### Windows

The script uses the `netsh` command to set `127.0.0.1` as the DNS server:

```cmd
netsh interface ip set dns "Local Area Connection" static 127.0.0.1
```

## Troubleshooting

### Chrome Secure DNS Issue

Chrome’s Secure DNS feature may bypass the local DNS server. To fix this:

1. Go to Chrome settings: `chrome://settings/`
2. Navigate to **Privacy and security**.
3. Disable **Use secure DNS** under **Security**.

### Permission Errors

If you encounter permission errors, ensure you run the setup or run scripts with elevated privileges:

- **Linux**: Use `sudo`.
- **Windows**: Run the batch files as an administrator.

## Project Structure

```
. 📂 Blocker
├── 📄 README.md
├── 📂 data/
│   ├── ads_domains.txt
│   ├── config.json
│   ├── nsfw_domains.txt
├── 📂 logs/
├── 📄 requirements.txt
├── 📄 run_linux.sh
├── 📄 run_windows.bat
├── 📄 setup_linux.sh
├── 📄 setup_windows.bat
├── 📂 src/
│   ├── __main__.py
│   ├── configuration_interface.py
│   ├── configuration_module.py
│   ├── dashboard_interface.py
│   ├── dns_resolver_interface.py
│   ├── dns_resolver_module.py
│   ├── domain_fetch_module.py
│   ├── interface_list_module.py
│   ├── logger_module.py
│   ├── setdns_module.py
│   ├── sniffer_interface.py
│   ├── sniffer_module.py
└── 📂 venv/
```

## Contributing

Feel free to submit issues or pull requests to improve this project. Contributions are welcome!
