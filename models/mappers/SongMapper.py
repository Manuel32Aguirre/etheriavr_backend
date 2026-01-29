from models.entities.Song import Song
from models.dto.response.SongResponse import SongResponse

class SongMapper:
    @staticmethod
    def toDto(entity: Song) -> SongResponse:
        if not entity: return None

        return SongResponse(
            id=entity.id,
            musical_genre=entity.musical_genre,
            musical_key=entity.musical_key,
            title=entity.title,
            duration=entity.duration,
            mode=entity.mode.value,
            tempo=entity.tempo,
            file_path=entity.file_path,
            artist_name=entity.artist.name if entity.artist else "Desconocido"
        )