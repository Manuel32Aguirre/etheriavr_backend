INSERT INTO artists (id, name) VALUES (1, 'A-ha');
INSERT INTO artists (id, name) VALUES (2, 'Alex North');
INSERT INTO artists (id, name) VALUES (3, 'The Beatles');
INSERT INTO artists (id, name) VALUES (4, 'Elton John');
INSERT INTO artists (id, name) VALUES (5, 'Caifanes');
INSERT INTO artists (id, name) VALUES (6, 'The scientist');
INSERT INTO artists (id, name) VALUES (7, 'Soda Stereo');

INSERT INTO songs (musical_genre, musical_key, title, duration, mode, tempo, file_path, artist_id) 
VALUES 
('Synth-Pop', 'A', 'Take On Me', 229, 'CANTO', 169, 'songs/take_on_me', 1),
('Rock', 'G', 'Matenme Porque Me Muero', 229, 'CANTO', 170, 'songs/matenme_porque_me_muero', 5),
('Synth-Pop', 'A', 'Take On Me', 229, 'CANTO', 169, 'songs/bohemian.midi', 1),
('Rock', 'F', 'The scientist', 229, 'PIANO', 73.5, 'songs/thescientist.json', 6),
('Rock', 'Bm', 'De musica ligera', 210, 'PIANO', 124, 'songs/demusicaligera.json', 7),
('Rock', 'Bm', 'Rocketman', 210, 'PIANO', 124, 'songs/rocketman.json', 4),
('Rock', 'C', 'Unchained melody', 229, 'PIANO', 169, 'songs/unchainedmelody.json', 2),
('Rock', 'D', 'Persiana Americana', 297, 'PIANO', 101, 'songs/persianaamericana.json', 7);
