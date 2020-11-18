import os

from skabenclient.config import SystemConfig
from skabenclient.main import start_app

from device import KonsoleDevice
from config import KonsoleConfig

root = os.path.abspath(os.path.dirname(__file__))

sys_config_path = os.path.join(root, 'conf', 'system.yml')
dev_config_path = os.path.join(root, 'conf', 'device.yml')

log_path = os.path.join(root, 'local.log')


if __name__ == "__main__":
    #
    # DO NOT FORGET TO RUN ./pre-run.sh install BEFORE FIRST START
    #

    # setting core config
    app_config = SystemConfig(sys_config_path, root=root)
    app_config.logger(file_path=log_path)
    # setting initial device config
    dev_config = KonsoleConfig(dev_config_path, app_config)

    device = KonsoleDevice(app_config, dev_config)
    start_app(app_config=app_config,
              device=device)
