from os import environ


def get_env_variable(key: str) -> str:
    value = environ.get(key)
    if value is None:
        raise ValueError(f"Write {key} in the environment variables.")
    return value


def load_bot_token() -> str:
    return get_env_variable("TOKEN")


def load_db_url() -> str:
    return get_env_variable("DB_URL")
