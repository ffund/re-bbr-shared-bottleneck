::: {.cell .markdown}
### Validate base network

Before we run any experiment, we should check the "base" network - before adding any emulated delay or rate limiting - and make sure that it will not be a limiting factor in the experiment.

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
# also check Linux kernel version on sender
_ = slice.get_node("sender").execute("uname -a")
```
:::


