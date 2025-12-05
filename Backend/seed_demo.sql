-- DEMO SEED DATA (Nov 2025 realistic-style values; not official quotes)

BEGIN TRANSACTION;

-- Banks
INSERT OR IGNORE INTO banks (name, website) VALUES
  ('Chase',           'https://www.chase.com'),
  ('Bank of America', 'https://www.bankofamerica.com'),
  ('Wells Fargo',     'https://www.wellsfargo.com'),
  ('Citi',            'https://www.citi.com'),
  ('U.S. Bank',       'https://www.usbank.com');

-- Products
-- Chase
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'checking', 'Total Checking', 'none', 'none', 'Basic checking with fee/waiver'
FROM banks WHERE name='Chase';
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'savings', 'High Yield Savings', 'monthly', 'apy', 'Online/high-yield style'
FROM banks WHERE name='Chase';

-- Bank of America
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'checking', 'Advantage Plus Banking', 'none', 'none', 'Everyday checking'
FROM banks WHERE name='Bank of America';
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'savings', 'Advantage Savings', 'monthly', 'apy', 'Standard savings'
FROM banks WHERE name='Bank of America';

-- Wells Fargo
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'checking', 'Everyday Checking', 'none', 'none', 'Basic checking'
FROM banks WHERE name='Wells Fargo';
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'savings', 'Way2Save Savings', 'monthly', 'apy', 'Branch-based savings'
FROM banks WHERE name='Wells Fargo';

-- Citi
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'checking', 'Access Checking', 'none', 'none', 'Basic checking'
FROM banks WHERE name='Citi';
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'savings', 'Accelerate Savings', 'monthly', 'apy', 'Online savings-style'
FROM banks WHERE name='Citi';

-- U.S. Bank
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'checking', 'Smartly Checking', 'none', 'none', 'Everyday checking'
FROM banks WHERE name='U.S. Bank';
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'savings', 'Standard Savings', 'monthly', 'apy', 'Standard savings'
FROM banks WHERE name='U.S. Bank';
INSERT INTO bank_products (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
SELECT bank_id, 'cd', '6-Month CD', 'monthly', 'apy', 'Short-term CD (demo)'
FROM banks WHERE name='U.S. Bank';

-- Terms (current)
-- Checking
INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules, atm_out_of_network_fee, overdraft_fee, notes)
SELECT product_id, '2025-10-01', 0.00, 12.00, 'Waived with $500 direct deposit or $1,500 daily balance', 3.00, 35.00, NULL
FROM bank_products WHERE product_name='Total Checking' AND product_type='checking';

INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules, atm_out_of_network_fee, overdraft_fee)
SELECT product_id, '2025-10-01', 0.00, 12.00, 'Waived with $250 direct deposit or $1,500 balance', 2.50, 35.00
FROM bank_products WHERE product_name='Advantage Plus Banking';

INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules, atm_out_of_network_fee, overdraft_fee)
SELECT product_id, '2025-10-01', 25.00, 10.00, 'Waived with $500 direct deposit or $500 daily balance', 2.50, 35.00
FROM bank_products WHERE product_name='Everyday Checking';

INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules, atm_out_of_network_fee, overdraft_fee)
SELECT product_id, '2025-10-01', 0.00, 10.00, 'Waived with qualifying deposits', 2.50, 35.00
FROM bank_products WHERE product_name='Access Checking';

INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules, atm_out_of_network_fee, overdraft_fee)
SELECT product_id, '2025-10-01', 25.00, 6.95, 'Waived with direct deposit or $1,500 balance', 2.50, 35.00
FROM bank_products WHERE product_name='Smartly Checking';

-- Savings
INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules, notes)
SELECT product_id, '2025-10-01', 0.00, 0.00, 'No monthly fee', 'High-yield style online savings (demo)'
FROM bank_products WHERE product_name='High Yield Savings';

INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules)
SELECT product_id, '2025-10-01', 100.00, 8.00, 'Waived with $500 daily balance'
FROM bank_products WHERE product_name='Advantage Savings';

INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules)
SELECT product_id, '2025-10-01', 25.00, 5.00, 'Waived with $300 daily balance'
FROM bank_products WHERE product_name='Way2Save Savings';

INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules, notes)
SELECT product_id, '2025-10-01', 0.00, 0.00, 'No monthly fee', 'Accelerate Savings (demo)'
FROM bank_products WHERE product_name='Accelerate Savings';

INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules)
SELECT product_id, '2025-10-01', 25.00, 4.00, 'Waived with $300 daily balance'
FROM bank_products WHERE product_name='Standard Savings';

-- CD terms
INSERT INTO product_terms (product_id, effective_start, minimum_open_deposit, monthly_maintenance_fee, fee_waiver_rules, notes)
SELECT product_id, '2025-10-01', 500.00, 0.00, 'Penalty for early withdrawal applies', '6-Month CD (demo)'
FROM bank_products WHERE product_name='6-Month CD';

-- Rates
-- Checking (no interest)
INSERT INTO interest_rate_history (product_id, rate_percent, effective_start, effective_end)
SELECT product_id, 0.00, '2025-10-01', NULL
FROM bank_products WHERE product_type='checking';

-- Savings tiers
-- Chase High Yield Savings
INSERT INTO product_rate_tiers (product_id, effective_start, min_balance, max_balance, apy_percent)
SELECT product_id, '2025-10-01', 0,     10000, 4.25 FROM bank_products WHERE product_name='High Yield Savings';
INSERT INTO product_rate_tiers (product_id, effective_start, min_balance, max_balance, apy_percent)
SELECT product_id, '2025-10-01', 10000, 50000, 4.40 FROM bank_products WHERE product_name='High Yield Savings';
INSERT INTO product_rate_tiers (product_id, effective_start, min_balance, max_balance, apy_percent)
SELECT product_id, '2025-10-01', 50000, NULL,  4.50 FROM bank_products WHERE product_name='High Yield Savings';

-- Bank of America Advantage Savings
INSERT INTO product_rate_tiers (product_id, effective_start, min_balance, max_balance, apy_percent)
SELECT product_id, '2025-10-01', 0, NULL, 0.01 FROM bank_products WHERE product_name='Advantage Savings';

-- Wells Fargo Way2Save
INSERT INTO product_rate_tiers (product_id, effective_start, min_balance, max_balance, apy_percent)
SELECT product_id, '2025-10-01', 0, NULL, 0.15 FROM bank_products WHERE product_name='Way2Save Savings';

-- Citi Accelerate Savings
INSERT INTO product_rate_tiers (product_id, effective_start, min_balance, max_balance, apy_percent)
SELECT product_id, '2025-10-01', 0, 25000, 4.20 FROM bank_products WHERE product_name='Accelerate Savings';
INSERT INTO product_rate_tiers (product_id, effective_start, min_balance, max_balance, apy_percent)
SELECT product_id, '2025-10-01', 25000, NULL, 4.35 FROM bank_products WHERE product_name='Accelerate Savings';

-- U.S. Bank Standard Savings
INSERT INTO product_rate_tiers (product_id, effective_start, min_balance, max_balance, apy_percent)
SELECT product_id, '2025-10-01', 0, NULL, 0.01 FROM bank_products WHERE product_name='Standard Savings';

-- CD
INSERT INTO interest_rate_history (product_id, rate_percent, effective_start, effective_end)
SELECT product_id, 5.00, '2025-10-01', NULL FROM bank_products WHERE product_name='6-Month CD';

-- Categories
INSERT OR IGNORE INTO categories (name, type) VALUES
  ('Salary','income'), ('Investments','income'),
  ('Groceries','expense'), ('Dining','expense'), ('Rent','expense'),
  ('Utilities','expense'), ('Transportation','expense'), ('Entertainment','expense'),
  ('Travel','expense'), ('Fees','fee'), ('Transfer','transfer');
-- Demo login user
INSERT OR IGNORE INTO users (username, email, password)
VALUES ('demo', 'demo@budgetingbuddy.com', 'password123');

COMMIT;
