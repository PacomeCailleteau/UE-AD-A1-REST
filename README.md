# UE-AD-A1-REST
### Auteurs
- Nicolas CHUSSEAU
- Pacôme CAILLETEAU
- Marina CARBONE
---

Pour le microservice User, nous avons décidé d'implémenter les fonctionnalités suivantes :
- ``POST - /users`` Créer un utilisateur
- ``GET - /users`` Récupérer tous les utilisateurs
- ``GET - /users/lastactive`` Récupérer tous les utilisateurs triés par leur dernière connexion
- ``GET - /users/{userid}`` Récupérer un utilisateur via son id
- ``DELETE - /users/{userid}`` Supprimer un utilisateur
- ``PUT - /users/{userid}`` Mettre à jour un utilisateur
- ``GET - /users/{userid}/bookings`` Récupérer les films réservés par un utilisateur
- ``GET - /users/{userid}/bookings/movies`` Récupérer les films réservés par un utilisateur et les informations associées aux films
- ``GET - /help`` Récupérer la liste des routes disponibles

Pour le microservice Movie, nous avons décidé d'implémenter les fonctionnalités suivantes :
- ``GET - /json`` Récupérer tous les films
- ``GET - /movies/{movieid}`` Récupérer un film via son id
- ``GET - /movies/rate`` Récupérer les films triés par leur note (best or worst)
- ``GET - /moviebytitle`` Récupérer un film via son titre
- ``GET - /moviesbydirector`` Récupérer les films d'un réalisateur
- ``POST - /addmovie/{movieid}`` Créer un film
- ``PUT - /movies/{movieid}/{rate}`` Mettre à jour la note d'un film
- ``DELETE - /movies/{movieid}`` Supprimer un film via son id

Pour le microservice Showtime, nous avons décidé d'implémenter les fonctionnalités suivantes :
- ``GET - /showtimes`` Récupérer tous les horaires
- ``GET - /showtimes/{date}`` Récupérer les horaires d'une date donnée

Pour le microservice Booking, nous avons décidé d'implémenter les fonctionnalités suivantes :
- ``GET - /bookings`` Récupérer toutes les réservations
- ``GET - /bookings/{userid}`` Récupérer les réservations d'un utilisateur
- ``POST - /bookings/{userid}`` Créer une réservation pour un utilisateur

## Lancer le projet
Avant de lancer le script, il faut télécharger les dépendances du fichier requirements.txt.  
Pour lancer le projet, il suffit de lancer le script `run.sh` à la racine du projet. Ce script va lancer les serveurs REST.
Les microservices lancés sont les suivants :
- [Movie](http://localhost:3200)
- [Booking](http://localhost:3201)
- [Showtime](http://localhost:3202)
- [User](http://localhost:3203)

Chaque microservice contient un fichier .yaml contenant la documentation de l'API.
L'endpoint [/help](http://localhost:3203/help) de User permet de voir les différentes routes disponibles pour ce microservice.

