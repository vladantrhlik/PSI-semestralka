# PSI - 2. úloha

Topologie sítě byla vytvořena dle zadání - obsahuje 4 koncové stroje (`psi-base-node`), které jsou rozděleny na 2 DHCP pooly. Dále jsou zde 3 routery (2 Cisco, 1 FRR), které směrují pakety pomocí OSPF.

![](topologie.png)

## R1 (Cisco)
Router R1 slouží jako DHCP server pro dva DHCP pooly. Pakety směruje dále pomocí OSPF.
#### Konfigurace
##### Interface
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
##### DHCP pool
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
##### OSPF
```
router ospf 1
   network 10.0.1.0 0.0.0.255 area 0
   network 10.0.2.0 0.0.0.255 area 0
   network 192.168.1.0 0.0.0.3 area 0
```

## FRR
FRR router složí pouze jako prostředník mezi R1 (DHCP server) a R2 (NAT server) a směruje pakety pomocí OSPF.
### Konfigurace
#### Interface
```
interface eth0
   ip address 192.168.2.2/30
   no shutdown

interface eth1
   ip address 192.168.1.2/30
   no shutdown
```
#### OSPF
Zapnutí systémové proměnné pro spuštění OSPF daemona:
```
ENABLE_OSPF=yes
```
Nastavení OSPF pro oba interfacy:
```
router ospf
   network 192.168.1.0/30 area 0
   network 192.168.2.0/30 area 0
```

## R2 (Cisco)
Router R2 slouží jako NAT server připojený ISP, od kterého získává defaultní směr pomocí dhcp.
#### Interface
```
interface GigabitEthernet0/0
   ip address dhcp
   no shutdown

interface GigabitEthernet1/0
   ip address 192.168.2.1 255.255.255.252
   no shutdown
```
#### OSPF
```
router ospf 1
   network 192.168.2.0 0.0.0.3 area 0
   default-information originate
```
#### NAT
```
interface GigabitEthernet0/0
   ip nat ouside

interface GigabitEthernet1/0
   ip nat inside

access-list 100 permit ip 192.168.1.0 0.0.0.3 any
access-list 100 permit ip 192.168.2.0 0.0.0.3 any
access-list 100 permit ip 10.0.0.0 0.0.255.255 any

ip nat inside source list 100 interface GigabitEthernet 0/0 overload
```

## psi-basenode-node-*
Pro každý stroj je potřeba zapnout DHCP - v Edit Config, odkomentování
```
auto eth0
iface eth0 inet dhcp
```
