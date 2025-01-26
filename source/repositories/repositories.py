from db.models.buildings import Building
from db.models.rooms import Room
from dependencies.dependencies import get_db_repository
from repositories.repository_sqla import RepositorySqla

room_repository = get_db_repository(Room, RepositorySqla)
building_repository = get_db_repository(Building, RepositorySqla)
