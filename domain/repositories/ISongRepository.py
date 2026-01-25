from abc import ABC, abstractmethod

from domain.entities.song import Song

class ISongRepository(ABC):

    @abstractmethod
    def get_all_songs(self) -> list[Song]:
        pass
    
    @abstractmethod
    def get_song_by_id(self, song_id: int) -> Song:
        pass
    
    