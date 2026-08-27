INSERT INTO artists (id, name) VALUES (1, 'A-ha'); 
INSERT INTO artists (id, name) VALUES (2, 'Alex North');
INSERT INTO artists (id, name) VALUES (3, 'Ludwig van Beethoven');
INSERT INTO artists (id, name) VALUES (4, 'Elton John');
INSERT INTO artists (id, name) VALUES (5, 'Caifanes');
INSERT INTO artists (id, name) VALUES (6, 'Belanova');
INSERT INTO artists (id, name) VALUES (7, 'Doris Day');
INSERT INTO artists (id, name) VALUES (8, 'Green Day');
INSERT INTO artists (id, name) VALUES (9, 'Soda Stereo');
INSERT INTO artists (id, name) VALUES (10, 'Coldplay');

-- file_path = solo el nombre del archivo. Cada modo resuelve su carpeta en el cliente:
--   PIANO -> StreamingAssets/PianoSongs/Songs/{file_path}
--   CANTO -> StreamingAssets/SingSongs/Songs/{basename}.json + .wav
INSERT INTO songs (musical_genre, musical_key, title, duration, mode, tempo, file_path, artist_id) VALUES 
('Synth-Pop', 'A', 'Take On Me', 229, 'CANTO', 169, 'take_on_me.json', 1),
('Punk', 'Fm', 'Boulevard Of Broken Dreams', 167, 'CANTO', 170, 'boulevard_of_broken_dreams.json', 8),
('Pop', 'Bm', 'Rosa Pastel', 212, 'CANTO', 128, 'rosa_pastel.json', 6),
('Jazz', 'C', 'Dream a Little Dream', 213, 'CANTO', 77, 'dream_a_little_dream.json', 7),
('Classical', 'Am', 'Für Elise', 231, 'PIANO', 98, 'furelise.mid', 3),
('Classical', 'C#m', 'Moonlight Sonata', 307, 'PIANO', 55, 'moonlightSonata.mid', 3),
('Classical', 'C', 'Himno a la Alegria', 32, 'PIANO', 60, 'himnoALaAlegria.mid', 3),
('Rock Alternativo', 'F', 'The Scientist', 264, 'PIANO', 73, 'thescientist.mid', 10),
('Rock', 'D', 'Persiana Americana', 312, 'PIANO', 101, 'persianaamericana.mid', 9);
