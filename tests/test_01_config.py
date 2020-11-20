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


ASSET_ROOT = os.path.join("res", "assets")


SYSTEM = {
    "topic": "terminal",
    "iface": _iface(),
    "assets_root": ASSET_ROOT,
    "asset_types": ['image', 'audio', 'video', 'text'],
    "http_retries": 1
}


@pytest.fixture
def get_system_config(get_config):
    cfg = get_config("system", SYSTEM, fname="system.yml")
    assert isinstance(cfg, SystemConfig)
    return cfg


def test_konsole_config(get_config, get_system_config):
    """test device config start with empty config no matter what in config file"""
    cfg = get_system_config
    config = get_config("dev", {"not": "minimal"},
                        fname="device.yml",
                        system_config=cfg)

    assert config.data == config.minimal_essential_conf


def test_konsole_extended_parsing(get_config, get_system_config, monkeypatch):
    config = get_config(KonsoleConfig,
                        {},
                        fname="device.yml",
                        system_config=get_system_config)
    config.make_asset_paths()

    ftype = "audio"
    fname = "snd.ogg"
    fhash = "1234AAA"

    monkeypatch.setattr(config, "get_json", lambda x: x)
    monkeypatch.setattr(config, "parse_modes", lambda x: {"modes": x})
    monkeypatch.setattr(config, "get_files_async", lambda x: {fhash: x[0]})  # WARN!!!

    EXAMPLE = {
        "file_list": {
            fhash: f"/{ftype}/{fname}",
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

    example = {**EXAMPLE}
    config.save(example)

    assert config.get("extended") == {"modes": EXAMPLE.get("modes_extended")}
    assert config.get("normal") == {"modes": EXAMPLE.get("modes_normal")}
    assert config.get("assets") == {
        fhash: {
            "local_path": os.path.join(get_system_config.root, ASSET_ROOT, ftype, fname),
            "hash": fhash,
            "url": f"/{ftype}/{fname}",
            "file_type": ftype,
            "loaded": False,
        }
    }
