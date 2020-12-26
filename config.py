import requests
from skabenclient.config import DeviceConfigExtended

ESSENTIAL = {
    "state_current": '',
    "assets": {}
}


class KonsoleConfig(DeviceConfigExtended):

    workmodes = {}
    mode_switch = {}

    def parse_menu(self, workmode):
        result = []
        for item in workmode.get('menu_set', []):
            menu_name = item.pop('name')
            item_timer = item.pop('timer')
            (item_type, item_hash) = list(item.items())[0]
            try:
                item_path = self.data['assets'].get(item_hash).get('local_path').split('/')[-1]
                if not item_path:
                    raise Exception('item not presented')
            except Exception as e:
                print(e)
                continue
            else:
                result.append({
                    'type': item_type,
                    'data': item_path,
                    'name': f'{item_type} document',
                    'menu': menu_name,
                    'timer': item_timer
                })
        workmode.update(menu_set=result)
        return workmode

    def get_modes(self, data: dict, mode: str) -> dict:
        if not data['mode_list'].get(mode):
            return {}

        for mode_url in data['mode_list'].pop(mode):
            states = []
            response = self.get_json(mode_url)
            unique = mode_url.split('/')[-1]
            content = self.parse_menu(response)
            self.workmodes.update({unique: content})

            if content.get('state'):
                states = [f'{_id}' for _id in content.pop('state')]

            for state_id in states:
                payload = {state_id: {mode: unique}}
                self._update_nested(self.mode_switch, payload)
        return self.workmodes

    def get_files(self, data: dict) -> list:
        if not data.get('file_list'):
            return []
        files = self.parse_files(data.pop('file_list')).values()
        return self.get_files_async(files)

    def save(self, data: dict = None):
        """extended save method

           parse terminal work modes (menu sets) and attached files
        """
        if not data:
            return super().save()

        try:
            if data.get('mode_list'):
                for mode_type in ['normal', 'extended']:
                    self.get_modes(data, mode_type)
            self.workmodes = self.parse_menu(self.workmodes)

            data.update({
                "assets": self.get_files(data),
                "mode_list": self.workmodes,
                "mode_switch": self.mode_switch
            })

            try:
                # oh, well, that's a crutch
                # should be fixed when full pub/sub pattern for client event queue will be implemented
                # todo: waiting for @hallucinite for client architecture update. go, Michael!
                device = self.system.get('device')
                # todo: WEBSOCKET is losing connection, update is so slow
                device.switch_page('main')
            except Exception:
                raise
            super().save(data)
        except Exception:
            raise
