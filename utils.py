import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()
tabela = 'CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, nome text, estrelas real, diaria real, cidade text)'
linha1 = 'INSERT INTO hoteis VALUES ("alpha", "Alpha Hotel", 4.5, 345, "Palmas")'
cursor.execute(tabela)
cursor.execute(linha1)
connection.commit()
connection.close()
