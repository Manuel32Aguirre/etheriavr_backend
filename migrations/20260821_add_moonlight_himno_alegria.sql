-- Añade solo Moonlight Sonata e Himno a la Alegria (PIANO MIDI).
-- Seguro para BD ya poblada: no borra canciones existentes.
-- file_path = solo filename → cliente resuelve StreamingAssets/PianoSongs/Songs/{file_path}

INSERT INTO songs (musical_genre, musical_key, title, duration, mode, tempo, file_path, artist_id)
SELECT 'Classical', 'C#m', 'Moonlight Sonata', 306, 'PIANO', 55, 'moonlightSonata.mid', 3
WHERE NOT EXISTS (
    SELECT 1 FROM songs WHERE file_path = 'moonlightSonata.mid' AND mode = 'PIANO'
);

INSERT INTO songs (musical_genre, musical_key, title, duration, mode, tempo, file_path, artist_id)
SELECT 'Classical', 'C', 'Himno a la Alegria', 32, 'PIANO', 120, 'himnoALaAlegria.mid', 3
WHERE NOT EXISTS (
    SELECT 1 FROM songs WHERE file_path = 'himnoALaAlegria.mid' AND mode = 'PIANO'
);
