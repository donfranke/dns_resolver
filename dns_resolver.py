# dns resolver

# gets hostname for list of IP addresses
# created because we have more than 1 authoritative DNS server, 
#   each with different DNS records
# this consolidates them all and adds some metadata to each record

# prerequisites:
#    list of all hostname prefixes and corresponding location
#    dns records in CSV format

import csv
import sys
import socket

# locations
allColos = []

class Colo:
	acronym = ""
	city = ""
	state = ""
	country = ""

	def __init__(self,a,b,c,d):
		self.acronym = a
		self.city = b
		self.state = c
		self.country = d

# populate allColos lookup array with hostname prefix and location information
# this is helpful if the hostname format is consistent

# example hostnames: 
#   CHI-LAB01
#   DVR-TEST03
#   TRN-PROD06

# example corresponding array entries:
#    allColos.append(Colo("CHI","Chicago","IL","US"))
#    allColos.append(Colo("DVR","Denver","CO","US"))
#    allColos.append(Colo("TRN","Toronto","-","CN"))

# open DNS csv files and loads into memory arrays
dnsAll = []

# create dns class object
class DNSRecord:
	ipaddr = ""
	hostname = ""
	source=""

	def __init__(self, a, b, c):
		self.ipaddr = a
		self.hostname = b
		self.source = c
		
# search DNS array for match
def findHostname(inIP):
	foundEntry = DNSRecord("127.0.0.1","unresolved","NA")
	for dEntry in dnsAll:
		if dEntry.ipaddr==inIP:
			#print str(i) + " " + dEntry.ipaddr + " " + dEntry.hostname
			foundEntry = dEntry
			break
	
	return foundEntry

# find match in allColos array
def findColo(inLoc):
	foundLoc = Colo("na","unknown","NA","NA")
	for dLoc in allColos:
		if(dLoc.acronym==inLoc):
			foundLoc = dLoc
			break

	return foundLoc

# load DNS1 records
with open('dns1.csv') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		hostname = row[2]
		if(hostname!="@"):
			d1 = DNSRecord(row[7],hostname,"DNS1")
			#print row[7].strip(' \t\n\r') + "," + row[2].strip(' \t\n\r')
			dnsAll.append(d1)

csvfile.close()

# load DNS2 records
with open('dns2.csv') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		hostname = row[2]
		if(hostname!="@"):
			d1 = DNSRecord(row[7],hostname,"DNS2")
			#print row[7].strip(' \t\n\r') + "," + row[2].strip(' \t\n\r')
			dnsAll.append(d1)

csvfile.close()

# load DNS3 records
with open('dns3.csv') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		hostname = row[2]
		if(hostname!="@"):
			d1 = DNSRecord(row[7],hostname,"DNS3")
			#print row[7].strip(' \t\n\r') + "," + row[2].strip(' \t\n\r')
			dnsAll.append(d1)

csvfile.close()

print len(dnsAll)," DNS records loaded\n"

# iterate list of ip addresses and try to resolve them using arrays in memory
# csv format: [ip address],[mac address],[colocode]
fIPList = open('iplist.csv')
i = 0
for line in fIPList:
	l = line.split(',')
	ipaddr = l[0]
	colocode = l[2].strip(' \t\n\r')
	mac = l[1]
	sa = findHostname(ipaddr)
	colo = findColo(colocode)
	print ipaddr + "," + mac + ","+ str(sa.hostname) + "," + colocode + "," + colo.city + "," + colo.state + "," + colo.country
	i = i + 1

fIPList.close()
