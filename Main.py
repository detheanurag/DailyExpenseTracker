import json
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt


def load_expenses():
    try:
        with open("expenses.json","r")as file:
            return json.load(file)
    except (FileNotFoundError,json.JSONDecodeError):
        return[]
    
def save_expenses():
    with open("expenses.json","w")as file:
        json.dump(expenses,file,indent=4)

def get_next_id():
    if len(expenses)==0:
        return 1
    return max(expense["id"]for expense in expenses)+1

def set_budget():
    while True:
        try:
            budget=float(input("Enter your monthly budget: "))
            if budget<=0:
                print("Budget must be greater than 0. ")
            else:
                break
        except ValueError:
            print("Please enter a Valid number. ")
    with open("budget.json","w")as file:
        json.dump({"budget":budget},file,indent=4)
    print("Monthly budget saved successfully!")


def check_budget():
    try:
        with open("budget.json","r")as file:
            data=json.load(file)
    except FileNotFoundError:
        print("\nPlease set your budget first.")
        return
    budget=data["budget"]
    current_month=str(date.today())[:7]
    total=0
    for expense in expenses:
        if expense["date"].startswith(current_month):
            total=total+expense["amount"]
    remaining=budget-total
    print("\n----Budget Status-----")
    print("Monthly Budget:",budget)
    print("Spent:",total)
    print("Remaining:",remaining)
    if total>budget:
        print("Budget exceeded!")
    elif total>=budget*0.8:
        print("Warning: You have used 80 % your budget.")
    else:
        print("You are within your budget.")


def automatic_budget_warning():
    try:
        with open("budget.json","r")as file:
            data=json.load(file)
    except FileNotFoundError:
        return
    budget=data["budget"]
    current_month=str(date.today())[:7]
    total=0
    for expense in expenses:
        if expense["date"].startswith(current_month):
            total=total+expense["amount"]
    if total>budget:
        print("\n WARNING: You have exceeded your monthly budget!")
    elif total>=budget*0.8:
        print("\n WARNING: You have used 80% your monthly budget!")

def add_expense():
    while True:
        try:
            amount=float(input("Enter amount: "))
            if amount<=0:
                print("Amount must be greater than 0.")
            else:
                break
        except ValueError:
            print("Please enter a vaild number.")

    print("\nCategories:")
    print("1. Food")
    print("2. Travel")
    print("3. Shopping")
    print("4. Bills")
    print("5. Entertainment")
    print("6. Other")

    category_choice=input("Choose catagory: ")
    if category_choice=="1":
        category="Food"
    elif category_choice=="2":
        category="Travel"
    elif category_choice=="3":
        category="Shopping"
    elif category_choice=="4":
        category="Bills"
    elif category_choice=="5":
        category="Entertainment"
    else:
        category="Other"

    description=input("Enter description: ")

    today=str(date.today())

    expense={
        "id":get_next_id(),
        "amount":amount,
        "category":category,
        "description":description,
        "date":str(date.today())
    }
    expenses.append(expense)
    save_expenses()

    print("\nExpense added Successfully!")
    automatic_budget_warning()

def view_expenses():
    if len(expenses)==0:
        print("\nNo expenses found.")
        return
    
    print("\n------Your Expenses------")

    for expense in expenses:
        print("------------")
        print("ID:",expense["id"])
        print("Amount :",expense["amount"])
        print("Category :",expense["category"])
        print("Description :",expense["description"])
        print("Date :",expense["date"])

def analyze_expenses():
    if len(expenses)==0:
        print("No expenses found.")
        return
    df=pd.DataFrame(expenses)
    print("\nAll Expenses:")
    print(df)

    print("\nTotal Expense:")
    print(df["amount"].sum())

    print("\nAverage Expense:")
    print(df["amount"].mean())

    print("\nHighest Expense:")
    print(df["amount"].max())

def category_summary():
    if len(expenses)==0:
        print("No expenses found.")
        return
    df=pd.DataFrame(expenses)
    summary=df.groupby("category")["amount"].sum()
    print("\nExpense by Category:")
    print(summary)

def category_chart():
    if len(expenses)==0:
        print("No expenses found.")
        return
    df=pd.DataFrame(expenses)
    summary=df.groupby("category")["amount"].sum()
    summary.plot(kind="bar")
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.show()


