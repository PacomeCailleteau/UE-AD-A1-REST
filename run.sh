# Un script qui lance tous les services en même temps (les microservices sont des
#application Flask en Python)

# Lancer le microservice showtime
cd showtime
python3 showtime.py &
cd ..

# Lancer le microservice booking
cd booking
python3 booking.py &
cd ..

# Lancer le microservice movie
cd movie
python3 movie.py &
cd ..

# Lancer le microservice user
cd user
python3 user.py &
cd ..
