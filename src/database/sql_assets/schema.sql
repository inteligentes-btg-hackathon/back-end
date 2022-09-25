CREATE TABLE IF NOT EXISTS investments (
  id int PRIMARY KEY NOT NULL UNIQUE,
  customer_id int NOT NULL,
  bank_id int NOT NULL,
  name varchar,
  type varchar DEFAULT 'Outros',
  exempt bool,
  interest_rate float,
  sell_date date DEFAULT null,
  date date,
  price float,
  rate float
);

CREATE TABLE IF NOT EXISTS banks (
  id int PRIMARY KEY NOT NULL UNIQUE,
  brand varchar,
  cnpj varchar
);

CREATE TABLE IF NOT EXISTS clients (
  customer_id varchar PRIMARY KEY NOT NULL UNIQUE,
  banks_id int ARRAY NOT NULL,
  investments_ids int ARRAY NOT NULL
);