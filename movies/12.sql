SELECT movies.title FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE people.name = 'Bradley Cooper' OR people.name = 'Jennifer Lawrence'
GROUP BY movies.title
HAVING COUNT(people.name) = 2;
