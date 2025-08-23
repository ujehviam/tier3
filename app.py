from flask import Flask, render_template, request, redirect, url_for, session
import services, models

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ✅ Initialize DB at startup (Flask 3.x safe)
models.init_db()

@app.route("/")
def home():
    if "username" in session:
        users = services.get_all_users()
        return render_template("home.html", username=session["username"], users=users)
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success, message = services.register_user(username, password)
        if success:
            return redirect(url_for("login"))
        else:
            return message
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if services.authenticate_user(username, password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "❌ Invalid credentials"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)