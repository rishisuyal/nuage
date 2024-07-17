from db.db import db_session
from datetime import datetime


def orm_to_dict(orm):
    """
    Convert an ORM model instance to a dictionary.

    Args:
        orm: The ORM model instance.

    Returns:
        dict: A dictionary representation of the ORM model instance.
    """
    ret = {}
    for col in orm.__table__.columns:
        val = getattr(orm, col.name)
        if isinstance(val, datetime):
            ret[col.name] = str(val)
        else:
            ret[col.name] = getattr(orm, col.name)
    return ret


def save(obj, payload):
    """
    Save an ORM model instance with the provided payload.

    Args:
        obj: The ORM model instance to save.
        payload (dict): The payload data to set on the ORM model instance.

    Returns:
        dict: A success message indicating the save operation was successful.
    """
    for k, v in payload.items():
        obj.__setattr__(k, v)
    db_session.add(obj)
    db_session.flush()
    db_session.commit()
    return {"msg": "successful"}
