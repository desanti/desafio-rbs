# INSTALAÇÃO E CONFIGURAÇÃO DO PROJETO


## CONFIGURAÇÃO DAS CONEXÕES DO AIRFLOW

Executar os scripts `datalake.sql` e `datawarehouse.sql` para criar os banco de dados no Postgres.

Posteriormente, adicionar as seguintes conexões:


Conexão com o Postgres com o banco de dados que tem as zonas RAW e Curated

```commandline
Connection Id: db_desafio_rbs
Connection Type: Postgres
Host: localhost
Schema: desafio_rbs
Login: desafio_rbs
Password: desafio_rbs
```

Conexão com o Postgres com o banco de dados que tem as zonas Application (DW)

```commandline
Connection Id: dw_desafio_rbs
Connection Type: Postgres
Host: localhost
Schema: dw_desafio_rbs
Login: desafio_rbs
Password: desafio_rbs
```

Conexão com a API RandomUser

```commandline
Connection Id: http_randomuser
Connection Type: HTTP
Host: https://randomuser.me/
```

## CONFIGURANDO O AMBIENTE LOCAL

### **Pré-requisitos**

Criar a virtual env com a versão do Python 3.7

- Instalação do Python 3.7

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
sudo apt install python3.7-distutils
sudo apt install python3-dev
```

- Instalação do PostgreSQL

O Postgres permite que o Airflow seja configurado para executar `tasks` em paralelo, diferentemente do SQLite que é o banco de dados utilizado na instalação padrão do Airflow.

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

### **Configurando e instalando o Airflow**

Para instalar o Airflow, devem ser seguidos os passos descritos abaixo:

#### **Passo 1: Criar o banco de dados no Postgres**

Acessar o prompt do Postgres através do comando:

```bash
sudo -u postgres psql
```

Uma vez no prompt do Postgres deve ser executado as queries abaixo:

```sql
CREATE DATABASE airflow;
CREATE USER airflow WITH PASSWORD 'airflow';
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
```

#### **Passo 3: Alterando as configuração do Airflow**

O arquivo `.env` tem a configuração para a execução do Airflow com o Postgres.

#### **Passo 4: Instalando o Airflow**

Após todos os passos acima, executar o arquivo `install_airflow.sh` na pasta `src`.

O script faz a instalação de todos os pacotes necessários do Airflow, e também inicia pela primeira vez o Airflow.

### **Executando o Airflow**

Para iniciar o Airflow, basta executar:

```bash
./start_airflow.sh
```

Com a execução do script com sucesso, será apresentado o texto abaixo:

```bash
standalone | 
standalone | Airflow is ready
standalone | Login with username: admin  password: XxXxXxxXX
standalone | Airflow Standalone is for development purposes only. Do not use this in production!
standalone |
```

Neste ponto o Airflow pode ser acessado através da url: <http://localhost:8080/> usando as credenciais:

- user: admin
- password: informada no output do script e também salva no arquivo `airflow/standalone_admin_password.txt`
