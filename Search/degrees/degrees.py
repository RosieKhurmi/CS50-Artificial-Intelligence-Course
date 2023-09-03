# Rosie Khurmi
# August 20, 2023
# Find degrees of seperation between 2 actors from different csv files

import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    load_data(directory)

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}") 

''' BREADTH FIRST SEARCH ALGORITHM '''

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # path[] will hold the final solution
    path = [] # Hold final solution

    explored = set() # Hold all explored nodes

    # Create a starting node that holds the source
    start = Node(source, None, None)
    # Create the frontier as a queue object (BFS)
    frontier = QueueFrontier()
    # Add start to frontier
    frontier.add(start)

    # Infinite Loop
    while True:
        
        # If the frontier is empty, exit the loop
        if frontier.empty():
            break

        # Otherwise, remove the head of the frontier
        out = frontier.remove()

        # If the removed node is the target node
        if out.state == target:

            # Work backwards until source is reached
            # Add all node state(person_id) and action(movie_id) t path 
            while out.parent is not None:
                path.append((out.action, out.state))
                out = out.parent

            # Reverse path so it is in the correct order and exit the loop
            path.reverse()
            break

        # Else, add removed node to explored
        explored.add(out)

        # Neighbors will hold everyone who has starred with source
        neighbors = neighbors_for_person(out.state)
        # Transverse through neighbors
        for n in neighbors:
            # If frontier and explored does not already contain the state
            # Create a new Node object of each neightbor and add to frontier
            if not frontier.contains_state(n[1]) and n[1] not in explored:
                add = Node(n[1], out, n[0])  
                frontier.add(add)

    # If there are items in the path, return the path, else None
    if len(path) > 0:
        return path
    else: 
        return None

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
