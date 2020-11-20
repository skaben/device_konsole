from skabenclient.config import DeviceConfigExtended

# это словарь, в котором содержится минимальный конфиг, с которым может стартовать девайс
# сомнительное решение, надо бы это переписать потом.

ESSENTIAL = {
    "assets": {}
}


class KonsoleConfig(DeviceConfigExtended):

    def parse_modes(self, mode_list: list) -> list:
        if not mode_list:
            return []
        return [self.parse_json(mode) for mode in mode_list]

    def save(self, data=None):
        if not data:
            return super().save()

        download_files = [item for item in self.parse_files(data.pop("file_list")).values()]

        data.update({
            "assets": self.get_files_async(download_files),
            "normal": self.parse_modes(data.pop("modes_normal")),
            "extended": self.parse_modes(data.pop("modes_extended"))
        })

        return super().save(data)
