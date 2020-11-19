import os
import asyncio
import concurrent.futures

from skabenclient.config import DeviceConfigExtended
from skabenclient.loaders import HTTPLoader

# это словарь, в котором содержится минимальный конфиг, с которым может стартовать девайс
# сомнительное решение, надо бы это переписать потом.

ESSENTIAL = {
    "assets": {}
}


class KonsoleConfig(DeviceConfigExtended):

    asset_dirs = ['image',
                  'audio',
                  'video',
                  'text'
                  ]

    def parse_modes(self, mode_list: list) -> list:
        if not mode_list:
            return []
        return [self.parse_json(mode) for mode in mode_list]

    def save(self, data=None):
        if not data:
            return super().save()

        download_files = self.parse_files(data.pop("file_list"))

        data.update({
            "files": self.get_files_async(download_files),
            "normal": self.parse_modes(data.pop["modes_normal"]),
            "extended": self.parse_modes(data.pop["modes_extended"])
        })

        return super().save(data)
