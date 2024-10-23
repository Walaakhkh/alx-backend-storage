#!/usr/bin/env python3
""" 9-insert_school """

def insert_school(mongo_collection, **kwargs):
    """Insert a new document in a collection based on kwargs.

    Args:
        mongo_collection: The pymongo collection object.
        **kwargs: The fields and values to insert in the new document.

    Returns:
        The new _id of the inserted document.
    """
    result = mongo_collection.insert_one(kwargs)  # Insert the document
    return result.inserted_id  # Return the _id of the new document
