-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';
SELECT transcript FROM interviews WHERE month = 7 AND day = 28 AND transcript LIKE '%bakery%';

-- The THIEF is:
SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25 AND activity = 'exit')
AND phone_number IN (SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60)
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = (SELECT id FROM flights WHERE month = 7 AND day = 29 AND origin_airport_id = 8 ORDER BY hour, minute LIMIT 1))
AND bank_accounts.account_number IN (SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw');

-- The city the thief ESCAPED TO:
SELECT city FROM airports WHERE id IN (SELECT destination_airport_id FROM flights WHERE month = 7 AND day = 29 AND origin_airport_id = 8 ORDER BY hour, minute LIMIT 1);

-- The ACCOMPLICE is:
SELECT name FROM people
WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60 AND caller IN (SELECT phone_number FROM people WHERE name = 'Bruce'))
