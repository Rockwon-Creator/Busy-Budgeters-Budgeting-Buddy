PRAGMA foreign_keys = ON;

-- Banks
CREATE TABLE IF NOT EXISTS banks (
  bank_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  website TEXT,
  support_phone TEXT
);

-- Products (checking/savings/etc.)
CREATE TABLE IF NOT EXISTS bank_products (
  product_id INTEGER PRIMARY KEY AUTOINCREMENT,
  bank_id INTEGER NOT NULL,
  product_type TEXT NOT NULL,        -- 'savings', 'checking', ...
  product_name TEXT NOT NULL,
  compounding_freq TEXT,             -- 'monthly','none',...
  interest_basis TEXT,               -- 'apy','none'
  notes TEXT,
  UNIQUE(bank_id, product_type, product_name),
  FOREIGN KEY(bank_id) REFERENCES banks(bank_id)
);

-- Terms/fees (versioned by date)
CREATE TABLE IF NOT EXISTS product_terms (
  term_id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL,
  effective_start DATE NOT NULL,
  effective_end DATE,
  minimum_open_deposit REAL,
  monthly_maintenance_fee REAL,
  fee_waiver_rules TEXT,
  atm_out_of_network_fee REAL,
  overdraft_fee REAL,
  notes TEXT,
  FOREIGN KEY(product_id) REFERENCES bank_products(product_id)
);

-- Simple rates (single APY; versioned)
CREATE TABLE IF NOT EXISTS interest_rate_history (
  rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL,
  rate_percent REAL NOT NULL,        -- APY as percent (e.g., 4.25)
  effective_start DATE NOT NULL,
  effective_end DATE,
  FOREIGN KEY(product_id) REFERENCES bank_products(product_id)
);

-- (Optional) Rate tiers (if you ever need them)
CREATE TABLE IF NOT EXISTS product_rate_tiers (
  tier_id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL,
  effective_start DATE NOT NULL,
  effective_end DATE,
  min_balance REAL DEFAULT 0,
  max_balance REAL,                  -- NULL = no upper bound
  apy_percent REAL NOT NULL,         -- APY as percent
  FOREIGN KEY(product_id) REFERENCES bank_products(product_id)
);

-- Categories for expense/income classification
CREATE TABLE IF NOT EXISTS categories (
  category_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  type TEXT NOT NULL                 -- 'income','expense','transfer', etc.
);

-- Users (for login/auth)
CREATE TABLE IF NOT EXISTS users (
  user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  username  TEXT NOT NULL UNIQUE,
  email     TEXT,
  password  TEXT NOT NULL
);
