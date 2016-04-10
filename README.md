# Infection
Infection simulation

## Description

This project simulates propogating a change through a population using graph traversing. A random population of users is generated or loaded from CSV files, where each user has a version number and any number of edges to other users.

Once the graph is created a full infection can be applied to a specific user and it will propogate to any connected edges, incrementing user versions.

A limited infection of a given size can be applied, where the system will attempt to find the requested number of users and increment their versions.

## Requirements

Python 3.4 or above, you may use the provided Vagrantfile for a testing enviornment.

## Unit Tests

```
$ python -m unittest
```

## Usage

### Population

**Usage: python infection.py [name] --population [size]**

This will generate a population of a given size and save the user versions and user graph as **[name]_user_versions.csv** and **[name]_user_graph.csv**

```
$ python infection.py test --population 10
```

This will generate a population of 10 users and save to **test_user_versions.csv**, **test_user_graph.csv** files.

```
$ cat test_user_versions.csv
user,version
A,0
B,0
C,0
D,0
E,0
F,0
G,0
H,0
I,0
J,0
$ cat test_user_graph.csv
user_from,user_to
C,D
E,J
F,I
G,I
H,B
J,D
```

### Visualize

**Usage: python infection.py [name] --visualize**

This will generate a visualization of user versions and connections for a given name and save it as **[name].html** file which can be opened in a browser.

```
$ python infection.py test --visualize
```

Creates **test.html** visualization.

![Alt text](/screenshots/test.png?raw=true "test")

### Full Infection

**Usage: python infection.py [name] --full [user]**

Infect user and any connections and save result to **[name]_full_user_versions.csv**, **[name]_full_user_graph.csv** files.

```
$ python infection.py test --full D
Infected 4 users
```

This will generate **test_full_user_versions.csv** and **test_full_user_graph.csv** files, which can be visualized.

```
$ python infection.py test_full --visualize
```

Creates **test_full.html** visualization.

![Alt text](/screenshots/test_full.png?raw=true "test full")

### Limited Infection

*** Usage: python infection.y [name] --limited [size]***

Infect users up to the requested size and save result to **[name]_limited_user_versions.csv**, **[name]_limited_user_graph.csv** files.

```
$ python infection.py test --limited 7
Infected 7 users of the 7 requested
```

This will generate **test_limited_user_versions.csv** and **test_limited_user_graph.csv** files, which can be visualized.

```
$ python infection.py test_limited --visualize
```

Creates **test_limited.html** visualization.

![Alt text](/screenshots/test_limited.png?raw=true "test limited")
