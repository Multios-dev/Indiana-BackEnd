from uuid import UUID

SGP_CREATOR = "http://scoutsetguidespluralistes.be"

_ENTITY_PATHS = {
    "user": "person",
    "organization": "organization",
    "event": "event",
    "membership": "membership",
    "participation": "participation",
}


def sgp_notation(entity_type: str, entity_id: UUID) -> str:
    path = _ENTITY_PATHS[entity_type]
    return f"{SGP_CREATOR}/{path}/{entity_id}"
