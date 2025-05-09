from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.db.mongo import get_mongo_db, serialize_object_id
from src.objects.find_path_services import build_graph, astar_path
from src.objects.schemas import PathRequest
from src.utils.getters_services import get_all_objects, get_all_from_mongols, get_mongodb_data

object_router = APIRouter()

@object_router.get("/")
def get_objects_list(db: Session = Depends(get_db)):
    objects = get_all_objects(db)
    return objects


@object_router.get("/nodes")
def get_all_the_mongols(db: Session = Depends(get_mongo_db)):
    nodes = get_mongodb_data(db)

    if not nodes:
        return {"message": "No nodes found"}

    serialized_nodes = serialize_object_id(nodes)

    return {"message": "Mongols are here", "nodes": serialized_nodes}


@object_router.post("/find_path")
def find_path(request: PathRequest, db: Session = Depends(get_mongo_db)):
    nodes = get_mongodb_data(db)
    if not nodes:
        return {"message": "No nodes found"}
    # return {"message": "Mongols are here", "nodes": nodes}

    G, nodes = build_graph(nodes, accessible=request.accessible)
    # return {"": nodes}
    # return{"", G}

    path = astar_path(G, nodes, (request.start.lat, request.start.lon), (request.end.lat, request.end.lon))

    if path is None:
        return {"message": "No route found."}

    route_coords = [nodes[nid] for nid in path]
    return {"route": route_coords}