import urllib
import re
import socket
import json
import os
import re
import urllib
import urllib2
import sys
import datetime

USERNAME = "userName"
PASSWORD = "password123"
DNS_NAME = "this.is.a.dns-name.com"
LOG_PATH = "C:\DynDNS_log.csv"
VPN_INTERFACE = "VPN Interface Name"

#========================================================================

def get_external_ip_wtf():

    # Get the external WAN Ip address
    try:
        site = urllib.urlopen("http://wtfismyip.com/json").read()
        site_dict = json.loads(site)

#       print "IP Address: ", site_dict['YourFuckingIPAddress']
#       print "Location:   ", site_dict['YourFuckingLocation']
#       print "Hostname:   ", site_dict['YourFuckingHostname']
#       print "ISP:        ", site_dict['YourFuckingISP']

    except Exception, e:
        return e

    return site_dict['YourFuckingIPAddress']

#========================================================================

def compare_ip(dyn_name):
    
    # Get IP address from dyn_name
    try:
        dyn_ip = socket.gethostbyname(dyn_name)
    except Exception, e:
        return e

    # Get external WAN IP Address
    try:
        ip = get_external_ip_wtf()
    except Exception, e:
        return e

    # Check for valid string
    if type(ip) != unicode:
        return ip

    print "DynDNS Name:", dyn_name
    print "DynDNS IP:  ", dyn_ip
    print "Actual IP:  ", ip

    # Check if IP addresses are the same
    if dyn_ip == ip:
        print "Same\n"
        return True
    else:
        print "Different\n"
        return False

#========================================================================

def list_interfaces():
    
    # use netsh to get a list of interfaces
    data = os.popen("netsh interface show interface").read()
    data = [s.strip() for s in data.splitlines()]
    data = data[3:-1]
    new_data = [re.split(r'\s{2,}', s) for s in data]
    interfaces = [[s[i] for i in (3, 1)] for s in new_data ]

    return interfaces

#========================================================================

def check_connected(interface):
    
    # Check to see if an interface is connected
    for i in list_interfaces():
        if i[0] == interface:
            if i[1] == "Connected":
                return True
    return False                

#========================================================================

def update_ip(host_name, new_ip):

    # Update DynDNS with new IP address
    try:
        params = urllib.urlencode({'hostname': host_name, "myip": new_ip})
        url = 'http://members.dyndns.org/nic/update?%s' % params
        
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None,url , USERNAME, PASSWORD)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        pagehandle = urllib2.urlopen(url)

        return True
        
    except Exception, e:
        print "Error: " + str(e)

        return e
    
#========================================================================

def write_log(vpn, status):

    path = LOG_PATH

    # Add header row if file is new
    if not os.path.isfile(path):
        header = "Date, Time, VPN, Status\n\n"
    else:
        header = ""

    # Get current date and time
    d = datetime.datetime.now()

    # Extract date and time
    date = d.strftime("%A %B %d %Y")
    time = d.strftime("%I:%M:%S %p")

    # Write entry to log file
    with open (path, 'a') as log_file:
        log_file.write(header)
        message = date + "," + time + "," + vpn + "," + status + "\n"
        log_file.write(message)
        
#========================================================================

if __name__ == '__main__':

#    write_log("Disconnected", "Periodic updater test")
#    print os.getcwd()
#    sys.exit()

    # Check if connected to VPN
    if check_connected(VPN_INTERFACE):
        print "VPN Connected"
        write_log("Connected", "")

    else:
        print "VPN Disconnected"

        # Compare current WAN IP with DNS IP
        compare = compare_ip(DNS_NAME)

        # Check for valid data
        if type(compare) != bool:
            print "Problem with internet connection"
            print "Error: " + str(compare)            
            write_log("Disconnected", "Error: " + str(compare))
            
        else:
            # Get WAN IP (should be OK)
            wan_ip = get_external_ip_wtf()
                
            # If IPs are the same, do not update DynDNS
            if compare:
                print "IPs are the same"
                write_log("Disconnected", "IPs are the same. No update required. (" + wan_ip + ")")

            else:
                print "IPs are different"

                # Update DynDNS
                if update_ip(DNS_NAME, wan_ip):
                    print "DynDNS has been updated"
                    write_log("Disconnected", "IPs are different. DynDNS Updated. New IP: " + wan_ip)
                else:
                    print "Error updating DynDNS"
                    write_log("Disconnected", "Error: " + str(compare))

