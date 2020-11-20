import os
import pytest
from flask import url_for, send_from_directory

from skabenclient.config import SystemConfig
from config import KonsoleConfig


def _iface():
    stream = os.popen(f"ip route | grep 'default' | sed -nr 's/.*dev ([^\ ]+).*/\\1/p'")
    iface_name = stream.read()
    stream.close()
    return iface_name.rstrip()

SYSTEM = {
    "topic": "terminal",
    "iface": _iface(),
    "assets_path": os.path.join("res", "assets"),
    "http_retries": 1
}


EXAMPLE = {
        "file_list": {
            "MqmVaQ7L": "/test/snd.ogg",
            "MqmVaQ7F": "/sound/snd.ogg",
            "MqmVaQ7R": "/another/snd.ogg",
        },
        "modes_normal": [
            "/api/workmode/1/"
        ],
        "modes_extended": [
            "/api/workmode/2/"
        ],
        "timestamp": 1605712087,
        "powered": True,
        "blocked": False,
        "hacked": False
}


@pytest.fixture
def get_system_config(get_config):
    return get_config(SystemConfig, SYSTEM, fname="system.yml")


def test_konsole_config(get_config, get_system_config):
    """test device config start with empty config no matter what in config file"""
    config = get_config(KonsoleConfig,
                        {},
                        fname="device.yml",
                        system_config=get_system_config)

    assert config.data == config.minimal_essential_conf


def test_konsole_extended_datahold_parsing(get_config, get_system_config, monkeypatch):
    config = get_config(KonsoleConfig,
                        {},
                        fname="device.yml",
                        system_config=get_system_config)
    monkeypatch.setattr(config, "parse_json", lambda x: x)
    monkeypatch.setattr(config, "parse_modes", lambda x: {"modes": x})
    monkeypatch.setattr(config, "asset_dirs", ["test", "sound", "another"])
    config.make_asset_dirs()

    example = {**EXAMPLE}
    config.save(example)

    assert config.data.get("extended") == {"modes":  EXAMPLE.get("modes_extended")}
    assert config.data.get("normal") == {"modes": EXAMPLE.get("modes_normal")}
    #assert config.data.get("assets") == {"files": EXAMPLE.get("file_list")}
