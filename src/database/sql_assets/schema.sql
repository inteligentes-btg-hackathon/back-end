CREATE TABLE IF NOT EXISTS variableincomes (
  id SERIAL PRIMARY KEY NOT NULL,
  customer_id int NOT NULL,
  bank_id int NOT NULL,
  name varchar,
  type varchar DEFAULT 'outros fundos de renda variável',
  exempt bool,
  interest_rate float,
  sell_date date DEFAULT null,
  date date,
  price float,
  rate float
  CONSTRAINT fk_author FOREIGN KEY(customer_id) REFERENCES clients(customer_id)
);
CREATE TABLE IF NOT EXISTS clients (
  customer_id varchar PRIMARY KEY NOT NULL UNIQUE,
  investments
);

CREATE TABLE IF NOT EXISTS banks (
  bank_id int PRIMARY KEY NOT NULL UNIQUE,
  brand varchar,
  cnpj varchar,
  clients varchar REFERENCES clients(customer_id)
);