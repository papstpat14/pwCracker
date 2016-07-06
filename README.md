![FH Joanneum Logo](/doc/FHJ_Logo_Computer_60mm_rgb-01.jpg)
# pwCracker
_**A Distributed Computing Project**_

* Documentation Team: 
     * Student: Stefan Jodl 
* Management Team
     * Student: Papst Patrick 
* DB-Team
     * Student: Patrick Kager
     * Student: Alb Pellumbi
* Message-Queue Team:
     * Student: Michael König
     * Student: Alexander Schug
* WebServer-Team
     * Student: Stefan Obendrauf
     * Student: Michael Koch
* Frontend Team
     * Student: Julian Purkart
     * Student: Melanie Schneider
* Workers
     * Student: Patrick Kainz 
     * Student: Markus Schalk

## Structure
* /db Datenbank
* /server NodeJS + Frontend
* /worker Worker
* /doc Documentation

## Architecture
* Schritt 1: GET Website von Node Server
* Schritt 2: Client baut Websocket Verbindung auf und schickt MD5 Hash an den Server
* Schritt 3: Node Server lässt den Hash vom Exchange in die Ordner Queues einsortieren
* Schritt 4: Einer der Worker sortiert das Ergebnis in die Reply Queue einsortieren
* Schritt 5: Node Server lässt Abbruchmeldung in die Control Queues einsortiert
* Schritt 6: Client wird über Websocket über das Ergebnis informiert.

![Architekture](/doc/Architecture_new.jpg)

## How to install
* install node.js server
* install python compiler
* install database
	* mongoDB
	* redis
* prepare database with your hashes
	* for further information read /db/README.md

## How to run
* $ node server.js
* \<start your database\>
* reach website http://localhost:8080 




