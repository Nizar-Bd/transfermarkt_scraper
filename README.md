<h1 align=center>Web Scraper for <a href=https://www.transfermarkt.com/>Transfermarkt</a></h1>

<h3>Purpose of this scraper</h2>  

The aim of this scraper is to create a dataset containing soccer players who played between 1980 and 2023 for each club in the following leagues :

ENGLISH PREMIER LEAGUE  
LA LIGA  
SERIE A  
BUNDESLIGA  
FRENCH LIGUE 1  
LIGA PORTUGAL BWIN  
DUTCH EREDIVISIE  
TURKISH SÜPERLIG  

For each club it creates a directory and a file like data/`league_name`/`club_name`/`club_name`.csv

Each CSV contains the following columns :

`name` : Full name of the player as registred on Transfermakt (str)  
`birth_date` : Birth date of the player, format : Mon XX XXX (str not a datetime object)  
`nation` : First nation of the player (str)  
`face_url` : URL of the face of the player (str)  
