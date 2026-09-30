from flask import Flask,render_template,request,redirect
import json
from datetime import date

app=Flask(__name__)

def load_expenses():
    try:
        with open("expenses.json","r")as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open("expenses.json","w")as file:
        json.dump(expenses,file,indent=4)


@app.route("/")
def home():
    expenses=load_expenses()
    total=sum(float(expense["amount"]) for expense in expenses)
    count=len(expenses)
    try:
        with open("budget.json","r")as file:
            data=json.load(file)
        budget=float(data["budget"])
    except FileNotFoundError:
        budget=0
    remaining=budget-total
    category_totals={}
    for expense in expenses:
        category=expense["category"]
        amount=float(expense["amount"])
        if category in category_totals:
            category_totals[category]+=amount
        else:
            category_totals[category]=amount
    return render_template("index.html",total=total,count=count,budget=budget,remaining=remaining,category_totals=category_totals)

@app.route("/add_expense",methods=["GET","POST"])
def add_expense():
    if request.method=="POST":
        try:
            amount=float(request.form["amount"])
            if amount<=0:
                return "Amount must be greater than 0."
        except ValueError:
            return "Please enter a valid amount."
        category=request.form["category"]
        description=request.form["description"].strip()
        if description=="":
            return "Description cannot be empty."
        expenses=load_expenses()
        if len(expenses)==0:
            expense_id=1
        else:
            expense_id=max(expense["id"] for expense in expenses)+1
        expense={
            "id":expense_id,
            "amount":amount,
            "category":category,
            "description":description,
            "date":str(date.today())
        }
        expenses.append(expense)
        save_expenses(expenses)
        return redirect("/expenses")

    return render_template("add_expense.html")

@app.route("/expenses")
def view_expenses():
    expenses=load_expenses()
    selected_month=request.args.get("month")
    search=request.args.get("search","").strip()
    selected_category=request.args.get("category")
    if selected_month:
        expenses=[
            expense for expense in expenses if expense["date"].startswith(selected_month)
        ]
    if search:
        expenses=[ expense for expense in expenses if search.lower() in expense["description"].lower()]
    if selected_category:
        expenses=[expense for expense in expenses if expense["category"]==selected_category]
    total=sum(float(expense["amount"])for expense in expenses)
    return render_template("expenses.html",expenses=expenses,selected_month=selected_month,selected_category=selected_category,total=total)

@app.route("/analytics")
def analytics():
    expenses=load_expenses()
    if len(expenses)==0:
        summary=[]
    else:
        import pandas as pd
        df=pd.DataFrame(expenses)
        category_summary=(df.groupby("category")["amount"].sum().reset_index())
        summary=category_summary.to_dict("records")
    return render_template("analytics.html",summary=summary)

@app.route("/delete-expense/<int:expense_id>")
def delete_expense(expense_id):
    expenses=load_expenses()
    for expense in expenses:
        if expense["id"]==expense_id:
            expenses.remove(expense)
            break
    save_expenses(expenses)
    return redirect("/expenses")

@app.route("/edit-expense/<int:expense_id>",methods=["GET","POST"])
def edit_expense(expense_id):
    expenses=load_expenses()
    for expense in expenses:
        if expense["id"]==expense_id:
            if request.method=="POST":
                try:
                    amount=float(request.form["amount"])
                    if amount<=0:
                        return "Amount must be greater than 0"
                except ValueError:
                    return "Please enter a vaild amount."
                category=request.form["category"]
                description=request.form["description"].strip()
                if description=="":
                    return "Description cannot be empty."
                expense["amount"]=amount
                expense["category"]=category
                expense["description"]=description
                save_expenses(expenses)
                return redirect("/expenses")
            return render_template("edit_expense.html",expense=expense)
        return "Expense not found"

@app.route("/budget",
methods=["GET","POST"])
def budget():
    if request.method=="POST":
        try:
            budget_amount=float(request.form["budget"])
            if budget_amount<=0:
                return "Budget must be greater than 0."
        except ValueError:
            return "Please enter a vaild budget amount."
        with open("budget.json","w")as file:
            json.dump({"budget":budget_amount},file,indent=4)
            return redirect("/budget")
    try:
        with open("budget.json","r")as file:
            data=json.load(file)
        budget_amount=data["budget"]
    except FileNotFoundError:
        budget_amount=0
    return render_template("budget.html",budget=budget_amount) 



if __name__=="__main__":
    app.run(debug=True)