# VASProjektni_zadatak_2026
U ovome repozitoriju nalaze se programska rješenja za (jednostavniju, ali korisnu) simulaciju epidemije korištenjem reaktivnih agenata u višeagentnim sustavima.

Ovaj sustav razvijan je u Windows operacijskom sustavu. 

Za njegovo pokretanje potrebno je kreirati virtualno okruženje te ga aktivirati.

Ukoliko već nije, potrebno je unutar okruženja instalirati spade (```pip install spade```) te pygame (```pip install pygame```).

Spade se pokreće naredbom ```spade run --host 127.0.0.1 --purge```.

Sam sustav, odnosno simulacija pokreće se naredbom ```python main.py```.

U konfiguracijskoj datoteci ```config.py``` podešavaju se postavke simulacije (broj agenata, veličina svijeta, postavke bolesti i prijenosa bolesti).
