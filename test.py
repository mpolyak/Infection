"""
Copyright (c) Michael Polyak. All rights reserved.
"""

import unittest

from infection.population import edge_rank, edge_matrix, trace_users, Population

class TestPopulation(unittest.TestCase):
    def test_edge_rank(self):
        graph = {'A': ['B'], 'B': ['C'], 'C': ['A']}

        unique = set()

        for rank in edge_rank(graph).values():
            unique.add(round(rank, 4))

        self.assertEqual(len(unique), 1)

    def test_edge_matrix(self):
        graph = {'A': ['B'], 'B': ['C'], 'C': ['A']}

        for user, edges in edge_matrix(graph).items():
            self.assertEqual(len(edges), 2)
            self.assertNotIn(user, edges)

    def test_trace_users(self):
        graph = {'A': ['B'], 'B': ['C'], 'C': ['A']}

        self.assertListEqual(sorted(trace_users(graph, 'A', [])), ['A', 'B', 'C'])

    def test_random(self):
        population = Population(5, 0.5, 1)

        self.assertListEqual(sorted(population.users), ['A', 'B', 'C', 'D', 'E'])
        self.assertSetEqual(set(population.versions), {0})
        self.assertDictEqual(population.graph, {'A': ['D'], 'E': ['D', 'B'], 'D': ['E'], 'B': ['D'], 'C': ['A']})

    def test_load(self):
        population = Population()

        population.load({'A': 0, 'B': 0, 'C': 0}, {'A': ['B'], 'B': ['C'], 'C': ['A']})

        self.assertListEqual(sorted(population.users), ['A', 'B', 'C'])
        self.assertSetEqual(set(population.versions), {0})
        self.assertDictEqual(population.graph, {'A': ['B'], 'B': ['C'], 'C': ['A']})

    def test_get_user_versions(self):
        population = Population()

        population.load({'A': 0, 'B': 0, 'C': 0}, {'A': ['B'], 'B': ['C'], 'C': ['A']})

        self.assertListEqual(sorted(population.get_user_versions(), key=lambda pair: list(pair)[0]),
            [('A', 0), ('B', 0), ('C', 0)])

    def test_get_user_graph(self):
        population = Population()

        population.load({'A': 0, 'B': 0, 'C': 0}, {'A': ['B'], 'B': ['C'], 'C': ['A']})

        self.assertListEqual(sorted(population.get_user_graph(), key=lambda pair: list(pair)[0]),
            [('A', 'B'), ('B', 'C'), ('C', 'A')])

    def test_infect(self):
        population = Population()

        population.load({'A': 0, 'B': 0, 'C': 0}, {'A': ['B'], 'B': ['C'], 'C': ['A']})

        self.assertEqual(population.infect(['A', 'B', 'C']), 3)

        self.assertSetEqual(set(population.versions), {1})

    def test_full_infection(self):
        population = Population()

        population.load({'A': 0, 'B': 0, 'C': 0}, {'A': ['B'], 'B': ['C'], 'C': ['A']})

        self.assertEqual(population.full_infection('A'), 3)

        self.assertSetEqual(set(population.versions), {1})

    def test_limited_infection(self):
        population = Population(10, 0.5, 1)

        population.load({'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}, {'A': ['B'], 'B': ['C'], 'C': ['A']})

        self.assertEqual(population.limited_infection(3), 3)

        self.assertListEqual(sorted(population.get_user_versions(), key=lambda pair: list(pair)[0]),
            [('A', 1), ('B', 1), ('C', 1), ('D', 0), ('E', 0)])

if __name__ == '__main__':
    unittest.main()