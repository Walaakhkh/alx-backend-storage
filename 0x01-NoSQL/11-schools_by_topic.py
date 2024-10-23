#!/usr/bin/env python3
""" 11-schools_by_topic """


def schools_by_topic(mongo_collection, topic):
    """Return the list of schools having a specific topic.

    Args:
        mongo_collection: The pymongo collection object.
        topic (str): The topic to search for.

    Returns:
        List of schools (documents) having the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))
