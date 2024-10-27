#!/usr/bin/env python3
"""Script that provides stats about Nginx logs stored in MongoDB."""

from pymongo import MongoClient
from collections import Counter


def log_stats():
    """Retrieves stats from the logs database."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Total logs
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # Methods statistics
    methods = Counter()
    for log in nginx_collection.find():
        methods[log['method']] += 1

    print("Methods:")
    for method, count in sorted(methods.items()):
        print(f"\tmethod {method}: {count}")

    # Status check statistics
    status_count = Counter()
    for log in nginx_collection.find():
        status_count[log['status']] += 1

    total_statuses = sum(status_count.values())
    print(f"{total_statuses} status check")

    # IP addresses statistics
    ip_count = Counter()
    for log in nginx_collection.find():
        ip_count[log['ip']] += 1

    print("IPs:")
    for ip, count in ip_count.most_common(10):
        print(f"\t{ip}: {count}")


if __name__ == "__main__":
    log_stats()
