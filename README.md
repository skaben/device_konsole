# smart_tester

основа для умного девайса. все Boilerplate переименуйте в желаемое имя устройства.
перед стартом необходимо сказать `./pre-run.sh` для создания виртуального окружения и копирования системного конфига.

компоненты:

### device

содержит интерфейс с локальным конфигурационным файлом и отправки сообщений на сервер.

```
    state_reload -> загрузить текущий локальный конфиг из файла
    state_update(data -> dict) -> записать данные в локальный конфиг и послать на сервер
    send_message(data -> any) -> отправить сообщение без записи в локальный конфиг
```

### config

- системный конфиг генерируется из `system_config.yml.template`, в процессе работы приложения не изменяется, хранится в `conf/system.yml`.
- конфиг устройства (приложения) изменяется в ходе работы, при первом запуске минимальный конфиг, описанный в `config.ESSENTIAL` будет записан в файл `conf/device.yml`

### пример

скажем, для устройства `Door`, имеющего параметр `closed`:


##### device.py

Создаем класс с желаемым именем, не забываем поправить имя класса конфига.

```
class CloseDevice(BaseDevice)

    config_class = CloseConfig

    def __init__(self, system_config, device_config, **kwargs):
        super().__init__(system_config, device_config)
        self.running = None
```
описываем поведение устройства
```
    def run(self):
        super().run()
        self.running = True
        while self.running:
            status = self.check_status()
```
сохраняем состояние
```
            if status == "closed":
                self.state_update({"closed": True})
```
или отправляем любое сообщение о событии
```
            elif status == "touched":
                self.send_message("I was touched")
```
