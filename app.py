import os

from skabenclient.config import SystemConfig
from skabenclient.main import start_app

from device import KonsoleDevice
from config import KonsoleConfig

root = os.path.abspath(os.path.dirname(__file__))

sys_config_path = os.path.join(root, 'conf', 'system.yml')
dev_config_path = os.path.join(root, 'conf', 'device.yml')


if __name__ == "__main__":
    # setting core config
    app_config = SystemConfig(sys_config_path, root=root)
    # setting initial device config
    dev_config = KonsoleConfig(dev_config_path, app_config)
    dev_config.make_asset_paths()
    device = KonsoleDevice(app_config, dev_config)
    start_app(app_config=app_config,
              device=device)
