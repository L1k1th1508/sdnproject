# Static Router Implementation using POX and Mininet

This project implements a **Software Defined Networking (SDN)** static router. It manages a linear topology of three switches and two hosts, using the POX controller to install bidirectional flow rules with specific timeout constraints.

## Project Overview
- **Controller:** POX (Python)
- **Network Emulator:** Mininet
- **Protocol:** OpenFlow 1.0
- **Topology:** Linear (h1 - s1 - s2 - s3 - h2)

##  Features
- **Manual Flow Entries:** Explicitly defines the path for packets between Host 1 and Host 2.
- **Bidirectional Connectivity:** Ensures traffic can flow both ways (h1 to h2 and h2 to h1).
- **Flow Expiration:** Implements `idle_timeout` and `hard_timeout` of 10 seconds to ensure flow tables stay clean after traffic stops.

##  File Structure
- `static_router.py`: The POX controller logic (place in `pox/ext/`).
- `topo.py`: Python script to generate the 3-switch linear topology.
- `Screenshots/`: Folder containing verification images of pings and flow dumps.

##  Execution Instructions

### 1. Start the POX Controller and run mininet in another terminal
Open a terminal and run:
cd pox/controller
sudo python3 remote_static.py
Open in another terminal
cd pox/controller/
sudo mn --custom topo.py --topo mystatictopo --controller remote

## check connectivity in mininet and strength of bandwith between hosts
hi ping h2
iperf h1 h2
# for flow table
leave the ping on
in another terminal
bash
sudo ovs-ofctl dump-flows s1
sudo ovs-ofctl dump-flows s2
sudo ovs-ofctl dump-flows s3