def delete_expense():
    if len(expenses)==0:
        print("\nNo expense found.")
        return
    print("\n----Your Expense----")
    for expense in expenses:
        print("ID:",expense["id"],"|",expense["category"],"|",expense["description"],"|",expense["amount"])
    while True:
        try:
            choice=int(input("\nEnter expense ID to delete: "))
            break
        except ValueError:
            print("Please enter a valid ID. ")

    found=False

    for expense in expenses:
        if expense["id"]==choice:
            print("\nExpense found:")
            print("Category:",expense["category"])
            print("Description:",expense["description"])
            print("Amount:",expense["amount"])
            confirmation=input("\nAre you sure. you want to delete this expense?(yes/No)").lower()
            if confirmation=="yes":
                expenses.remove(expense)
                save_expenses()
                print("Expense deleted successfully!")
            else:
                print("Delete cancelled.")
            found=True
            break
    if not found:
        print("Invalid expense number.")

def edit_expense():
    if len(expenses)==0:
        print("\nNo expenses found.")
        return
    print("\n----Your Expense----")

    for expense in expenses:
        print("ID:",expense["id"],"|",expense["category"],"|",expense["description"],"|",expense["amount"])
    while True:
        try:
            choice=int(input("\nEnter expense ID to edit: "))
            break
        except ValueError:
            print("Please enter a valid ID. ")
    found=False
    for expense in expenses:
        if expense["id"]==choice:
            print("\nEnter new details")
            while True:
                try:
                    amount=float(input("Enter new amount :"))
                    if amount<=0:
                        print("Amount must be greater than 0. ")
                    else:
                        break
                except ValueError:
                    print("please enter a valid number.")
            print("\nCategories")
            print("1. Food")
            print("2. Travel")
            print("3. Shopping")
            print("4. Bills")
            print("5. Entertainment")
            print("6. Other")

            category_choice=input("Choose category: ")
            if category_choice=="1":
                category="Food"
            elif category_choice=="2":
                category="Travel"
            elif category_choice=="3":
                category="Shopping"
            elif category_choice=="4":
                category="Bills"
            elif category_choice=="5":
                category="Entertainment"
            else:
                category="Other"

            description=input("Enter new description :")
            expense["amount"]=amount
            expense["category"]=category
            expense["description"]=description
            save_expenses()
            print("Expense updated successfully!")
            found=True
            break
    if not found:
        print("Invalid expense ID.")


        
def calculate_total():
    if len(expenses)==0:
        print("\nNo expense found.")
        return
    total=0
    for expense in expenses:
        total=total+expense["amount"]
    print("\nTotal expenses :",total)

def search_by_category():
    if len(expenses)==0:
        print("\nNo expenses found.")
        return
    category=input("Enter category:").lower()
    found=False
    for expense in expenses:
        if expense["category"].lower()==category:
            print("---------------")
            print("Amount:",expense["amount"])
            print("Category:",expense["category"])
            print("Description:",expense["description"])
            print("Date:",expense["date"])
            found=True
    if not found:
        print("No expenses found for this category")

def search_by_date():
    if len(expenses)==0:
        print("\nNo expenses found.")
        return
    search_date=input("Enter date(YYYY-MM-DD):")
    found=False
    for expense in expenses:
        if expense["date"]==search_date:
            print("---------------")
            print("Amount:",expense["amount"])
            print("Category:",expense["category"])
            print("Description:",expense["description"])
            print("Date:",expense["date"])
            found=True
    if not found:
        print("No expenses found for this date")

def monthly_report():
    if len(expenses)==0:
        print("\nNo expenses found.")
        return
    month=input("Enter month(YYYY-MM): ")
    total=0
    count=0
    for expense in expenses:
        if expense["date"].startswith(month):
            total=total+expense["amount"]
            count=count+1
    print("\n------Monthly Report------")
    print("Month:",month)
    print("Number of expenses:", count)
    print("Total Expenses:",total)






expenses=load_expenses()

while True:
    print("\n======Daily Expense Tracker======")
    print("1. Add Expense")
    print("2. View Expense")
    print("3. Total Expenses")
    print("4. Analyze Expenses")
    print("5. Category Summary")
    print("6. Category Chart")
    print("7. Delete Expense")
    print("8. Edit Expense")
    print("9. Search by Category")
    print("10. Search by Date")
    print("11. Monthly Report")
    print("12. Set Monthly Budget")
    print("13. Check Monthly Budget")
    print("14. Exit")


    choice=input("Enter Choice: ")

    if choice=="1":
        add_expense()

    elif choice=="2":
        view_expenses()

    elif choice=="3":
        calculate_total()

    elif choice=="4":
        analyze_expenses()

    elif choice=="5":
        category_summary()

    elif choice=="6":
        category_chart()

    elif choice=="7":
        delete_expense()

    elif choice=="8":
        edit_expense()

    elif choice=="9":
        search_by_category()

    elif choice=="10":
        search_by_date()

    elif choice=="11":
        monthly_report()

    elif choice=="12":
        set_budget()

    elif choice=="13":
        check_budget()

    elif choice=="14":
        print("GoodBye!")
        break

    else:
        print("Invaild choice. Please try again.")

