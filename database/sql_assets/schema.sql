CREATE TABLE IF NOT EXISTS investments (
  id int PRIMARY KEY NOT NULL UNIQUE,
  customer_id varchar NOT NULL,
  bank_id int NOT NULL,
  name varchar,
  itype varchar DEFAULT 'Outros',
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
  banks_ids int ARRAY,
  investments_ids int ARRAY
);

CREATE TABLE IF NOT EXISTS profit_loss (
  customer_id varchar PRIMARY KEY NOT NULL UNIQUE,
  day_trade_profit float,
  swing_trade_profit float,
  cripto_profit float,
  fi_profit float,
  day_trade_accumulated_loss float,
  swing_trade_accumulated_loss float,
  fi_loss float,
  cripto_accumulated_loss float,
  acumulated_loss float,
  date date
);