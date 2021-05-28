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
            data = self.parse_text_item(item_hash)
        else:
            data = self.parse_file_item(item_hash)

        return {
            'type': item_type,
            'data': data,
            'name': f'{item_type} document'
        }

    def get_local_path(self, item_hash):
        if not self.data.get('assets'):
            self.logger.error('no assets!')
            return

        item = self.data['assets'].get(item_hash, {})
        item_path = item.get('local_path', None)
        if not item_path:
            self.logger.error(f'no `local_path` found for {item}')
            return

        return item_path

    def parse_game_item(self, item):
        return item.get('game')

    def parse_text_item(self, item_hash: str):
        item_path = self.get_local_path(item_hash)
        try:
            if not item_path:
                raise ValueError
            with open(item_path, 'r', encoding='utf-8') as fh:
                content = fh.readlines()
                return '\n'.join([row.strip() for row in content])
        except Exception:
            return ''

    def parse_file_item(self, item_hash):
        _path = self.get_local_path(item_hash)
        if not _path:
            raise ValueError
        return _path.split('/')[-1]

    def get_files(self, data: dict) -> dict:
        if not data.get('file_list'):
            return {}

        files = self.parse_files(data.pop('file_list')).values()
        return self.get_files_async(files)

    def get_workmodes(self, urls: list) -> dict:
        for url in urls:
            mode_uid = url.split('/')[-1]
            response = self.get_json(url)
            parsed = self.parse_menu(response)
            self.workmodes.update({mode_uid: parsed})
        return self.workmodes

    def gen_mode_switch(self, mode_type: str) -> dict:
        for uid, content in self.workmodes.items():
            state = content.get('state')
            if not state:
                continue
            states = [f'{_id}' for _id in content.get('state')]
            for state_id in states:
                payload = {state_id: {uid: mode_type}}
                self._update_nested(self.mode_switch, payload)
        return self.mode_switch

    def save(self, data: dict = None):
        """extended save method

           parse terminal work modes (menu sets) and attached files
           typical config looks like:

           {
                'file_list': {
                    '1620381838-nvuEWpoF': 'http://127.0.0.1/media/text/документ.txt'
                },
                'mode_list': {
                    'normal': [
                        'http://127.0.0.1/api/workmode/1'
                    ],
                    'extended': [
                        'http://127.0.0.1/api/workmode/1'
                    ]
                },
                    'alert': '2',
                    'uid': '080027cf78c2',
                    'timestamp': 1620469674,
                    'powered': True,
                    'blocked': True,
                    'hacked': False
                }
           }

        """
        if not data:
            return super().save()

        self.logger.error(f'{data}')

        try:
            if data.get('mode_list'):
                # resetting mode_switch
                self.mode_switch = {}
                unique_mode_urls = list(set(sum(list(data['mode_list'].values()), [])))
                self.workmodes = self.get_workmodes(unique_mode_urls)

                # data.update(FORCE=True)
                for mode_type in ['normal', 'extended']:
                    # fixme: forced should be optional
                    self.gen_mode_switch(mode_type)

                data.update(menu=self.workmodes)

            data.update(assets=self.get_files(data))
            self.logger.info(f'{self.mode_switch}')

            try:
                # oh, well, that's a crutch
                # should be fixed when full pub/sub pattern for client event queue will be implemented
                device = self.system.get('device')
                device.switch_page('main')
            except Exception:
                raise
            super().save(payload=data)
        except Exception:
            raise
