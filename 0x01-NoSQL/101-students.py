#!/usr/bin/env python3
"""
unction that returns all students sorted by average score
"""


def top_students(mongo_collection):
    # List to store students with their average scores
    result = []
    
    # Iterate through each student document in the collection
    for student in mongo_collection.find():
        if 'topics' in student and student['topics']:
            # Calculate the average score
            total_score = sum(topic['score'] for topic in student['topics'])
            average_score = total_score / len(student['topics'])
            # Append the student information along with the average score
            result.append({
                '_id': student['_id'],
                'name': student['name'],
                'averageScore': average_score
            })

    # Sort the result by averageScore in descending order
    return sorted(result, key=lambda x: x['averageScore'], reverse=True)
