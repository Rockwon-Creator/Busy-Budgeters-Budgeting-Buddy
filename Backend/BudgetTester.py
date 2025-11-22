# Test Client for Budgeting Buddy

import BudgetingBuddy

def main():

    budget_obj = BudgetingBuddy.BudgetingBuddy()
    print(budget_obj)

    budget_obj.set_firstname("Jessie")
    budget_obj.set_lastname("Lee")
    budget_obj.set_bankname("Chase")
    budget_obj.set_accounttype("Chase Premier Savings")
    budget_obj.set_interestrate(0.02)
    budget_obj.set_startingbalance(10000)
    budget_obj.set_monthlydeposit(250)
    budget_obj.set_savingperiod(60)
    budget_obj.set_monthsyears("Months")
    budget_obj.calculate_finalbalance()
    print(budget_obj)

    budget_obj.set_savingperiod(0)
    # budget_obj.set_finalbalance(25017.63)
    budget_obj.calculate_savingsperiod()
    print(budget_obj)

    budget_obj.set_monthlydeposit(0)
    budget_obj.calculate_monthlydeposit()
    print(budget_obj)

main()

def calculate_balance(monthly_deposit, starting_balance, months_years, saving_period, interest_rate):
        # Calculate the yearly deposit
        yearly_deposit = monthly_deposit * 12
        print(yearly_deposit)
        # Starts final tally
        final_balance = starting_balance
        print(final_balance)
        # Set months to 0 in case we don't use it
        months = 0
        print(months)
        
        # Handle months vs. years
        if months_years == "Months":
            years = int(saving_period / 12)
            months = saving_period % 12
            print(years, months)
        else:
            years = saving_period
            print(years, months)

        for i in range(years):
            print(i)
            # final_balance += yearly_deposit
            # print(final_balance)
            print(interest_rate/100)
            final_balance *= (1 + (interest_rate/100))
            print(final_balance)
            final_balance += yearly_deposit
            print(final_balance)
        if months != 0:
            final_balance += (monthly_deposit * months)
            print(final_balance)

        print("outside the loop.", final_balance)  
        return final_balance

# print(calculate_balance(250, 10000, "Months", 60, .02))

def calculate_period(monthly_deposit, starting_balance, months_years, final_balance, interest_rate):
        # Calculate the yearly deposit
        yearly_deposit = monthly_deposit * 12
        # Starts time tally
        savings_period = 0
        # Starts balance tally
        current_balance = starting_balance

        if months_years == "Years":
            print("In years")
            while current_balance < final_balance:
                current_balance *= (1 + (interest_rate/100))
                current_balance += yearly_deposit
                savings_period += 1
        elif months_years == "Months":
            print("In months")
            while current_balance < final_balance:
                if savings_period % 12 == 0:
                    current_balance *= (1 + (interest_rate/100))
                    if current_balance >= final_balance:
                        break
                current_balance += monthly_deposit
                savings_period += 1
                if current_balance >= final_balance:
                    break

        # self.set_savingperiod(savings_period)
        return savings_period


# print(calculate_period(250, 10000, "Months", 25016.01, .02))
