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

CREATE TABLE IF NOT EXISTS profit_loss (
  customer_id varchar PRIMARY KEY NOT NULL UNIQUE,
  day_trade_profit FLOAT,
  swing_trade_profit FLOAT,
  cripto_profit FLOAT,
  fundos_imobiliarios_profit FLOAT,
  day_trade_accumulated_loss FLOAT,
  swing_trade_accumulated_loss FLOAT,
    fundos_imobiliarios_loss FLOAT,
  cripto_accumulated_loss FLOAT

);

