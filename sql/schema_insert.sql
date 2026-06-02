-- Ny sql fil til at indsætte data fra vores csv fil til vores tables
-- Vi har vores csv fil som vi importerer vores ting fra

\copy Amino_acids(Name, Abbr, Letter, Molecular Formula,property) FROM 'C:/stien/til/din_fil.csv' 
DELIMITER ',' CSV HEADER;

--Nu indsætter vi vores forskellige gamemodes med titler som man skal kune vælge fra på hjemmesiden;
INSERT INTO Game_modes (Mode_name) VALUES
('Match one-letter code'),
('Match three-letter abbreviation'),
('Match property (hydrophobe/hydrophile)'),
('Match molecular formula');


