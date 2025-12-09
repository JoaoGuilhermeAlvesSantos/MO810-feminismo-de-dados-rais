SELECT
  cbo_2002,
  COUNT(*) AS total_registros
FROM `basedosdados.br_me_rais.microdados_vinculos`
WHERE id_municipio = '3509502'
GROUP BY cbo_2002
ORDER BY total_registros DESC
LIMIT 150000;