from importlib import reload
import src.config as config_module

def test_openai_api_key(monkeypatch):
    # Set the environment variable and reload the config module.
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    reload(config_module)
    assert config_module.Config.OPENAI_API_KEY == "test_key"