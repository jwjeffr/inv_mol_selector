# inv_mol_selector

This repository contains a custom OVITO modifier that will select invalid molecules based on user-provided molecule templates and a pre-computed bond topology.

This is useful for atomistic simulations where one deletes overlapping atoms, likely creating invalid molecules in the process.

The modifier works by:

1. Creating a connected (and undirected) graph using the bond topology, where the graph's nodes and edges correspond to atoms and bonds respectively
2. Partitioning the graph into its connected components, each representing a molecule
3. Selecting all the atoms in a connected component if the connected component does not match any user-provided templates

All graph-related computations are done via the networkx Python package
