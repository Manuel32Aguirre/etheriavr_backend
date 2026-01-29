from sqlalchemy.orm import Session
from infrastructure.dao.SongDAO import SongDAO
from models.mappers.SongMapper import SongMapper
from models.dto.response.SongResponse import SongResponse

class SongService:
    def __init__(self, db: Session):
        self.dao = SongDAO(db)

    def getAllSongs(self) -> list[SongResponse]:
        listaCanciones = self.dao.getAll()
        lista_dtos = []
        for cancion in listaCanciones:
            dto = SongMapper.toDto(cancion)
            lista_dtos.append(dto)
        return lista_dtos
