import requests
from skabenclient.config import DeviceConfigExtended

ESSENTIAL = {
    "assets": {}
}


class KonsoleConfig(DeviceConfigExtended):

    workmodes = {}
    mode_switch = {}

    def get_files(self, data: dict) -> list:
        if not data.get('file_list'):
            return []
        files = [item for item in self.parse_files(data.pop('file_list')).values()]
        return self.get_files_async(files)

    def get_modes(self, data: dict, mode: str) -> dict:
        if not data['mode_list'].get(mode):
            return {}

        for mode_url in data['mode_list'].pop(mode):
            states = []
            content = self.get_json(mode_url)
            unique = mode_url.split('/')[-1]
            self.workmodes.update({unique: content})

            if content.get('state'):
                states = [f'{_id}' for _id in content.pop('state')]

            for state_id in states:
                payload = {state_id: {mode: unique}}
                self._update_nested(self.mode_switch, payload)
        return self.workmodes

    def save(self, data: dict = None):
        if not data:
            return super().save()

        try:
            if data.get('mode_list'):
                for mode_type in ['normal', 'extended']:
                    self.get_modes(data, mode_type)

            data.update({
                "assets": self.get_files(data),
                "mode_list": self.workmodes,
                "mode_switch": self.mode_switch
            })

            super().save(data)
        except Exception:
            raise
