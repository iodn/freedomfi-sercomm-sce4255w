# calc_f2 (Small Cell FreedomFi Indoor CBRS Radio – Sercomm SCE4255W Englewood)

Generates the root SSH password and the GUI admin password for a FreedomFi Indoor CBRS Radio (Sercomm SCE4255W Englewood) from the device's MAC address.

## What it does
- Telnet key: generate the root SSH password
- Debug key: generate the GUI admin password

## Requirements
- Python 3
- Tested on small cell FreedomFi Indoor CBRS Radio (Sercomm SCE4255W Englewood) - Software version `DG3934v3@2308041842` 

## Usage
```bash
python3 calc_f2.py --mac 3C:62:F0:AA:AA:AA -k Telnet
python3 calc_f2.py --mac 3C:62:F0:AA:AA:AA -k Debug
```
Example output (Telnet → root SSH password):
```bash
python3 calc_f2.py --mac 3C:62:F0:AA:AA:AA -k Telnet
pag2bw4onpflqg3q
```
Example output (Debug → GUI admin password):
```bash
python3 calc_f2.py --mac 3C:62:F0:AA:AA:AA -k Debug
72oj8fr92895e2db
```
## Step-by-step guide to enable Sercomm GUI

1) Connect the small cell FreedomFi's LAN port to your PC. It should obtain an IP address via DHCP (for example, 11.11.11.100).

2) SSH to the device using the account `sc_femto/tsFid2wz` and use the command `rma get mac` to read the MAC address.
```bash
ssh sc_femto@11.11.11.188
sc_femto@11.11.11.188's password: 


BusyBox v1.24.2 (2023-08-04 18:00:02 CST) built-in shell (ash)
Enter 'help' for a list of built-in commands.

$ rma get mac
[mac] 3C:62:F0:AA:AA:AA
```
3) With the MAC address in hand, generate the root SSH password (Telnet key) using the python script `calc_f2.py`:
```bash
python3 calc_f2.py --mac 3C:62:F0:AA:AA:AA -k Telnet
pag2bw4onpflqg3q
```
4) SSH as root using the generated password, then enable the GUI using `femto_cli`:

```bash
ssh root@11.11.11.188    
root@11.11.11.188's password: 


BusyBox v1.24.2 (2023-08-04 18:00:02 CST) built-in shell (ash)
Enter 'help' for a list of built-in commands.

RF_CARD_ID=0x46
# femto_cli sset Device.X_SCM_DeviceFeature.X_SCM_WebServerEnable="1"
OK
# femto_cli fsave
OK
# reboot
```

5) After the device reboots, the Sercomm GUI should be available at https://11.11.11.188.

    screenshot GUI

6) Now generate the GUI admin password (Debug key) with the same MAC:

```bash
python3 calc_f2.py --mac 3C:62:F0:AA:AA:AA -k Debug 
72oj8fr92895e2db
```

7) Log into the GUI using the debug username (this is the admin account) and the Debug password:

    screenshot GUI

And you now have full control over your femtocell.
