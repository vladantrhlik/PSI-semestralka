
## R1 (Cisco)
### Interface
```
interface GigabitEthernet0/0
 ip address 10.0.1.254 255.255.255.0
 no shutdown
 
interface GigabitEthernet1/0
 ip address 10.0.2.254 255.255.255.0
 no shutdown

interface GigabitEthernet2/0
 ip address 192.168.1.1 255.255.255.252
 no shutdown
```
### DHCP pool
```
ip dhcp exclude-addresses 10.0.1.254
ip dhcp exclude-addresses 10.0.2.254

ip dhcp pool 1
   network 10.0.1.0 255.255.255.0
   dns-server 8.8.8.8 8.8.4.4
   default-router 10.0.1.254

ip dhcp pool 2
   network 10.0.2.0 255.255.255.0
   dns-server 8.8.8.8 8.8.4.4
   default-router 10.0.2.254
```
### OSPF
```
router ospf 1
   network 10.0.1.0 0.0.0.255 area 0
   network 10.0.2.0 0.0.0.255 area 0
   network 192.168.1.0 0.0.0.3 area 0
```

## FRR
### Interface
```
interface eth0
 ip address 192.168.2.2/30
 no shutdown

interface eth1
 ip address 192.168.1.2/30
 no shutdown
```
### OSPF
Zapnutí systémové proměnné pro spuštění ospf daemona:
```
ENABLE_OSPF=yes
```
Nastavení OSPF pro oba interfacy:
```
router ospf
 network 192.168.1.0/30 area 0
 network 192.168.2.0/30 area 0
```

## R2
### Interface
```
interface GigabitEthernet0/0
 ip address dhcp
 ip nat ouside
 no shutdown

interface GigabitEthernet1/0
 ip address 192.168.2.1 255.255.255.252
 ip nat inside
 no shutdown
```
### OSPF
```
router ospf 1
   network 192.168.2.0 0.0.0.3 area 0
   default-information originate
```
### NAT
```
access-list 100 permit ip 192.168.1.0 0.0.0.3 any
access-list 100 permit ip 192.168.2.0 0.0.0.3 any
access-list 100 permit ip 10.0.0.0 0.0.255.255 any

ip nat inside source list 100 interface GigabitEthernet 0/0 overload
```

## psi-basenode-node-*
Pro každý stroj je potřeba zapnout DHCP - Edit Config, odkomentování
```
auto eth0
iface eth0 inet dhcp
```
