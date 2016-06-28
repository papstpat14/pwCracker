![FH Joanneum Logo](/doc/FHJ_Logo_Computer_60mm_rgb-01.jpg)
# pwCracker
A Distributed Computing Project

* Documentation Team: 1
     * Student: Stefan Jodl 1a
* Management Team2
     * Student: Papst Patrick 2a
* DB-Team3
     * Student: Patrick Kager 3a
     * Student: Alb Pellumbi 3b
* Message-Queue Team: 4
     * Student: Michael König 4a
     * Student: Alexander Schug 4b
* WebServer-Team 5
     * Student: Stefan Obendrauf 5a
     * Student: Michael Koch 5b
* Frontend Team 6
     * Student: Michael Purkart 6a
     * Student: Melanie Schneider 6b
* Workers 7
     * Student: Patrick Kainz 7a
     * Student: Markus Schalk 7b


## Structure
* /db Datenbank
* /server NodeJS + Frontend
* /worker Worker
* /doc Documentation
## Architecture
Schritt 1: GET Website von Node Server
Schritt 2: Client baut Websocket Verbindung auf und schickt MD5 Hash an den Server
Schritt 3: Node Server lässt den Hash vom Exchange in die Ordner Queues einsortieren
Schritt 4: Einer der Worker sortiert das Ergebnis in die Reply Queue einsortieren
Schritt 5: Node Server lässt Abbruchmeldung in die Control Queues einsortiert
Schritt 6: Client wird über Websocket über das Ergebnis informiert.
![Architekture](/doc/Architecture.jpg)


