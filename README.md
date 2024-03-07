# DESAFIO RBS

No desafio foi utilizado o Airflow como orquetrador do pipeline.
Para armazenar os dados foi utilizado o Postgres.

## Zonas do Datalake

### RAW ZONE

Nela são mantidos os resultados da API da forma que são extraídos, ou seja, sem qualquer alteração no payload.
Os dados são armazenados na tabela `user`, do schema `raw` no banco de dados `desafio_rbs`.

### CURATED ZONE

Nessa zona são armazenados os dados processados, após transformação e limpeza.
No processo de transformação foram excluídos alguns que poderiam ser considerados "dados sensíveis" em outras situações,
como por exemplo, as informações de `login`.

Esses dados estão armazenados na tabela `user` do schema `curated` no banco de dados `desafio_rbs`.

### APPLICATION ZONE

Zona com os dados destinados ao usuários finais, como por exemplo, em um datawarehouse.
Mas também é possível que os mesmos sejam destinados a microserviços em REST API, entre outros.

Neste caso, os dados enviados para a Application Zone são os necessários para a respostas das métricas do desafio.
Esses dados foram armazenados no banco de dados `datawarehouse` na tabela `fact_user`.

## Observações

#### DATALAKE

Foi utilizado o Postgres como repositório de dados pelo entendimento que o desafio desejava validar o conhecimento em
SQL.

Entretanto, uma solução mais apropriada é armazenar os dados das Zona RAW e Curated em um datalake em serviços como GCS,
S3.

#### APPLICATION ZONE (DW)

Para uma camada de aplicação, uma solução mais apropriada seria a utilizada de serviços como o BigQuery, Athena,
Redshift.

Não foram adicionados indices as tabelas, pois as consultas em geral fazem SeqScam.

## Regras de negócio

Poderia ser utilizado uma chave candidata para identificar registros duplicados, entretanto:

1. a utilização dos campos `id` não foi possível, isto porque, em muitos registros essa informação vinha em branco;
2. outra chave candidata seria o `email`, entretanto a API sempre gera essa informação com o
   padrão `{first name}.{last name}@example.com`. O que levaria a métrica a não retornar dados.

```
Em tempo: o valor `login`->`uuid` pode ser utilizado como chave candidata para identificar como usuário único.
Desta forma, iria alterar a tabela Curated e o código de inserção.
```

## IMPLEMENTAÇÃO

Os módulos:

- `hooks/randomuser`: abstração da API. Neste `hook` fica a lógica para realizar as chamadas a API com os diversos
  parâmetros disponíveis.
- `packages/pg_repository`: abstração das chamadas ao banco de dados.
- `projects/user_transform`: módulo para fazer a transformação dos dados do usuário para a Zona Curated.
- `projects/desafio_db/pipeline`: módulo que faz a conexão entre os outros módulos. Por exemplo, acesso a API
  pelo `hook/randomuser` e, posteriomente, a gravação do dados utilizando `packages/pg_repository`.
- `desafio_db`: a DAG que executa o pipeline.
