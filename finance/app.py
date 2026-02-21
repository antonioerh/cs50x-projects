import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import sqlite3
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create database path
os.makedirs(app.instance_path, exist_ok=True)
db_path = os.path.join(app.instance_path, "database.db")

# Configure SQLite3 to access database
db = SQL(f"sqlite:///{db_path}")

# Create database tables
def init_db():
    with sqlite3.connect(db_path) as conn:
        with open("schema.sql") as f:
            conn.executescript(f.read())

# Check if database exists already
if not os.path.exists(db_path):
    init_db()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Store user's id
    user_id = session.get("user_id")

    # Store user's data
    stocks = db.execute("SELECT * FROM stocks WHERE user_id = ?", user_id)
    users = db.execute("SELECT * FROM users WHERE id = ?", user_id)

    total_stocks = 0

    # Loop through each stock price and calculate total
    for stock in stocks:
        total_stocks += stock["total"]

    # Add the value of user's stocks to user's cash
    total = float(total_stocks) + users[0]['cash']

    # Render main page
    return render_template("index.html", stocks=stocks, users=users, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")

    elif request.method == "POST":
        # Store form data
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Store the company name, current price and symbol of the stock
        stock = lookup(symbol)

        # Store data from database of this session
        user_id = session.get("user_id")
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

        # Store user's data
        tmp_date = datetime.datetime.now()
        date = tmp_date.strftime("%Y-%m-%d %H:%M")

        # Ensure user's symbol or shares input is valid
        if not lookup(symbol) or not shares.isdecimal() or int(shares) < 1:
            return apology("Invalid stock symbol or number of shares", 400)

        else:
            # Store the price of the purchase
            stock_price = float(stock["price"]) * int(shares)

            # Ensure user can afford purchase
            if cash[0]["cash"] - stock_price > 0:
                # Update user's cash amount
                updated_cash = cash[0]["cash"] - stock_price
                db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

                # Update stock table
                ownership_check = db.execute(
                    "SELECT symbol FROM stocks WHERE user_id = ? AND symbol = ?", user_id, symbol)
                shares_number = db.execute(
                    "SELECT shares FROM stocks WHERE user_id = ? AND symbol = ?", user_id, symbol)

                # Ensure the user does not have any share of the stock
                if not ownership_check:
                    db.execute("INSERT INTO stocks (user_id, symbol, shares, price, total) VALUES (?, ?, ?, ?, ?)",
                               user_id, symbol, shares, stock["price"], float(stock["price"] * int(shares)))
                    db.execute("INSERT INTO transactions (user_id, transaction_type, symbol, shares, proceeds, date, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               user_id, "Buy", symbol, f"+{shares}", float(stock['price']) * int(shares), date, float(stock["price"]))

                else:
                    # Update database
                    db.execute("UPDATE stocks SET shares = ?, total = ? WHERE user_id = ? AND symbol = ?", int(
                        shares_number[0]["shares"]) + int(shares), float(stock["price"]) * (float(shares_number[0]["shares"]) + int(shares)), user_id, symbol)
                    db.execute("INSERT INTO transactions (user_id, transaction_type, symbol, shares, proceeds, date, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               user_id, "Buy", symbol, f"+{shares}", float(stock['price']) * int(shares), date, float(stock["price"]))

                # Redirect user to home page
                return redirect("/")

            else:
                return apology("User cannot afford the purchase")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Store user's
    user_id = session.get("user_id")

    # Store everything from the transactions table
    logs = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)

    # Render history page
    return render_template("history.html", logs=logs)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Store user's username and session
        user_id = session.get("user_id")
        session["user_id"] = user_id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/change", methods=["GET", "POST"])
def change():
    """Change username"""

    # Store user's data
    user_id = session.get("user_id")

    if request.method == "GET":
        return render_template("change.html")

    elif request.method == "POST":
        # Store form data
        current_username = request.form.get("current-username")
        new_username = request.form.get("new-username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        # Store database data
        users = db.execute("SELECT * FROM users")
        user_current = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        user_password = db.execute("SELECT hash FROM users WHERE id = ?", user_id)

        # Ensure current username field is valid
        if current_username == False or current_username != user_current[0]["username"]:
            return apology("Invalid current username", 400)

        # Ensure new username field is valid
        elif new_username == False or new_username in users or not new_username.isalpha():
            return apology("Invalid new username", 400)

        # Ensure passwords fields are valid
        elif password == False or confirm_password == False or password != confirm_password:
            return apology("Passwords don't match", 400)

        elif not check_password_hash(user_password[0]["hash"], password):
            return apology("Invalid password", 400)

        else:
            # Update database
            db.execute("UPDATE users SET username = ? WHERE id = ?", new_username, user_id)

            # Return home page
            return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Display the registration form
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        # Store user's data on a variable
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        # Ensure none of the fields is left blank
        if username == "" or password == "":
            return apology("Username and password are required", 400)

        # Ensure the passwords match
        elif password != confirm_password:
            return apology("Passwords don't match", 400)

        # Ensure the username hasn't already been taken
        elif len(db.execute("SELECT username FROM users WHERE username = ?", username)) > 0:
            return apology("Username is already taken", 400)

        else:
            # Encrypt user's password
            database_password = generate_password_hash(password)

            # Insert user's data into the database
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, database_password)

            # Log the user in
            temp_id = db.execute(
                "SELECT id FROM users WHERE username = ? AND hash = ?", username, database_password)
            user_id = temp_id[0]["id"]
            session["user_id"] = user_id

            # Redirect user to home page
            return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # Display the quote form
    if request.method == "GET":
        return render_template("quote.html")

    elif request.method == "POST":
        # Store stock symbol typed by the user
        symbol = request.form.get("symbol")

        # Ensure user's input is valid
        if not lookup(symbol):
            return apology("Invalid stock symbol", 400)

        else:
            # Store the company name, current price and symbol of the stock
            stock = lookup(symbol)

            # Redirect to page with information about it
            return render_template("quoted.html", stock=stock)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Store user's id
    user_id = session.get("user_id")

    # Render sell form
    if request.method == "GET":
        symbols = db.execute("SELECT symbol FROM stocks WHERE user_id = ?", user_id)
        return render_template("sell.html", symbols=symbols)

    elif request.method == "POST":
        # Store form data
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Store user's data
        symbols = db.execute("SELECT symbol FROM stocks WHERE user_id = ?", user_id)
        current_shares = db.execute(
            "SELECT shares FROM stocks WHERE user_id = ? AND symbol = ?", user_id, symbol)
        price = db.execute(
                "SELECT price FROM stocks WHERE user_id = ? AND symbol = ?", user_id, symbol)
        total_price = price[0]["price"] * int(shares)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        tmp_date = datetime.datetime.now()
        date = tmp_date.strftime("%Y-%m-%d %H:%M")

        # Ensure user's shares input is valid
        if not shares.isdigit() or int(shares) > current_shares[0]["shares"] or int(shares) < 1:
            return apology("Invalid number of shares", 400)

        else:
            # Update database
            db.execute("UPDATE users SET cash = ? WHERE id = ?",
                       total_price + cash[0]["cash"], user_id)
            db.execute("UPDATE stocks SET shares = ?, total = ? WHERE user_id = ? AND symbol = ?", int(
                current_shares[0]["shares"]) - int(shares), price[0]["price"] * (int(current_shares[0]["shares"]) - int(shares)), user_id, symbol)
            db.execute("INSERT INTO transactions (user_id, transaction_type, symbol, shares, proceeds, date, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       user_id, "Sell", symbol, f"-{shares}", float(price[0]['price']) * int(shares), date, price[0]["price"])

            shares = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND symbol = ?", user_id, symbol)

            if shares[0]["shares"] == 0:
                db.execute("DELETE FROM stocks WHERE user_id = ? AND symbol = ? AND shares = ?", user_id, symbol, 0)

            # Redirect to main page
            return redirect("/")
