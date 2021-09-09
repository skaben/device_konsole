from typing import List
from skabenclient.config import DeviceConfigExtended

ESSENTIAL = {
    "state_current": '',
    "assets": {}
}


class KonsoleConfig(DeviceConfigExtended):

    menu: List[dict] = []
    SUPPORTED_NOT_FILES = [
        'game',
        'user',
    ]
    SUPPORTED_IS_FILES = [
        'audio',
        'video',
        'image',
        'text'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SUPPORTED = self.SUPPORTED_IS_FILES + self.SUPPORTED_NOT_FILES

    def get_mode(self):
        """get workmode for current alert state and terminal status (hacked|normal)"""
        try:
            current_state = self.get("alert")
            mode_type = "extended" if self.get("hacked") else "normal"

            if not current_state:
               raise Exception('no current state - blocking!')

            mode_switch = self.get("mode_switch", {})
            all_modes = self.get("mode_list", {})
            if mode_switch and all_modes:
                current_switch = mode_switch.get(current_state)
                if current_switch:
                    mode_id = current_switch.get(mode_type)
                    return all_modes.get(mode_id, {})
                else:
                    raise Exception('blocking')
        except Exception:
            raise

    def parse_menu(self, workmode: dict) -> list:
        result = []

        for item in workmode.get('menu_set', []):
            item_type = ''
            for _type in self.SUPPORTED:
                if _type in item.keys():
                    item_type = _type
            if not item_type:
                continue

            content = item.get(item_type)
            if item_type == 'text':
                item_content = self.parse_text_item(content)
            elif item_type in self.SUPPORTED_IS_FILES:
                item_content = self.parse_file_item(content)
            else:
                item_content = content
            result.append({
                'display': item.get('display'),
                'type': item_type,
                'data': item_content,
                'timer': item.get('timer', -1)
            })
        return result

    def get_local_path(self, item_hash):
        assets = self.get('assets')
        if not assets:
            self.logger.error('no assets!')
            return

        item = assets.get(item_hash, {})
        item_path = item.get('local_path')
        if not item_path:
            self.logger.error(f'no `local_path` found for {item}')
            return

        return item_path

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

    def save(self, data: dict = None):
        """extended save method"""
        if not data:
            return super().save()

        try:
            # todo: сделать обработку ошибки загрузки файлов, сейчас оно встает раком просто так само
            data.update(assets=self.get_files(data))

            try:
                # oh, well, that's a crutch
                # should be fixed when full pub/sub pattern for client event queue will be implemented
                device = self.system.get('device')
                device.switch_page('main')
            except Exception:
                raise
            super().save(payload=data)
        except Exception:
            logging.exception('while saving device config')
            raise
