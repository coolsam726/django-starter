import os

def env(key, default=None, var_type=str):
    """
    Get an environment variable, with optional default value and type conversion.

    :param key: The environment variable key.
    :param default: Default value if the key is not found.
    :param var_type: Type to convert the value to (default is str).
    :return: The value of the environment variable, converted to the specified type.
    """
    value = os.getenv(key, default)
    if value is None:
        return None

    if var_type == bool:
        return str(value).lower() in ['true', '1', 'yes', 'on', 'y', 't']
    try:
        return var_type(value)
    except (ValueError, TypeError):
        return default