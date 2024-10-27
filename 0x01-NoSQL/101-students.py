#!/usr/bin/env python3
"""Module for retrieving top students from a MongoDB collection."""

def top_students(mongo_collection):
    """Returns all students sorted by average score.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of students sorted by average score.
    """
    result = []
    
    for student in mongo_collection.find():
        if 'topics' in student and student['topics']:
            total_score = sum(topic['score'] for topic in student['topics'])
            average_score = total_score / len(student['topics'])
            result.append({
                '_id': student['_id'],
                'name': student['name'],
                'averageScore': average_score
            })

    return sorted(result, key=lambda x: x['averageScore'], reverse=True)
