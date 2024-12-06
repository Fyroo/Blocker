from scapy.all import *

# Fonction qui sera appelée pour chaque paquet capturé
def procPacket(p):
    # Vérifier si la couche Ethernet, IP et UDP sont présentes
    if p.haslayer(Ether) and p.haslayer(IP) and p.haslayer(UDP):
        eth_layer = p.getlayer(Ether)
        src_mac, dst_mac = (eth_layer.src, eth_layer.dst)
        
        ip_layer = p.getlayer(IP)
        src_ip, dst_ip = (ip_layer.src, ip_layer.dst)
        
        udp_layer = p.getlayer(UDP)
        src_port, dst_port = (udp_layer.sport, udp_layer.dport)
        
        # Affichage des informations
        print(f"Ethernet Layer: Src MAC: {src_mac}, Dst MAC: {dst_mac}")
        print(f"IP Layer: Src IP: {src_ip}, Dst IP: {dst_ip}")
        print(f"UDP Layer: Src Port: {src_port}, Dst Port: {dst_port}")
        
        # Réaction spécifique si le paquet concerne le port 53 (DNS)
        if src_port == 53 or dst_port == 53:
            print("DNS packet detected (port 53)!")

# Capturer des paquets UDP sur le port 53
p = sniff( filter="udp port 53", prn=procPacket)

# Afficher les informations du premier paquet capturé
if p:  # Si un paquet a été capturé
    p.show()  # Afficher les détails du premier paquet capturé