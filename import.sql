INSERT INTO artists (id, name) VALUES (1, 'A-ha'); 
INSERT INTO artists (id, name) VALUES (2, 'Alex North');
INSERT INTO artists (id, name) VALUES (4, 'Elton John');
INSERT INTO artists (id, name) VALUES (5, 'Caifanes');
INSERT INTO artists (id, name) VALUES (6, 'Belanova');
INSERT INTO artists (id, name) VALUES (7, 'Doris Day');
INSERT INTO artists (id, name) VALUES (8, 'Green Day');
INSERT INTO artists (id, name) VALUES (9, 'Soda Stereo');
INSERT INTO artists (id, name) VALUES (10, 'Coldplay');

INSERT INTO songs (musical_genre, musical_key, title, duration, mode, tempo, file_path, artist_id) VALUES 
('Synth-Pop', 'A', 'Take On Me', 229, 'CANTO', 169, 'songs/take_on_me', 1),
('Rock', 'F', 'The scientist', 229, 'PIANO', 73.5, 'songs/thescientist.json', 10),
('Rock', 'G', 'Matenme Porque Me Muero', 229, 'CANTO', 170, 'songs/matenme_porque_me_muero', 5),
('Rock', 'Bm', 'De musica ligera', 210, 'PIANO', 124, 'songs/demusicaligera.json', 9),
('Punk', 'Fm', 'Boulevard Of Broken Dreams', 167, 'CANTO', 170, 'songs/boulevard_of_broken_dreams', 8),
('Rock', 'Bm', 'Rocketman', 210, 'PIANO', 124, 'songs/rocketman.json', 4),
('Pop', 'Bm', 'Rosa Pastel', 212, 'CANTO', 128, 'songs/rosa_pastel', 6),
('Rock', 'C', 'Unchained melody', 229, 'PIANO', 169, 'songs/unchainedmelody.json', 2),
('Jazz', 'C', 'Dream a Little Dream', 213, 'CANTO', 77, 'songs/dream_a_little_dream', 7),
('Rock', 'D', 'Persiana Americana', 297, 'PIANO', 101, 'songs/persianaamericana.json', 9);