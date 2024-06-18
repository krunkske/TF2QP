import json

servers = []
unsorted_list_ip = []
unsorted_list_name = []
unsorted_list_region = []

with open('configs/casual_unsorted_ip.txt', 'r') as f:
    unsorted_list_ip = f.read().split('\n')

with open('configs/casual_unsorted_name.txt', 'r') as f:
    unsorted_list_name = f.read().split('\n')

with open('configs/casual_unsorted_regions.txt', 'r') as f:
    unsorted_list_region = f.read().split('\n')


for i in range(len(unsorted_list_ip)):
    ip_and_port = unsorted_list_ip[i].split(':')
    ip = ip_and_port[0]
    port = ip_and_port[1]
    name = unsorted_list_name[i]
    region = unsorted_list_region[i]
    
    servers.append({"name": name, "region": region, "ip": ip, "port": int(port)})
    
with open('configs/casual_servers.json', 'w') as f:
    f.write(json.dumps(servers, indent=4))
    