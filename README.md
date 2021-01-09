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
# standalone: true start app without network support
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
# headless: true start app without web-interface
headless: bool
# web-interface screen resolution
resolution:
  - 1024
  - 768
# fullscreen: true start web-interface in fullscreen mode
fullscreen: bool
```
