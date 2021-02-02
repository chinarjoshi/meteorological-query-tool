name,command
columns,PRAGMA table_info ("climate")
stations,SELECT DISTINCT name FROM climate
output,SELECT * FROM climate WHERE name LIKE "%?%" AND date LIKE "%?%" ORDER BY name DESC LIMIT 1