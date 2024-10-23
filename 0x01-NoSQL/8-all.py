#!/usr/bin/env python3
""" 8-all """


def list_all(mongo_collection):
    """List all documents in a collection.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of documents or an empty list if no document in the collection
    """
    return list(mongo_collection.find())
