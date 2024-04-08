import numpy as np
import matplotlib.pyplot as plt

# In this model, BBR is BBRv1. 

# p = Cubic/Reno's share of the link capacity at convergence
# 1-p = BBR's share of the link capavity at convergence
# N = Number of BBR flows sharing bottleneck
# q = Bottleneck queue capacity (packets)
# c = Bottleneck link capacity (packets per second)
# l = RTT when there is no congestion (seconds) (base RTT)
# X = Queue capacity as multiple of BDP. (q = X*c*l, where BDP = c*l)
# d = Flow completion times after convergence (seconds)



# Assumptions:
    # Flows have infinite data to send.
    # Flows' sending rates are determined by their CCA, which is either BBR, Cubic or Reno.
    # All flows experience the same congestion-free RTT and the available link capacity is fixed.
    # All packets are a fixed size.
    # The network is congested and the queue is typically full; a flow’s share of throughput hence equals its share of the queue.
    # All loss-based CCA and BBR flows are synchronized. All flows begin at the same time.
    

    
def ware_BBR_Model(base_rtt, link_capacity, X, N, d):
    
    
    packet_size_in_bytes=1500
    packet_size = packet_size_in_bytes * 8  # in bits
    l = base_rtt * 0.001  # in seconds
    c = link_capacity * 1000000 / packet_size  # bottleneck link capacity (packets per second)
        
    # Simple Model: BBR's In-flight Cap

    # Assumptions:
        # There is only 1 BBR flow competing with any number loss-based CCAs.
        # The queue capacity is much greater than the BDP (q ≫ c*l).        
    # Model: 
        
        # inflight_cap= 2 * RTT_est * Btlbw_est (1)
        # With a queue capacity of q we can assume that, at any given point of competition p from loss-based flows,
            # BBR will consume the remaining bandwidth:  Btlbw_est = (1-p) * c (2)
        # About every 10 seconds, BBR enters ProbeRTT to measure the baseline RTT, draining any packets BBR has in the queue.
        # When there is no competing traffic, 1 BBR flow can successfully measure the baseline RTT l during ProbeRTT.
        # When there is competing traffic from loss-based CCAs, there will be (p * q) data in the queue.
        # Assuming a negligible baseline RTT (q ≫ c*l), as bufferbloat increases, queuing delay becomes the dominant factor in latency, we have:
            # RTT_est = (p * q) / c (3)
            
        # Plugging (2) and (3) into (1) and reducing gives:
            # inflight_cap = 2 * p * (1-p) * q
            
        # We know from the previous subsection that BBR will increase its rate until it is limited by the in-flight cap. 
        # To compute this, we set inflight_cap equal to the amount of data BBR has in-flight and solve for p.
            # 2 * p * (1-p) * q =  (1-p) * q
            # p = 1/2
            
        # We can now see that while 1 BBR flow increases its sending rate during ProbeBW, once it intersects the in-flight cap it will not be able to consume more than 50% of the available capacity.
        
        
    # Result for this Model:
        
        # In convergence, when single BBR flows competes with loss based CCA flows on the shared bottleneck, BBR occupies half of the available capacity with 2BDP in-flight cap. (with the assumptions defined above)
            
    # bottleneck queue capacity (packets)
    q = X*c*l

    # BBR queue occupancy in convergence
    bbr_occupancy_simple_model = q/2  # equation (5) in the original paper
    
    
    # Extended Model: BBR's In-flight Cap


    # The simple model assumes a buffer-bloated network and only one BBR flow. 
    # In this section, we show how BBR’s in-flight cap changes given the size of the queue (bloated or not) and with an increasing number of BBR flows.


    # Multiple BBR Flows Alone (no other CCA flows)

        # After convergence, each BBR flow has a slightly overestimated Btlbw_est near their fair share:
            # Btlbw_est = (1/N) * c + ε  
            # The additional ε is due to the aggression of ProbeBW. 
            # Here, BBR flows compete against each other.
            # BBR uses a max() operation to compute Btlbw_est over multiple samples of sending rates resulting in, usually, a slight overestimate of its fair share. 
            # The additional ε is ignored in the model. However,  its existence forces the aggregate of BBR flows to send at a rate slightly higher than c, filling queues until each flow reaches its bandwidth cap and becomes window-limited and subsequently ACK-clocked.
        
        # However, the cap may also be elevated due to the presence of multiple competing flows.
        
            # During ProbeRTT, each flow will limit inflight to 4 packets, so that they can drain all of their packets from the queue and measure the baseline RTT. 
            # For N BBR flows, this means in aggregate they will have 4N packets inflight.
            # However, if 4N packets is greater than the BDP, the queue will not drain during ProbeRTT so RTTest includes some queueing delay:
                # RTT_est = max(l, (4*N - c*l)/c + l)
                
                # Thus, the in-flight cap when N BBR flows compete is dependent on the BDP. 
                # Further, if the queue capacity is smaller than 4N − cl when 4N > cl, then the BBR flows will consume the entire queue and hence 100% link capacity.
    
    
    # RTT_est calculation 
    RTT_est = np.maximum(l, (4 * N - c * l) / c + l)  # equation (6) in the original paper
    RTT_est_ms = RTT_est * 1000
    
    # inflight cap calculation

    inflight_cap = (2 * (c / N)* RTT_est) * packet_size /(8*1000)  # 2 * (Estimated BDP) # in Kbytes
    
    
    
    
    # Multiple BBR Flows vs Loss-Based Flows

    # In previous section, it is observed that when BBR flows were only competing with each other, if the BDP is not large enough to accommodate 4*N packets during ProbeRTT, BBR’s RTT estimate will be too large.
    # If we assume 4N additional packets are in the queue during ProbeRTT, then,
        # RTT_est = (p*q + 4*N)/c + l    (7)
        # Here, l is also included. It is no longer negligible compared to queueing delay. 
        # Plugging (7) and (2) into (1), in aggregate all N BBR flows will have:
            # inflight_cap= 2 * Btlbw_est * RTT_est  = 2 *  (1-p) * c * ((p*q + 4*N)/c + l) (8)
            
        # To compute the BBR flows’ aggregate fraction of the link, we set inflightcap equal to the amount of data BBR flows have in-flight and solve for p:
            #  2 *  (1-p) * c * ((p*q + 4*N)/c + l) = (1-p) * q + (1-p) * c * l
            #  p = (1/2) - (1/(2*X)) - (4*N/q)  (9)
            
        # If p were a negative number, this would mean BBR’s inflight cap exceeded the total capacity (BDP + the queue size) and hence BBR’s share of the link would be 100%.
        
    # Extended Model: ProbeRTT Duration

    # During ProbeRTT, BBR stops sending data while it waits for its in- flight data to fall to 4 packets.
    # If the queue is large and also full when BBR goes into ProbeRTT, this results in long intervals where BBR is not sending any data.
    # This results in BBR on average consuming a lower fraction of link capacity than if it were sending constantly at a rate proportional to its inflight cap.

    # Model
        # If the total duration of time the flows are competing (after convergence) is d, the fraction of the link BBR flows will use when competing with loss-based CCAs is:
            # BBR_frac = (1-p) * (d - Probe_time)/d   (10)
            # p could be computed using  equation (9)
            # During Probetime throughput is nearly zero.
          
        # We compute Probetime by computing the length of time spent in ProbeRTT state, and multiply by how many times BBR will go into ProbeRTT state.
        # Assuming the queue is full before BBR enters ProbeRTT state, BBR will have to wait for the queue to drain before its data in-flight falls to 4 packets.
        # Once it reaches this in-flight cap, BBR also waits an additional 200ms and a packet-timed round trip before exiting ProbeRTT. 
        # Assuming synchronized flows and the queue is typically full, BBR flows should rarely measure a smaller RTT outside of ProbeRTT state so it should enter ProbeRTT about every 10 seconds.
        # Altogether, this means probe time increases linearly with queue size:
            # Probe_time = (q/c + 0.2 + l) * (d/10) (11)
    
    
    # Probe Time calculation 
    probe_time=(q/c + 0.2 + l)*(d/10)  # equation (11) in the original paper
    
    
    
    # Validating the Extended Model
    
    # Cubic/Reno's share of the link capacity at convergence
    p = np.maximum(0, ((1/2) - (1/(2*X)) - (4*N/q)))
    
    #BBR fraction calculation
    BBR_frac=(1-p)*(d-probe_time)/d
    
    result_dict = {
    "simple_model_bbr_occupancy": bbr_occupancy_simple_model,
    "RTT_est_ms": RTT_est_ms,
    "inflight_cap": inflight_cap,
    "probe_time": probe_time,
    "Non_BBR_share": p,
    "BBR_fraction": BBR_frac
}    
    
    return result_dict
    
    
    
    
    