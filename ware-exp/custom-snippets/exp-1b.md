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
    'loss_cc': ['cubic', 'reno'],
    'trial': [1]
}
factor_names = [k for k in exp_factors]
factor_lists = list(itertools.product(*exp_factors.values()))
exp_lists = [dict(zip(factor_names, factor_l)) for factor_l in factor_lists]
```
:::


::: {.cell .code}
```python
import time

# make sure BBR is available
sender_node.execute("sudo modprobe tcp_bbr")
receiver_node.execute("sudo modprobe tcp_bbr")

for exp in exp_lists:
    # set router buffer limit 
    router_node.execute("sudo tc qdisc replace dev " + router_egress_name + " parent 1:3 bfifo limit " + str(bdp_kbyte*exp['bufcap']) + "kb")

    # clean up
    receiver_node.execute("sudo killall iperf3")
    sender_node.execute("sudo killall iperf3")

    # start an iperf3 receiver for the BBR flow
    receiver_node.execute_thread("iperf3 -s -1 -i 1 -fm --logfile fig1b_bbr_" + str(exp['bufcap']) + "_bbrV" + exp['loss_cc'] + ".txt")
    # start an iperf3 receiver for the Cubic flows
    receiver_node.execute_thread("iperf3 -s -1 -i 1 -fm --logfile fig1b_" + exp['loss_cc'] + "_" + str(exp['bufcap']) + "_bbrV" + exp['loss_cc'] + ".txt -p 5301")

    time.sleep(5) 

    # start an iperf3 sender for the BBR flow
    sender_node.execute_thread("iperf3 -c receiver -fm -t " + str(exp['duration']) + " -C bbr ")
    # start an iperf3 receiver for the Cubic flows
    sender_node.execute_thread("iperf3 -c receiver -fm -t " + str(exp['duration']) + " -C " + exp['loss_cc'] + "-p 5301")

    time.sleep(exp['duration'] + 5)

```
:::


::: {.cell .code}
```python
df = pd.DataFrame(columns=['bufcap', 'combo', 'cc', 'goodput'])

for exp in exp_lists:

    bbr_file = "fig1b_bbr_" + str(exp['bufcap']) + "_bbrV" + exp['loss_cc'] + ".txt"
    tput_bbr = receiver_node.execute("cat " + bbr_file + " | grep 'receiver' | awk -F '-' '{print $2}' | awk '{print $5}'", quiet=True)
    df_dict = {'bufcap': exp['bufcap'], 'combo': "BBR-" + exp['loss_cc'], 'cc': 'BBR', 'goodput': float(tput_bbr[0].strip())}
    df = pd.concat([df, pd.DataFrame(df_dict, index=[0])], ignore_index=True)


    loss_file = "fig1b_" + exp['loss_cc'] + "_" + str(exp['bufcap']) + "_bbrV" + exp['loss_cc'] + ".txt"
    tput_loss = receiver_node.execute("cat " + loss_file + " | grep 'receiver' | awk -F '-' '{print $2}' | awk '{print $5}'", quiet=True)
    df_dict = {'bufcap': exp['bufcap'], 'combo': "BBR-" + exp['loss_cc'], 'cc': exp['loss_cc'], 'goodput': float(tput_loss[0].strip())}
    df = pd.concat([df, pd.DataFrame(df_dict, index=[0])], ignore_index=True)

```
:::


::: {.cell .code}
```python
df['buf_str'] = df['bufcap'].astype(str)
g = sns.FacetGrid(df, row="combo", legend_out=True, aspect=2);
g = g.map(sns.lineplot, "buf_str", "goodput",  hue=df.cc);
g.set_axis_labels("Buffer size (BDP)", "Goodput (Mbps)");
plt.legend();
```
:::
