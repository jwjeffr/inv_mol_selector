import dataclasses
import networkx


@dataclass
class StrayMoleculeSelector:

    templates: list[dict]
    
    def __call__(self, frame: int, data: ovito.Data.DataCollection) -> None:
    
        # create the selection from a mutable copy of particles
    
        selection = data.particles_.create_property('Selection')
        
        # get types and a set of unique types
        
        types = data.particles['Particle Type'][...]
        unique_types = set(list(types))
        
        # build the list of bonds from a pre-computed bond topology
        # each member of the list will be (a, b), where a and b are particle indices
        # and the a'th and b'th particle are bonded
    
        list_of_bonds = [tuple(data_arr) for data_arr in data.particles.bonds.topology]
        
        # create a graph from those bonds, with bonds corresponding to edges
        
        graph = networkx.from_edgelist(list_of_bonds)
        
        # partition into subgraphs from the connected components
        
        subgraphs = networkx.connected_components(graph)
        
        # loop through each subgraph (molecule)
        
        number_of_molecules_selected = 0
        for subgraph in subgraphs:
        
            # initialize the molecule's info corresponding to this subgraph
            # info is the number of each atom type in the molecule
        
            molecule = {type_: 0 for type_ in unique_types}
            
            # loop through the nodes (atoms) in the subgraph (molecule)
            
            for node in subgraph:
            
                # get the type of the atom at the node
            
                node_type = types[node]
                molecule[node_type] += 1
                
            # if the molecule matches any user provided templates, go to the next subgraph (molecule)
                
            if any([molecule == template for template in self.templates]):
                continue
                
            number_of_molecules_selected += 1
            
            # if the molecule isn't in any of the templates, select each node (atom) in the subgraph (molecule)
                
            for node in subgraph:
                selection[node] = 1
                
        print(f'{number_of_molecules_selected:.0f} bad molecules detected')
        if number_of_molecules_selected:
            print(f'{np.sum(selection == 1)} atoms selected from those molecules')