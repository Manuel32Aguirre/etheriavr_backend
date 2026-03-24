INSERT INTO artists (id, name) VALUES (3, 'Queen');
INSERT INTO artists (id, name) VALUES (4, 'Frédéric Chopin');
INSERT INTO artists (id, name) VALUES (5, 'Michael Jackson');
INSERT INTO artists (id, name) VALUES (6, 'Dave Brubeck');
INSERT INTO artists (id, name) VALUES (7, 'Ludwig van Beethoven');

INSERT INTO songs (musical_genre, musical_key, title, duration, mode, tempo, file_path, artist_id) 
VALUES 
('Synth-Pop', 'A', 'Take On Me', 229, 'CANTO', 169, 'songs/bohemian.midi', 3),
('Clásica', 'Eb', 'Nocturne Op. 9 No. 2', 270, 'PIANO', 60, 'songs/nocturne.midi', 4),
('Pop', 'F#m', 'Billie Jean', 294, 'CANTO', 117, 'songs/billiejean.midi', 5),
('Jazz', 'Ebm', 'Take Five', 324, 'PIANO', 174, 'songs/takefive.midi', 6),
('Clásica', 'Am', 'Test Song', 30, 'PIANO', 120, 'test_song.json', 7);