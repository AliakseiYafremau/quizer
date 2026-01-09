from os import environ


def get_env_variable(key: str) -> str:
    value = environ.get(key)
    if value is None:
        raise ValueError(f"Write {key} in the environment variables.")
    return value


def load_bot_token() -> str:
    return get_env_variable("TOKEN")


def load_db_url() -> str:
    db_url = environ.get("DB_URL")
    if db_url:
        return db_url
    user = get_env_variable("DB_USER")
    password = get_env_variable("DB_PASS")
    port = get_env_variable("DB_PORT")
    host = get_env_variable("DB_HOST")
    database = get_env_variable("DB_NAME")
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"
