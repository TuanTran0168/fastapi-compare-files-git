def escape_percent_for_alembic(url: str) -> str:
    """
    Escape % to %% for ConfigParser / Alembic
    """
    return url.replace("%", "%%")