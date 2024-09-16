# Scrapper pour reddit

[NOTE: Ceci est un vieux script non-finalisé mais que je mets en dépôt pour référence future pour moi-même]

Ce script permet de télécharger les media d'un subreddit ou d'un onglet d'une page d'un utilisateur. 
En option il est possible de spécifier le tri (pour les subreddits) ou l'onglet (pour les pages utilisateur).

Ce script est exécutable avec Python 3.x et nécessite les modules `requests` et `bs4` (BeautifulSoup).

Utilisation :
```bash
usage: scrap-reddit.py [-h] [--user] [--tab TAB] [--sort_by SORT_BY] [--limit LIMIT] sub

Reddit image scrapper

positional arguments:
  sub                   The name of the subreddit to scrap

options:
  -h, --help            show this help message and exit
  --user, -u            Scrap user page instead of subreddit
  --tab TAB, -t TAB     Tab to scrap in user page (default=submitted): overview, comments, submitted
  --sort_by SORT_BY, -s SORT_BY
                        Sorting of the subreddit (default=hot): hot, new, rising, controversial, top
  --limit LIMIT, -l LIMIT
                        Limit of pages to download (default: unlimited)
```