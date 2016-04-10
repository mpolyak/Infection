"""
Copyright (c) Michael Polyak. All rights reserved.
"""

import argparse
import csv
import json

from string import Template

from infection.population import Population

def save_user_versions(name, population):
    with open("{}_user_versions.csv".format(name), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['user', 'version'])

        writer.writeheader()

        for user, version in population.get_user_versions():
            writer.writerow({'user': user, 'version': version})

def save_user_graph(name, population):
    with open("{}_user_graph.csv".format(name), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['user_from', 'user_to'])

        writer.writeheader()

        for user_from, user_to in population.get_user_graph():
            writer.writerow({'user_from': user_from, 'user_to': user_to})

def load_user_versions(name):
    users = {}

    with open("{}_user_versions.csv".format(name), 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            users[row['user']] = int(row['version'])

    return users

def load_user_graph(name):
    graph = {}

    with open("{}_user_graph.csv".format(name), 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            user_from = row['user_from']

            if user_from not in graph:
                graph[user_from] = []

            graph[user_from].append(row['user_to'])

    return graph

def generate_population(name, size):
    population = Population(size)

    # Save random population of given size.
    save_user_versions(name, population)
    save_user_graph(name, population)

def visualize_graph(name):
    user_versions = load_user_versions(name)
    user_graph = load_user_graph(name)

    index = {}
    users = []
    
    # Save user name and version.
    for i, user in enumerate(user_versions):
        index[user] = i

        users.append({'name': user, 'version': user_versions[user]})

    graph = []

    # Save edges between users.
    for user, edges in user_graph.items():
        i = index[user]

        for other in edges:
            j = index[other]

            graph.append({'source': i, 'target': j})

    with open('templates/visualize.html', 'r') as template:
        visualize = Template(template.read())

        with open("{}.html".format(name), 'w') as html:
            html.write(visualize.substitute(users=json.dumps(users), graph=json.dumps(graph)))

def full_infection(name, user):
    population = Population()

    # Load user versions and graph from files.
    population.load(
        load_user_versions(name),
        load_user_graph(name))

    # Infect user and those connected.
    infected = population.full_infection(user)

    print("Infected {} users".format(infected))

    # Save full infection user versions and graph.
    save_user_versions("{}_full".format(name), population)
    save_user_graph("{}_full".format(name), population)

def limited_infection(name, count):
    population = Population()

    # Load user versions and graph from files.
    population.load(
        load_user_versions(name),
        load_user_graph(name))

    # Infect N users.
    infected = population.limited_infection(count)

    print("Infected {} users of the {} requested".format(infected, count))

    # Save full infection user versions and graph.
    save_user_versions("{}_limited".format(name), population)
    save_user_graph("{}_limited".format(name), population)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('name', type=str, help='Infection name')
    parser.add_argument('--population', type=int, help="Generate random population of N users and save to {name}_user_versions.csv and {name}_user_graph.csv.")
    parser.add_argument('--visualize', action='store_true', help="Visualize named population.")
    parser.add_argument('--full', type=str, help="Infect named user of the population and any that are connected, and save to {name}_full_user_versions.csv and {name}_full_user_graph.csv.")
    parser.add_argument('--limited', type=int, help="Attempt to infect the number of specified users and save to {name}_limited_user_versions.csv and {name}_limited_user_graph.csv.")

    args = parser.parse_args()

    # Generate random population.
    if args.population is not None:
        generate_population(args.name, args.population)

    # Visualize population.
    if args.visualize:
        visualize_graph(args.name)

    # Full infection.
    if args.full:
        full_infection(args.name, args.full)

    # Limited infection.
    if args.limited is not None:
        limited_infection(args.name, args.limited)