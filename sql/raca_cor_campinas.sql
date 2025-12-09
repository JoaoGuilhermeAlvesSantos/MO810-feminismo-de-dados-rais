SELECT
  raca_cor,
  COUNT(*) AS registros,
  COUNTIF(sexo = '1') AS masculino,
  COUNTIF(sexo = '2') AS feminino,
  COUNTIF(sexo NOT IN ('1', '2')) AS nao_identificado
FROM `basedosdados.br_me_rais.microdados_vinculos`
WHERE id_municipio = '3509502'
GROUP BY raca_cor
ORDER BY raca_cor;