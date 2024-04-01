::: {.cell .markdown}

### Reproduce Figure 1b

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
import itertools
exp_factors = { 
    'bufcap': [0.25, 0.5] + [2**n for n in range(8)],
    'duration': [240],
    'loss_cc': ['cubic', 'reno']
    'trial': [1]
}
factor_names = [k for k in exp_factors]
factor_lists = list(itertools.product(*exp_factors.values()))
exp_lists = [dict(zip(factor_names, factor_l)) for factor_l in factor_lists]
```
:::


::: {.cell .code}
```python
import time # to allow resume
for exp in exp_lists:
    # set router buffer limit 
    router_node.execute("sudo tc qdisc replace dev " + router_egress_name + " parent 1:3 bfifo limit " + str(bdp_kbyte*exp['bufcap']) + "kb")

    # make sure BBR is available
    sender_node.execute("sudo modprobe tcp_bbr")

    # clean up
    receiver_node.execute("sudo killall iperf3")
    receiver_node.execute("rm fig1c_bbr.txt")
    receiver_node.execute("rm fig1c_cubic.txt")

    # start an iperf3 receiver for the BBR flow
    receiver_node.execute_thread("iperf3 -s -1 -i 1 --logfile fig1b_bbr_" + str(exp['bufcap']) + "_bbrV" + exp['loss_cc'] + ".txt")
    # start an iperf3 receiver for the Cubic flows
    receiver_node.execute_thread("iperf3 -s -1 -i 1 --logfile fig1b_" + exp['loss_cc'] + "_bbrV" + str(exp['bufcap']) + "_" + exp['loss_cc'] + ".txt -p 5301")

    time.sleep(5) 

    # start an iperf3 sender for the BBR flow
    sender_node.execute_thread("iperf3 -c receiver -fm -t " + exp['duration'] + " -C bbr ")
    # start an iperf3 receiver for the Cubic flows
    sender_node.execute_thread("iperf3 -c receiver -fm -t " + exp['duration'] + " -C " + exp['loss_cc'] + "-p 5301")

    time.sleep(305)

```
:::

