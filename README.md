# device konsole

экспериментальный web терминал

config syntax:

```
# mqtt topic name - /ask/<topic> for pub, /<topic> for sub
topic: 'terminal'
# external network interface
iface: <iface>
# MQTT broker IP
broker_ip: <IP>
# MQTT auth
username: <username>
password: <password>
# standalone=True start app without network support
standalone: bool
# API server IP
host: <IP:port>
# retries policy
http_retries: 1
# directory for storing in-game documents
asset_root: <dirname>
# supported document asset types
asset_types:
  - image
  - audio
  - video
  - text
# headless=True start app without web-interface
headless: bool
# screen resolution
resolution:
  - 1024
  - 768
# fullscreen=True start in fullscreen mode
fullscreen: bool
```
