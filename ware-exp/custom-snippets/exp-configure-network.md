::: {.cell .markdown}

### Configure the network capacity and delay

In this section, we configure the bottleneck link to have a 40Mbps capacity and 10ms delay.  We will initialize the queue size to 32 BDP (although we will change this later).

:::

::: {.cell .code}
```python
exp = {'rtt': 40, 'bandwidth': 10 }
bdp_kbyte = exp['rtt']*exp['bandwidth']/8

router_node = slice.get_node("router")
router_ingress_iface = router_node.get_interface(network_name = "net0")
router_ingress_name = router_ingress_iface.get_device_name()
router_egress_iface  = router_node.get_interface(network_name = "net1")
router_egress_name = router_egress_iface.get_device_name()

router_node.execute("sudo tc qdisc del dev " + router_ingress_name + " root")
router_node.execute("sudo tc qdisc del dev " + router_egress_name + " root")

# set up RTT
router_node.execute("sudo tc qdisc replace dev " + router_ingress_name + " root netem delay " + str(exp['rtt']) + "ms limit 10000")
# set up rate limit, buffer limit
router_node.execute("sudo tc qdisc replace dev " + router_egress_name + " root handle 1: htb default 3")
router_node.execute("sudo tc class add dev " + router_egress_name + " parent 1: classid 1:3 htb rate " + str(exp['bandwidth']) + "Mbit")
router_node.execute("sudo tc qdisc add dev " + router_egress_name + " parent 1:3 bfifo limit " + str(bdp_kbyte*32) + "kb")

```
:::

::: {.cell .markdown}

Then, we validate the new network setting.

:::


::: {.cell .code}
```python
# check base delay
_ = slice.get_node("sender").execute("ping -c 5 receiver")
```
:::

::: {.cell .code}
```python
# check base capacity (by sending 10 parallel flows, look at their sum throughput)
import time
_ = slice.get_node("receiver").execute("iperf3 -s -1 -D")
time.sleep(5)
_ = slice.get_node("sender").execute("iperf3 -t 30 -i 10 -P 10 -c receiver")
```
:::



::: {.cell .code}
```python
# make sure each flow is a "fresh start"
slice.get_node("sender").execute("sudo sysctl -w net.ipv4.tcp_no_metrics_save=1")
slice.get_node("receiver").execute("sudo sysctl -w net.ipv4.tcp_no_metrics_save=1")
```
:::
