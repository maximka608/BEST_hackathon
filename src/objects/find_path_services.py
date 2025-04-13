import heapq
import math

import networkx as nx


def haversine(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def calculate_accessibility_weight(tags, accessible=False):
    """
    Calculate weight modifier based on accessibility features.
    If accessible=True, paths that aren't wheelchair friendly get much higher weights.

    Returns:
    - weight_factor: the weight multiplier (lower is preferred)
    - is_accessible: boolean indicating if the way is accessible
    """
    if not accessible:
        return 1.0, True

    weight_factor = 1.0
    is_accessible = True

    wheelchair = tags.get('wheelchair', '')
    if wheelchair in ['no', 'limited']:
        weight_factor *= 10.0
        is_accessible = False
    elif wheelchair == 'yes':
        weight_factor *= 0.8

    if tags.get('highway') == 'steps':
        weight_factor *= 20.0
        is_accessible = False

    surface = tags.get('surface', '')
    if surface in ['cobblestone', 'cobblestone:flattened', 'paving_stones']:
        weight_factor *= 2.0
    elif surface in ['gravel', 'dirt', 'sand', 'mud']:
        weight_factor *= 5.0
        is_accessible = False
    elif surface in ['asphalt', 'concrete', 'paved']:
        weight_factor *= 0.9

    smoothness = tags.get('smoothness', '')
    if smoothness in ['bad', 'very_bad', 'horrible', 'very_horrible', 'impassable']:
        weight_factor *= 4.0
        is_accessible = False
    elif smoothness in ['excellent', 'good']:
        weight_factor *= 0.9

    if 'incline' in tags:
        try:
            incline_str = tags['incline'].rstrip('%')
            incline = abs(float(incline_str))
            if incline > 6:
                weight_factor *= (1.0 + incline / 5.0)
                if incline > 10:
                    is_accessible = False
        except ValueError:
            if tags['incline'] in ['steep', 'up', 'down']:
                weight_factor *= 3.0
                is_accessible = False

    if 'width' in tags:
        try:
            width_str = tags['width'].split()[0]
            width = float(width_str)
            if width < 0.9:
                weight_factor *= 5.0
                is_accessible = False
            elif width >= 1.5:
                weight_factor *= 0.9
        except ValueError:
            pass

    # Check kerb height
    if 'kerb' in tags:
        try:
            kerb_height = float(tags['kerb'])
            if kerb_height > 0.03:  # Kerbs > 3cm are difficult
                weight_factor *= (1.0 + kerb_height * 10)
                if kerb_height > 0.07:  # Kerbs > 7cm are very difficult
                    is_accessible = False
        except ValueError:
            if tags['kerb'] in ['raised', 'high']:
                weight_factor *= 3.0
                is_accessible = False
            elif tags['kerb'] in ['lowered', 'flush']:
                weight_factor *= 0.9

    if tags.get('handrail') == 'yes':
        weight_factor *= 0.95

    if tags.get('tactile_paving') == 'yes':
        weight_factor *= 0.95

    return weight_factor, is_accessible


# def build_graph(osm_data, accessible=False):
#     G = nx.Graph()
#     nodes = {}
#
#     for element in osm_data:
#         if element['type'] == 'node':
#             nodes[element['id']] = (element['lat'], element['lon'])
#             G.add_node(element['id'])  # Add standalone node to graph
#
#     for element in osm_data:
#         if element['type'] == 'way':
#             tags = element.get('tags', {})
#             weight_factor, _ = calculate_accessibility_weight(tags, accessible)
#             way_nodes = element['nodes']
#             for i in range(len(way_nodes) - 1):
#                 node_a, node_b = way_nodes[i], way_nodes[i + 1]
#                 if node_a in nodes and node_b in nodes:
#                     dist = haversine(nodes[node_a], nodes[node_b]) * weight_factor
#                     G.add_edge(node_a, node_b, weight=dist)
#
#     return G, nodes

def build_graph(osm_data, accessible=False):
    G = nx.Graph()
    nodes = {}

    for element in osm_data:
        if element['type'] == 'node':
            nodes[element['id']] = (element['lat'], element['lon'])

    for element in osm_data:
        if element['type'] == 'way':
            if 'tags' in element:
                accessibility_modifier, is_accessible = calculate_accessibility_weight(element['tags'], accessible)
                weight_factor = accessibility_modifier
            else:
                weight_factor = 1.0
            way_nodes = element['nodes']
            for i in range(len(way_nodes) - 1):
                node_a, node_b = way_nodes[i], way_nodes[i + 1]
                if node_a in nodes and node_b in nodes:
                    dist = haversine(nodes[node_a], nodes[node_b]) * weight_factor
                    G.add_edge(node_a, node_b, weight=dist)

    return G, nodes


def nearest_node(G, nodes, coord):
    from math import radians, cos, sin, asin, sqrt

    def haversine(lat1, lon1, lat2, lon2):
        # Radius of earth in meters
        R = 6371000
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        return 2 * R * asin(sqrt(a))

    min_dist = float('inf')
    nearest_node = None

    for node_id in G.nodes:
        lat, lon = nodes[node_id]
        dist = haversine(coord[0], coord[1], lat, lon)
        if dist < min_dist:
            min_dist = dist
            nearest_node = node_id

    return nearest_node


def astar_path(G, nodes, start_coord, end_coord):
    start_node = nearest_node(G, nodes, start_coord)
    end_node = nearest_node(G, nodes, end_coord)

    if start_node is None or end_node is None:
        print("No valid nearest node found for start or end.")
        return None

    if start_node == end_node:
        return [start_node]

    def heuristic(a, b):
        return haversine(nodes[a], nodes[b])

    open_set = []
    closed_set = set()
    came_from = {}
    g_cost = {start_node: 0}
    f_cost = {start_node: heuristic(start_node, end_node)}
    heapq.heappush(open_set, (f_cost[start_node], 0, start_node))
    unique_counter = 1

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current == end_node:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_node)
            return path[::-1]

        closed_set.add(current)

        for neighbor in G.neighbors(current):
            if neighbor in closed_set:
                continue
            tentative_g = g_cost[current] + G[current][neighbor]['weight']
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g
                f_cost[neighbor] = tentative_g + heuristic(neighbor, end_node)
                heapq.heappush(open_set, (f_cost[neighbor], unique_counter, neighbor))
                unique_counter += 1

    print("No path found.")
    return None
