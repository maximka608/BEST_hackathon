import heapq
import networkx as nx
import math


def haversine(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


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
            if kerb_height > 0.03:
                weight_factor *= (1.0 + kerb_height * 10)
                if kerb_height > 0.07:
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


def build_graph(osm_data, accessible=True):
    G = nx.Graph()
    nodes = {}

    for element in osm_data:
        if element['type'] == 'node':
            nodes[element['id']] = (element['lat'], element['lon'])

    accessibility_modifier, is_accessible = calculate_accessibility_weight(element['tags'], accessible)
    weight_factor = accessibility_modifier

    for element in osm_data:
        if element['type'] == 'way':
            way_nodes = element['nodes']
            for i in range(len(way_nodes) - 1):
                node_a, node_b = way_nodes[i], way_nodes[i + 1]
                if node_a in nodes and node_b in nodes:
                    dist = haversine(nodes[node_a], nodes[node_b]) * weight_factor
                    G.add_edge(node_a, node_b, weight=dist)

    return G, nodes


def nearest_node(coord, nodes, max_distance=200):
    nearest = min(nodes.items(), key=lambda x: haversine(coord, x[1]))
    node_id, node_coords = nearest

    distance = haversine(coord, node_coords)
    if distance > max_distance:
        print(f"найближча нода дуже далекооо")

    return node_id


def astar_path(G, nodes, start_coord, end_coord):
    try:
        start_node = nearest_node(start_coord, nodes)
        end_node = nearest_node(end_coord, nodes)
    except ValueError:
        print("Error finding nearest nodes. Check if the coordinates are within the fetched area.")
        return None

    if start_node == end_node:
        return [start_node]

    def heuristic(a, b):
        return haversine(nodes[a], nodes[b])

    open_set = []
    closed_set = set()

    unique_counter = 0
    heapq.heappush(open_set, (heuristic(start_node, end_node), unique_counter, start_node))
    unique_counter += 1

    came_from = {}

    g_cost = {start_node: 0}

    f_cost = {start_node: heuristic(start_node, end_node)}

    while open_set:
        current_f, _, current_node = heapq.heappop(open_set)

        if current_node == end_node:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start_node)
            return path[::-1]

        closed_set.add(current_node)

        for neighbor in G.neighbors(current_node):
            if neighbor in closed_set:
                continue

            tentative_g_cost = g_cost[current_node] + G[current_node][neighbor]['weight']

            if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current_node
                g_cost[neighbor] = tentative_g_cost
                f_cost[neighbor] = tentative_g_cost + heuristic(neighbor, end_node)

                if neighbor not in [node for _, _, node in open_set]:
                    heapq.heappush(open_set, (f_cost[neighbor], unique_counter, neighbor))
                    unique_counter += 1

    print("No path found between the given points.")
    return None
