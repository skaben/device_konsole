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
            try:
                data = self.parse_item_data(item)
            except Exception:
                self.logger.exception('when parsing menu:')
                continue
            else:
                data.update({
                    'menu': menu_name,
                    'timer': item_timer
                })
                result.append(data)
        if result:
            workmode.update(menu_set=result)
        return workmode

    def parse_item_data(self, item):
        (item_type, item_hash) = list(item.items())[0]
        if item_type == 'game':
            data = self.parse_game_item(item)
        elif item_type == 'text':
            data = self.parse_text_item(item)
        else:
            data = self.parse_file_item(item_hash)

        return {
            'type': item_type,
            'data': data,
            'name': f'{item_type} document'
        }

    def parse_game_item(self, item):
        return item.get('game')

    def parse_text_item(self, item):
        return item.get('text')

    def parse_file_item(self, item_hash):
        item_path = self.data['assets'].get(item_hash).get('local_path').split('/')[-1]
        self.logger.error(f'{item_path}')
        if not item_path:
            raise Exception(f'item not presented {item_path}')
        return item_path

    def get_mode_content(self, unique: str, mode_url: str) -> dict:
        response = self.get_json(mode_url)
        content = self.parse_menu(response)
        self.workmodes.update({unique: content})
        return content

    def get_modes(self, data: dict, mode: str) -> dict:
        if not data['mode_list'].get(mode):
            return {}

        for mode_url in data['mode_list'].pop(mode):
            states = []
            unique = mode_url.split('/')[-1]
            # get existing content or download JSON from remote URL
            content = self.workmodes.get(unique, self.get_mode_content(unique, mode_url))

            if content.get('state'):
                states = [f'{_id}' for _id in content.pop('state')]

            for state_id in states:
                payload = {state_id: {mode: unique}}
                self._update_nested(self.mode_switch, payload)
        return self.workmodes

    def get_files(self, data: dict) -> list:
        if not data.get('file_list'):
            return {}
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
                device = self.system.get('device')
                device.switch_page('main')
            except Exception:
                raise
            super().save(data)
        except Exception:
            raise
