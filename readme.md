# Censys take-home
Kyle Metscher | January 20, 2023

## 1: Determine service and version running on 114.119.117.220
At first glance, this appears to be a web server running NGINX, a highly popular web server and load balancer with a user-friendly configuration syntax, serving a typical web application. This is supported 
by Censys' recorded information on the host, specifically the services metadata collected under `services.software.vendor`, `services.product`, and `services.family` fields, and by preliminary port and service scanning 
using nmap (found under `scans`), which shows NGINX running on port 80, the same as Censys' data on `services.port`, which is the standard port for HTTP. Other common ports are closed, including 443 
for HTTPS, and 113 for IDENT. This server appears to be running a Linux-based operating system of some kind.

Further investigation points to the service in question actually being Atlassian Confluence, a workspace productivity platform for collaborative knowledge bases inspired by the "wiki" format. 
Confluence -- and most Atlassian software licensed for on-premise use -- typically hosts itself via Atlassian's Tomcat web server, making the appearance of NGINX notable. Metadata suggesting Confluence 
include myriad html meta tags detailing Atlassian-specific configurations with the signature "`ajs`", a title tag plainly reading "主页面 - Confluence", which would be expected of a host running in China
(as suggested by Censys' `location.country`, `location.registered_country`, and `location.timezone` metadata), and Confluence-specific data being passed in the HTTP response header (`Confluence-Request-Time` and a timestamp).
HTML metadata further suggest the version of Confluence running on this host is 7.13.2 in the tag `<meta name="ajs-version-number" content="7.13.2">`; Censys collected this under 
`services.http.response.html_tags`.

Using NGINX as a reverse proxy for Confluence is not an uncommon configuration scheme. Atlassian even provides basic instructions for [configuring Jira](https://confluence.atlassian.com/jirakb/configure-jira-server-to-run-behind-a-nginx-reverse-proxy-426115340.html)
(another Atlassian product often used alongside Confluence) and [Confluence specifically](https://confluence.atlassian.com/confkb/how-to-use-nginx-to-proxy-requests-for-confluence-313459790.html) 
to use NGINX as a reverse proxy, and to use the same HTTP port 80 for external connections. 

## 2: Summary report of similar hosts 
The primary identifying characteristics of this host are:

- The NGINX web server,
- Atlassian Confluence running behind the NGINX reverse proxy,
- and its location in China.

By querying Censys hosts for servers in China running NGINX with a service banner of Confluence returning OK HTTP status codes, we can enumerate hosts and services and further break them down by protocol.
The returned query makes it possible to then parse for the Confluence version number located within the meta tags of the HTML response by regular expression. This process can be observed in the `report.py` file;
I apologize for the spaghetti therein, I usually prefer to do parsing work in other languages!

## 3: Count the number of vulnerable hosts
Confluence, and most Atlassion software, is an attractive starting point for threat actors seeking to gain access to corporate networks. [CVE 2022-26134](https://nvd.nist.gov/vuln/detail/CVE-2022-26134) was disclosed June 30, 2022. It is a critical
severity remote code execution (RCE) vulnerability affecting all versions of Confluence from 1.3.0 to 7.4.17, and the following minor releases of version 7 (inclusive lower, exclusive upper):

- 7.13.0 to 7.13.7
- 7.14.0 to 7.14.3
- 7.15.0 to 7.15.2
- 7.16.0 to 7.16.4
- 7.17.0 to 7.17.4
- 7.18.0 to 7.18.1

Versions 8 and greater are not known to be vulnerable to this specific exploit at this time.

A brief parse job of the version numbers obtained from the report generated in section 2 allows us to compare each version number to those named in the CVE and provide us with a final count of the number of hosts vulnerable in this scan,
which by my count is 52. This comparison could also be done during the scanning phase on a per-host basis which would provide for some additional granularity, and would be of benefit to an organization
conducting reconnaissance or audits on its own networks. This count was made by the vulncount.go script.
