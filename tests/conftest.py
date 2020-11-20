import os
import yaml
import pytest
import shutil

root_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope="module")
def get_root():
    return root_dir


def write_config(config, fname):
    path = os.path.join(root_dir, "res", fname)
    try:
        with open(path, "w") as file:
            yaml.dump(config, file)
        return path
    except Exception:
        raise


def make_object(obj, path, system_config=None):
    if system_config:
        return obj(path, system_config)
    return obj(path, root=root_dir)


@pytest.fixture(autouse=True, scope="session")
def setup_tests():
    res = os.path.join(root_dir, "res")
    assets = os.path.join(root_dir, "res", "assets")
    for _ in [res, assets]:
        if not os.path.exists(_):
            os.mkdir(_)

    yield

    try:
        for _ in [res, assets]:
            shutil.rmtree(_, ignore_errors=True)
    except:
        # all hail virtualbox shared folders
        pass


@pytest.fixture()
def write_config_fixture():

    def _wrap(config, fname):
        return write_config(config, fname)

    return _wrap


@pytest.fixture()
def get_config(request):

    def _wrap(config_obj, config_dict, **kwargs):
        path = write_config(config_dict, kwargs.get('fname', 'not_named.yml'))
        config = make_object(config_obj, path, system_config=kwargs.get("system_config"))

        def _td():
            try:
                os.remove(path)
                os.remove(f"{path}.lock")
            except FileNotFoundError:
                pass
            except Exception:
                raise

        request.addfinalizer(_td)
        return config

    return _wrap
