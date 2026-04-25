

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class StaticRouter(object):
    """
    Handles packet_in events and installs explicit flow rules 
    to establish a static path between h1 and h2.
    """
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        """
        Logic for match-action rule design based on Switch DPID.
        Includes idle_timeout to ensure flows expire when POX is inactive.
        """
        dpid = event.connection.dpid
        in_port = event.port
        
        # Initialize the OpenFlow Flow Modification message [cite: 10]
        msg = of.ofp_flow_mod()
        msg.priority = 100  # High priority for explicit flow rule [cite: 9]
        
        # --- TIMEOUT LOGIC ---
        # Rule vanishes if no traffic is detected for 10 seconds.
        # This ensures the ping stops 10s after POX is exited.
        msg.idle_timeout = 10 
        
        # Optional: Hard timeout forces rule removal even if traffic is active.
        # msg.hard_timeout = 30 
        # ---------------------

        # Path Construction Logic: h1 <-> s1 <-> s2 <-> s3 <-> h2 [cite: 3]
        if dpid == 1: # Switch 1 (h1 side)
            if in_port == 1: # From h1
                msg.match.in_port = 1
                msg.actions.append(of.ofp_action_output(port = 2)) # To s2
            elif in_port == 2: # From s2
                msg.match.in_port = 2
                msg.actions.append(of.ofp_action_output(port = 1)) # To h1

        elif dpid == 2: # Switch 2 (Middle)
            if in_port == 1: # From s1
                msg.match.in_port = 1
                msg.actions.append(of.ofp_action_output(port = 2)) # To s3
            elif in_port == 2: # From s3
                msg.match.in_port = 2
                msg.actions.append(of.ofp_action_output(port = 1)) # To s1

        elif dpid == 3: # Switch 3 (h2 side)
            if in_port == 1: # From s2
                msg.match.in_port = 1
                msg.actions.append(of.ofp_action_output(port = 2)) # To h2
            elif in_port == 2: # From h2
                msg.match.in_port = 2
                msg.actions.append(of.ofp_action_output(port = 1)) # To s2

        # Send the explicit flow rule to the switch [cite: 9, 10]
        self.connection.send(msg)
        log.info("Rule (with 10s timeout) installed on Switch %s for Port %s", dpid, in_port)

def launch():
    """
    Registers the ConnectionUp listener to initialize the StaticRouter.
    """
    def start_switch(event):
        log.info("Controller-switch interaction established with DPID %s", event.dpid)
        StaticRouter(event.connection)
    
    core.openflow.addListenerByName("ConnectionUp", start_switch)
