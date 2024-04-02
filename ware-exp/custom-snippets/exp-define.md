::: {.cell .markdown}
### Define configuration for this experiment 
:::

::: {.cell .code}
```python
slice_name="ware-" + fablib.get_bastion_username()

node_conf = [
 {'name': "sender",    'cores': 2, 'ram': 4, 'disk': 10, 'image': 'default_ubuntu_22', 'packages': ['iperf3']}, 
 {'name': "receiver",  'cores': 2, 'ram': 4, 'disk': 10, 'image': 'default_ubuntu_22', 'packages': ['iperf3']}, 
 {'name': "router",    'cores': 2, 'ram': 4, 'disk': 10, 'image': 'default_ubuntu_22', 'packages': []}
]
net_conf = [
 {"name": "net0", "subnet": "10.0.0.0/24", "nodes": [{"name": "sender",   "addr": "10.0.0.100"}, {"name": "router", "addr": "10.0.0.1"}]},
 {"name": "net1", "subnet": "10.0.1.0/24", "nodes": [{"name": "receiver", "addr": "10.0.1.100"}, {"name": "router", "addr": "10.0.1.1"}]},
]
route_conf = [
 {"addr": "10.0.1.0/24", "gw": "10.0.0.1", "nodes": ["sender"]}, 
 {"addr": "10.0.0.0/24", "gw": "10.0.1.1", "nodes": ["receiver"]}
]
exp_conf = {'cores': sum([ n['cores'] for n in node_conf]), 'nic': sum([len(n['nodes']) for n in net_conf]) }
```
:::
