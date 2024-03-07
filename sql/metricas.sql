-- Queries com as métricas

-- 1. Total de pessoas com o mesmo nome por país

WITH country_count AS (
	SELECT name, country, COUNT(1) AS count
	FROM fact_user
	GROUP BY 1, 2
	HAVING COUNT(1) > 1
)
SELECT country, SUM(count) as sum
FROM country_count
GROUP BY 1
ORDER BY 2 DESC, 1


-- 2. Distribuição de pessoas por gênero por país

SELECT
    country,
    SUM(CASE WHEN gender = 'male' THEN 1 ELSE 0 END) AS male,
    SUM(CASE WHEN gender = 'female' THEN 1 ELSE 0 END) AS female
FROM fact_user
GROUP BY 1
ORDER BY 1


-- 2. Quantas pessoas da distribuição do ítem 2 possuí + de 50

SELECT
    country,
    SUM(CASE WHEN gender = 'male' THEN 1 ELSE 0 END) AS male,
    SUM(CASE WHEN gender = 'female' THEN 1 ELSE 0 END) AS female
FROM fact_user
WHERE  (CURRENT_DATE - INTERVAL '50 years') > date_of_birth
GROUP BY 1
ORDER BY 1