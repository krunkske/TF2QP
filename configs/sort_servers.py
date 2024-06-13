import json

servers = []
unsorted_list_ip = []
unsorted_list_name = []

with open('casual_unsorted_ip.txt', 'r') as f:
    unsorted_list_ip = f.read().split('\n')

with open('casual_unsorted_name.txt', 'r') as f:
    unsorted_list_name = f.read().split('\n')

for i in range(len(unsorted_list_ip)):
    ip_and_port = unsorted_list_ip[i].split(':')
    ip = ip_and_port[0]
    port = ip_and_port[1]
    name = unsorted_list_name[i]
    
    servers.append({"name": name, "ip": ip, "port": port})
    
with open('casual_servers.json', 'a') as f:
    f.write(json.dumps(servers, indent=4))
    