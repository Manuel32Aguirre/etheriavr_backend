INSERT INTO artists (id, name) VALUES (1, 'A-ha');
INSERT INTO artists (id, name) VALUES (2, 'Alex North');
INSERT INTO artists (id, name) VALUES (3, 'The Beatles');
INSERT INTO artists (id, name) VALUES (4, 'Elton John');
INSERT INTO artists (id, name) VALUES (5, 'Caifanes');

INSERT INTO songs (musical_genre, musical_key, title, duration, mode, tempo, file_path, artist_id) 
VALUES 
('Synth-Pop', 'A', 'Take On Me', 229, 'CANTO', 169, 'songs/take_on_me', 1),
('Rock', 'G', 'Matenme Porque Me Muero', 229, 'CANTO', 170, 'songs/matenme_porque_me_muero', 5),
('Rock', 'C', 'Unchained melody', 229, 'PIANO', 169, 'songs/unchainedmelody.json', 2);
('Rock', 'C', 'Let it be', 229, 'PIANO', 169, 'songs/letitbe.json', 3);
('Synth-Pop', 'A', 'Take On Me', 229, 'CANTO', 169, 'songs/bohemian.midi', 1);

