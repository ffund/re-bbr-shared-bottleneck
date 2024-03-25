::: {.cell .markdown}
## Reproduce results from "Modeling BBR’s Interactions with Loss-Based Congestion Control"

This notebook will reproduce selected findings from 

> Ranysha Ware, Matthew K. Mukerjee, Srinivasan Seshan, and Justine Sherry. 2019. Modeling BBR's Interactions with Loss-Based Congestion Control. In Proceedings of the Internet Measurement Conference (IMC '19). Association for Computing Machinery, New York, NY, USA, 137–143. https://doi.org/10.1145/3355369.3355604


specifically, 

* Figure 1b and 1c (initial measurements of BBR’s empirical behaviors)
* Figure 2: BBR vs Cubic in a 40ms × 10Mbps network (convergence time and goodput for 1 BBR and 1 Cubic flow over varying queue sizes)
* Figure 3: BBR and Cubic or Reno’s queue when competing for 4 minutes over a network with a 64 BDP (1024 packet) queue

:::

