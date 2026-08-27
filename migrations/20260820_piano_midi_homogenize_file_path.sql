-- Homogeneiza file_path (solo nombre de archivo) y deja piano en MIDI.
-- Ejecutar manualmente si la BD ya tenía datos (import.sql solo corre con tabla vacía).

DELETE FROM practice_sessions;
DELETE FROM songs;
DELETE FROM artists;

INSERT INTO artists (id, name) VALUES (1, 'A-ha');
INSERT INTO artists (id, name) VALUES (2, 'Alex North');
INSERT INTO artists (id, name) VALUES (3, 'Beethoven');
INSERT INTO artists (id, name) VALUES (4, 'Elton John');
INSERT INTO artists (id, name) VALUES (5, 'Caifanes');
INSERT INTO artists (id, name) VALUES (6, 'Belanova');
INSERT INTO artists (id, name) VALUES (7, 'Doris Day');
INSERT INTO artists (id, name) VALUES (8, 'Green Day');
INSERT INTO artists (id, name) VALUES (9, 'Soda Stereo');
INSERT INTO artists (id, name) VALUES (10, 'Coldplay');

INSERT INTO songs (musical_genre, musical_key, title, duration, mode, tempo, file_path, artist_id) VALUES
('Synth-Pop', 'A', 'Take On Me', 229, 'CANTO', 169, 'take_on_me.json', 1),
('Punk', 'Fm', 'Boulevard Of Broken Dreams', 167, 'CANTO', 170, 'boulevard_of_broken_dreams.json', 8),
('Pop', 'Bm', 'Rosa Pastel', 212, 'CANTO', 128, 'rosa_pastel.json', 6),
('Jazz', 'C', 'Dream a Little Dream', 213, 'CANTO', 77, 'dream_a_little_dream.json', 7),
('Classical', 'Am', 'Fur Elise', 180, 'PIANO', 72, 'furelise.mid', 3),
('Classical', 'C#m', 'Moonlight Sonata', 306, 'PIANO', 55, 'moonlightSonata.mid', 3),
('Classical', 'C', 'Himno a la Alegria', 32, 'PIANO', 120, 'himnoALaAlegria.mid', 3);
