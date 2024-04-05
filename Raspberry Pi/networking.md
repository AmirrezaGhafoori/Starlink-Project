### Network architecture 

There are two interfaces of the Raspberry Pi that are being used: 
1- wlan0: which is connected to a WiFi router and it's providing internet connection for the RPi. 
2- eth0: which is connected to an ethernet switch which is providing the LAN communication between all the RPis. 

All Raspberry Pis are connected to an ethernet switch which is not connected to any router. A challenge here for the communication between the raspberry pis is that their default gateway is being configured through the wlan0 interface which is connected to WiFi network and accordingly to the internet. On the other hand, the eth0 interface is not getting any advertisement from a DHCP server since it's only connected to a switch. 

# What happens here? 

When we try to "ping" a RPi, the ICMP echo request enters through the "eth0" interface, but it goes out through the "wlan0" interface since the default gateway is configures througth the "wlan0." This is why the RPi can ping the laptop conencted to the same ethernet swtich, but the laptop can't ping the RPi (the requests enter the RPi, but goes out the wrong way to the WiFi router)

# Why the laptop works properly? 

The laptop "ip route" table includes both the wired and wireless interfaces with different metric scores. So, when it receives something on the wired interface, it will send it throught the wired back first, then the wireless interface. 

