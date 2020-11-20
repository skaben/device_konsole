from skabenclient.config import DeviceConfigExtended

# это словарь, в котором содержится минимальный конфиг, с которым может стартовать девайс
# сомнительное решение, надо бы это переписать потом.

ESSENTIAL = {
    "assets": {}
}


class KonsoleConfig(DeviceConfigExtended):

    WORKMODE_API_URL = '/api/workmode/'

    def make_api_url(self, mode_id):
        # todo: bullshit URL assembling. must be refactored
        return f'http://{self.system.get("broker_ip")}{self.WORKMODE_API_URL}{mode_id}'

    def parse_modes(self, mode_list: list) -> list:
        if not mode_list:
            return []
        return [self.get_json(self.make_api_url(mode)) for mode in mode_list]

    def save(self, data=None):
        if not data:
            return super().save()

        try:
            file_list = data.pop("file_list")
            download_files = [item for item in self.parse_files(file_list).values()]

            data.update({
                "assets": self.get_files_sync(download_files),
                #"normal": self.parse_modes(data.pop("modes_normal")),
                #"extended": self.parse_modes(data.pop("modes_extended"))
            })

            super().save(data)
        except Exception as e:
            self.logger.exception('!!!')
