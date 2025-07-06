"""
Get the next ID for a model based on its prefix.
"""
from typing import Type
def get_next_id(model, sequence_name=None):
    """
    Get the next ID for a model based on its prefix.
    This function assumes that the model has a 'code' field.
    """
    from django.db import connection
    # Get the current database driver and check support each separately.
    driver = connection.vendor
    # For PostgreSQL, we can use the sequence name directly.

    if driver == 'postgresql':
        table = model._meta.db_table
        pk_column = model._meta.pk.column
        seq_name = sequence_name or f"{table}_{pk_column}_seq"
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT nextval(%s)", [seq_name])
            row = cursor.fetchone()
        return row[0] if row else 1

    elif driver == 'mysql':
        # For MySQL, we can use the AUTO_INCREMENT value.
        table = model._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s", [table])
            row = cursor.fetchone()
        return row[0] if row else 1

    elif driver == 'sqlite':
        # For SQLite, we can use the last inserted row ID.
        table = model._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT seq FROM sqlite_sequence WHERE name = %s", [table])
            row = cursor.fetchone()
        return row[0] + 1 if row else 1
    else:
        raise NotImplementedError(f"Database driver '{driver}' is not supported for get_next_id.")

def generate_code(model) -> str:
    """
    Generate a code based on the ID and an optional prefix.
    If no prefix is provided, it defaults to 'ID'.
    """
    prefix = model._get_prefix()
    # If model has id, use it. otherwise get next id and set it as the id
    if hasattr(model, 'id') and model.id:
        id_value = model.id
    else:
        id_value = get_next_id(model)
        model.id = id_value

    # Left pad the ID with zeros up to 4 digits
    id_str = str(id_value).zfill(4)
    # Combine prefix and ID to form the code
    code = f"{prefix}{id_str}"
    model.code = code
    return code