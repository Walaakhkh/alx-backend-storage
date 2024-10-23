#!/usr/bin/env python3
""" 10-update_topics """


def update_topics(mongo_collection, name, topics):
    """Change all topics of a school document based on the name.

    Args:
        mongo_collection: The pymongo collection object.
        name (str): The school name to update.
        topics (list): The list of topics to set in the school document.
    """
    mongo_collection.update_many(
        {"name": name},  # Filter for the school by name
        {"$set": {"topics": topics}}  # Set the new topics
    )
