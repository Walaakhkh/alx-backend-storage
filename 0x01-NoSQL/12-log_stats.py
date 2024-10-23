#!/usr/bin/env python3
""" 12-log_stats """

from pymongo import MongoClient


def print_log_stats():
    """Print statistics about Nginx logs stored in MongoDB."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Count total number of logs
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # Methods
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Count the number of GET requests with path = /status
    status_check_count = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    print_log_stats()
