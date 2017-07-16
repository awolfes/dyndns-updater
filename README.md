# dyndns-updater
Simple Python DynDNS Updater with VPN check and log

dyndns-updater checks the WAN IP against the IP of a DNS Name. If the two are different, it will connect to DynDNS and update the DNS IP with the WAN IP. If a VPN is currently connected, it will not update the DNS IP. Additionally, it will log the current status and IP to a log file. This script is useful if you regularly connect to a VPN and don't want your DNS IP to update when connected.

## **Instructions**

Constants at the top of the file:

    USERNAME = "userName"
    PASSWORD = "password123"
    DNS_NAME = "this.is.a.dns-name.com"
    LOG_PATH = "C:\DynDNS_log.csv"
    VPN_INTERFACE = "VPN Interface Name"
    
USERNAME - Log in name for DynDNS

PASSWORD - Password for log in for DynDNS

DNS_NAME - DNS name in question

LOG_PATH - Path and file name for log file

VPN_INTERFACE - The name of the VPN interface in "Network Connections", visible when typing the following in a command prompt in Windows:

    netsh interface show interface
