-- Insertar Artistas primero (para que existan las llaves foráneas)
INSERT INTO artists (id, name) VALUES (1, 'Beethoven');
INSERT INTO artists (id, name) VALUES (2, 'John Lennon');

-- Insertar Canciones respetando el orden de Song.py
INSERT INTO songs (musical_genre, musical_key, title, duration, mode, tempo, file_path, artist_id) VALUES ('Clásica', 'C#m','Claro de Luna',300,'PIANO',54,'songs/moonlight.midi',1),('Rock/Pop','C','Imagine',183,'CANTO', 76, 'songs/imagine.midi',2);