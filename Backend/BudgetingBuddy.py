# Group 5 - Busy Budgeters
# Budgeting Buddy
# Creates an online budgeting / investment tool for users to calculate savings based on specific banking criteria.

class BudgetingBuddy:

    # Constructor
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.bank_name = ""
        self.account_type = ""
        self.interest_rate = 0.00
        self.starting_balance = 0.00
        self.monthly_deposit = 0.00
        self.saving_period = 0
        self.months_years = ""
        self.final_balance = 0.00

    # Set first name
    def set_firstname(self, first_name):
        self.first_name = first_name

    # Get first name
    def get_firstname(self):
        return self.first_name

    # Set last name
    def set_lastname(self, last_name):
        self.last_name = last_name

    # Get last name
    def get_lastname(self):
        return self.last_name

    # Set bank name
    def set_bankname(self, bank_name):
        self.bank_name = bank_name

    # Get bank name
    def get_bankname(self):
        return self.bank_name

    # Set account type
    def set_accounttype(self, account_type):
        self.account_type = account_type

    # Get account type
    def get_accounttype(self):
        return self.account_type

    # Set interest rate
    def set_interestrate(self, interest_rate):
        self.interest_rate = interest_rate

    # Get interest rate
    def get_interestrate(self):
        return self.interest_rate

    # Set starting balance
    def set_startingbalance(self, starting_balance):
        self.starting_balance = starting_balance

    # Get starting balance
    def get_starting_balance(self):
        return self.starting_balance

    # Set monthly deposit
    def set_monthlydeposit(self, monthly_deposit):
        self.monthly_deposit = monthly_deposit

    # Get monthly deposit
    def get_monthlydeposit(self):
        return self.monthly_deposit
        
    # Set saving period (number)
    def set_savingperiod(self, saving_period):
        self.saving_period = saving_period

    # Get saving period (number)
    def get_savingperiod(self):
        return self.saving_period

    # Set saving period (months/years)
    def set_monthsyears(self, months_years):
        self.months_years = months_years

    # Get saving period (months/years)
    def get_monthsyears(self):
        return self.months_years

    # Set final balance
    def set_finalbalance(self, final_balance):
        self.final_balance = final_balance

    # Get final balance
    def get_finalbalance(self):
        return self.final_balance
    
    # Calculate the savings of the account & set final balance
    def calculate_finalbalance(self):
        # calculate the monthly interest rate
        monthly_interest = (self.interest_rate / 100) / 12
        # Starts final tally
        final_balance = self.starting_balance
        
        # Handle months vs. years
        if self.months_years == "Months":
            months = self.saving_period
        else:
            months = self.saving_period * 12

        for i in range(months):
            final_balance += self.monthly_deposit
            final_balance *= (1 + monthly_interest)

        final_balance = round(final_balance, 2)    
        self.final_balance = final_balance
        return final_balance

    # Calculate the time needed to reach final balance
    def calculate_savingsperiod(self):
        # monthly interest rate
        monthly_interest = (self.interest_rate / 100) / 12
        # Starts time tally
        savings_period = 0
        # Starts balance tally
        current_balance = self.starting_balance
        target_balance = self.final_balance
        # Starts time tally
        savings_period = 0

        while current_balance < target_balance:
            current_balance += self.monthly_deposit
            current_balance *= (1 + monthly_interest)
            savings_period += 1

        if self.months_years == "Years":
            savings_period = savings_period / 12

        self.set_savingperiod(savings_period)
        return savings_period

    # Calculate the monthly deposit
    def calculate_monthlydeposit(self):
        # monthly interest rate
        monthly_interest = (self.interest_rate / 100) / 12

        # months and years
        if self.months_years == "Years":
            months = self.saving_period * 12
        else:
            months = self.saving_period

        starting_balance = self.starting_balance
        final_balance = self.final_balance

        # create compounding factor
        compound_factor = (1 + monthly_interest) ** months

        # find the deposit
        if monthly_interest == 0:
            monthly_deposit = (final_balance - starting_balance) / months
        else:
            monthly_deposit = (final_balance - starting_balance * compound_factor) * (monthly_interest / (compound_factor - 1))

        monthly_deposit = round(monthly_deposit, 2)
        self.monthly_deposit = monthly_deposit
        return monthly_deposit
            
    def __str__(self):
        return f"""
First Name: {self.first_name}
Last Name: {self.last_name}
Bank: {self.bank_name}
Account: {self.account_type}
Interest rate: {self.interest_rate}
Starting balance: {self.starting_balance}
Monthly Deposit: {self.monthly_deposit}
Savings Period: {self.saving_period}
Months/Years: {self.months_years}
Final Balance: {self.final_balance:,.2f}
        """
