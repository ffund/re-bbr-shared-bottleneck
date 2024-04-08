::: {.cell .markdown}

### Reproduce Figure 1c

:::

::: {.cell .code}
```python
router_node = slice.get_node("router")
sender_node = slice.get_node("sender")
receiver_node = slice.get_node("receiver")
```
:::


::: {.cell .code}
```python
# set router buffer limit to 32 BDP
router_node.execute("sudo tc qdisc replace dev " + router_egress_name + " parent 1:3 bfifo limit " + str(bdp_kbyte*32) + "kb")

# make sure BBR is available
sender_node.execute("sudo modprobe tcp_bbr")
receiver_node.execute("sudo modprobe tcp_bbr")

# clean up
receiver_node.execute("sudo killall iperf3")
receiver_node.execute("rm fig1c_bbr.txt")
receiver_node.execute("rm fig1c_cubic.txt")

# start an iperf3 receiver for the BBR flow
receiver_node.execute_thread("iperf3 -s -1 -i 1 -fm --logfile fig1c_bbr.txt")
# start an iperf3 receiver for the Cubic flows
receiver_node.execute_thread("iperf3 -s -1 -i 1 -fm --logfile fig1c_cubic.txt -p 5301")

time.sleep(5) 

# start an iperf3 sender for the BBR flow
sender_node.execute_thread("iperf3 -c receiver -fm -t 300 -C bbr ")
# start an iperf3 receiver for the Cubic flows
sender_node.execute_thread("iperf3 -c receiver -fm -t 300 -C cubic -P 16 -p 5301")

time.sleep(305)
```
:::

::: {.cell .code}
```python
tput_bbr = receiver_node.execute("head --lines=-5 fig1c_bbr.txt | grep 'Mbits/sec' | awk -F '-' '{print $2}' | awk '{print $1\",\"$5}'", quiet=True)
df_bbr = pd.read_csv(StringIO(tput_bbr[0]), names = ['time','goodput'])

tput_cubic = receiver_node.execute("head --lines=-37 fig1c_cubic.txt | grep 'SUM' | awk -F '-' '{print $2}' | awk '{print $1\",\"$5}'", quiet=True)
df_cubic = pd.read_csv(StringIO(tput_cubic[0]), names = ['time','goodput'])

_ = plt.figure(figsize=(6,3))
_ = plt.plot(df_bbr.time, df_bbr.goodput, label="1 BBR flow")
_ = plt.plot(df_cubic.time, df_cubic.goodput, label="Sum of 16 CUBIC flows")
_ = plt.legend(loc="upper center", ncol=2)
_ = plt.ylabel("Goodput (Mbps)")
_ = plt.xlabel("Time (s)")
```
:::
