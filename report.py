from censys.search import CensysHosts
import re

hosts = CensysHosts()

# The host in question has a handful of interesting attributes.
servicesHttpHeaderServer = "nginx"
portNumber = 80
portService = "HTTP"
softwareUpper = "Confluence"
softwareLower = "confluence"
metaIdentifier = "ajs"
versionMetaTag = re.compile(r'"ajs-version-number" content="\d+\.\d+\.\d+"')

def walk(d, i):
    for key, value in d.items():
        if isinstance(value, dict):
            print("    " * i + key + ":")
            walk(value, i + 1)
        else:
            print("    " * i + key + ": " + value)

searchme = "location.country_code: CN and services.service_name: HTTP and \
        services.http.response.headers.Server: nginx and services.port: 80 and \
        services.banner: Confluence and services.http.response.status_code: 200"

query = hosts.search(query=searchme, per_page=50, virtual_hosts="EXCLUDE")

handle = open("readouts", "a")
protocols = dict()
ports = dict()
versions = dict()

for ip, attrs in query.view_all().items():
    print(ip + ":")
    handle.write(ip + "\n")
    for service in attrs["services"]:
        if service["port"] == 80 or service["port"] == 443:
            portReadout = "   Port:" + service["port"] 
            print(portReadout)
            handle.write(portReadout + "\n")
            ports[service["port"]]
            protocolReadout = "   Protocol:" + service["service_name"]
            print(protocolReadout)
            protocols.get(service["service_name"])
            protocols[service["service_name"]] += 1
            handle.write(protocolReadout + "\n")
            
    
