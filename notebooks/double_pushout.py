import networkx as nx
import networkx.algorithms.isomorphism as iso

def match_subgraph(L, G, K):
    """
    Match subgraph L in G such that the common part with K is preserved.
    Uses NetworkX graph isomorphism algorithm.
    """
    matcher = iso.GraphMatcher(G, L)
    matches = []

    # Find isomorphisms (subgraph matches) between L and subgraphs of G
    for subgraph in matcher.subgraph_isomorphisms_iter():
        # Check that the match preserves K (i.e., K is the common subgraph)
        match_preserves_K = True
        for k_node in K.nodes():
            if subgraph.get(k_node) is None:
                match_preserves_K = False
                break
        if match_preserves_K:
            matches.append(subgraph)
    
    return matches

def double_pushout(L, R, G, K):
    """
    Apply Double Pushout (DPO) transformation on the graph G using L, R, and K.
    L is the left graph, R is the right graph, and K is the context graph.
    """
    # Step 1: Match the left graph L in the target graph G (with context K)
    matches = match_subgraph(L, G, K)

    if not matches:
        print("No valid match found for L in G with context K.")
        return G
    
    # Step 2: Apply the transformation for each match
    for match in matches:
        # Match is a dict with the nodes of L mapped to nodes in G
        # Remove the subgraph L from G
        subgraph_nodes = list(match.values())
        G.remove_nodes_from(subgraph_nodes)
        
        # Step 3: Insert the right graph R into G
        for node in R.nodes():
            if node not in G:
                G.add_node(node)
        for edge in R.edges():
            G.add_edge(*edge)
    
    return G
