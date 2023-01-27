from censys.search import CensysHosts
import re

hosts = CensysHosts()

versionMetaTag = re.compile(r"ajs-version-number") 
versionNumber = re.compile(r"\d+\.\d+\.\d+")

searchme = "location.country_code: CN and \
        services.http.response.headers.Server: nginx and \
        services.banner: Confluence and \
        services.http.response.status_code: 200"

query = hosts.search(query=searchme, per_page=100, virtual_hosts="INCLUDE")

handle = open("report.txt", "a")
protocols = dict()
ports = dict()
versions = dict()

for ip, attrs in query.view_all().items():
    print(ip + ":")
    handle.write(ip + "\n")
    confluenceVersion = None
    protocol = None
    for service in attrs["services"]:
        serviceCount = 0
        portReadout = "    Port: {}".format(service["port"]) 
        protocol = service["extended_service_name"]
        protocolReadout = "    Protocol: {}".format(protocol)
        if "http" in service.keys():
            if "html_tags" in service["http"]["response"].keys():
                for tag in service["http"]["response"]["html_tags"]:
                    if re.search(versionMetaTag, tag):
                        versionNo = re.search(versionNumber, tag)
                        if versionNo:
                            confluenceVersion = versionNo[0]
                            versions[confluenceVersion] = versions.get(confluenceVersion, dict())
                            versions[confluenceVersion]["services"] = versions[confluenceVersion].get("services", 0) + 1
                            versionNoReadout = "    Confluence version no: {}".format(confluenceVersion) 
                            print(versionNoReadout)
                            print(portReadout)
                            print(protocolReadout)
                            protocols[service["extended_service_name"]] = protocols.get(service["service_name"], 0) + 1
                            handle.writelines([versionNoReadout + "\n",portReadout + "\n",protocolReadout + "\n"])
    if confluenceVersion and protocol in ["HTTP", "HTTPS"]:
        versions[confluenceVersion]["hosts"] = versions[confluenceVersion].get("hosts", dict())
        versions[confluenceVersion]["hosts"][protocol] = versions[confluenceVersion]["hosts"].get(protocol, 0) + 1

print("Confluence versions:")
handle.write("Confluence versions \n")
for version, stats in versions.items():
    versionLine = "    {}".format(version)
    print(versionLine)
    handle.write(versionLine + "\n")
    if "hosts" in stats.keys():
        hostLine = "        Hosts:"
        print(hostLine)
        handle.write(hostLine + "\n")
        for protocol, count in stats["hosts"].items():
            protocolLine = "            {}: {}".format(protocol, count)
            print(protocolLine)
            handle.write(protocolLine + "\n")
    servicesLine = "    Services: {}".format(stats["services"])
    print(servicesLine)
    handle.write(servicesLine + "\n")

            
    
