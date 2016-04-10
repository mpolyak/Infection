"""
Copyright (c) Michael Polyak. All rights reserved.
"""

import string
import random

from random import seed, random, randrange
from math import sqrt
from queue import PriorityQueue

def edge_rank(graph, dampen=0.85, tolerance=0.0001):
    users = len(graph.keys())

    if not users:
        return {}

    probability = 1 / users

    vector = {}
    matrix = {}

    # Initialize probabilities for each user and calculate bi-directional edge matrix.
    for user, edges in graph.items():
        vector[user] = probability

        if user not in matrix:
            matrix[user] = []

        for other in edges:
            if other not in matrix[user]:
                matrix[user].append(other)

            if other not in matrix:
                matrix[other] = []

            if user not in matrix[other]:
                matrix[other].append(user)

    coefficient = (1 - dampen) / users

    rank = []

    # Calculate rank until probabilities converge.
    while len(rank) < users:
        rank = []

        for user, probability in vector.items():
            total = 0

            if user in matrix:
                for other in matrix[user]:
                    total += vector[other] / users

            p = coefficient + (dampen * total)

            if p >= probability - tolerance and p <= probability + tolerance:
                rank.append(p)

            vector[user] = p

    return vector

def edge_matrix(graph):
    matrix = {}

    # Calculate connections matrix, treat each edge in graph as bi-directional.
    for user, edges in graph.items():
        if user not in matrix:
            matrix[user] = []

        for other in edges:
            if other not in matrix[user]:
                matrix[user].append(other)

            if other not in matrix:
                matrix[other] = []

            if user not in matrix[other]:
                matrix[other].append(user)

    return matrix

def trace_users(graph, user, visited):
    if user in visited or user not in graph:
        return []

    visited.append(user)

    users = [user]

    # Collect all connected users.
    for other in graph[user]:
        users += trace_users(graph, other, visited)

    return users

class Population:
    def __init__(self, size=0, edge_probability=0.5, random_seed=None):
        size = max(size, 0)

        self.users = []
        self.versions = []

        # Generate names for each user in sequence.
        for i in range(size):
            self.users.append("".join([string.ascii_uppercase[(i + j) % 26]
                for j in range(int(i / 26) + 1)]))

            # Everyone is on the same version to start.
            self.versions.append(0)

        self.graph = {}

        seed(random_seed)

        # For each user randomly generate N edges to others given the specified probability.
        for i, user in enumerate(self.users):
            self.graph[user] = []

            edges = 1

            while random() <= edge_probability / sqrt(edges):
                other = self.users[randrange(size)]

                if other != user and other not in self.graph[user]:
                    self.graph[user].append(other)

                edges += 1

    def load(self, user_versions, user_graph):
        self.users = []
        self.versions = []

        self.graph = {}

        # Load users and versions.
        for user, version in user_versions.items():
            self.users.append(user)
            self.versions.append(version)

            # Initialize user node.
            self.graph[user] = []

        # Connect users.
        for user, edges in user_graph.items():
            self.graph[user] = edges

    def get_user_versions(self):
        # Return list of user, version tuples.
        return [(user, self.versions[self.users.index(user)])
            for user in self.users]

    def get_user_graph(self):
        # Return list of connections from user, to user tuples.
        return [(user, other) for user in self.graph
            for other in self.graph[user]]

    def infect(self, users):
        count = len(users)

        if count:
            version = max(self.versions)

            # Increment all linked users version.
            for user in users:
                self.versions[self.users.index(user)] = version + 1

        return count

    def full_infection(self, user):
        # Infect all those connected to 'user'.
        return self.infect(trace_users(edge_matrix(self.graph), user, []))

    def limited_infection(self, count):
        queue = PriorityQueue()

        # Prioritize users with the least number of connections.
        for user, rank in edge_rank(self.graph).items():
            queue.put((rank, user))

        traces = []
        unique = []

        graph = edge_matrix(self.graph)

        # Collect unique lists of connected users.
        while not queue.empty():
            _, user = queue.get()

            # Calculate list of connected users.
            trace = trace_users(graph, user, unique)

            _count = len(trace)

            if _count <= count:
                # Exact count match, infect users.
                if _count == count:
                    return self.infect(trace)
            else:
                break

            if _count:
                traces.insert(0, trace)

                # Keep list of all found users.
                unique = list(set(unique + trace))

                if len(unique) == count:
                    return self.infect(unique)

        unique = []

        # Build up list of users up to the requested count for infection.
        for trace in traces:
            _count = len(unique) + len(trace)

            if _count > count:
                continue

            unique += trace

            if _count == count:
                break

        return self.infect(unique)