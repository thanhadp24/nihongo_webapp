INSERT INTO jlpt_levels (code, name, display_order) VALUES
('N5', 'JLPT N5', 1),
('N4', 'JLPT N4', 2),
('N3', 'JLPT N3', 3),
('N2', 'JLPT N2', 4),
('N1', 'JLPT N1', 5)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    display_order = VALUES(display_order);

