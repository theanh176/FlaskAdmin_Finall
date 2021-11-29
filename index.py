import flask_login
from flask import render_template, request, session, jsonify, redirect
from hospital import app, admin_Login
from hospital.models import Account, AccountAssistant, AccountPatient, Books, Medicine, ReceiptDetails, Receipt, ClinicalRecords
from flask_login import login_user, current_user, login_required
from datetime import datetime
import hashlib
from admin import *
import utils


@app.route("/")
def home():
    return render_template("home.html")


@admin_Login.user_loader
def user_load(user_id):
    if AccountPatient.query.get(user_id):
        return AccountPatient.query.get(user_id)
    return AccountAssistant.query.get(user_id)


@app.route("/login", methods=['post'])
def login_exe():
    username = request.form.get("username")
    password = request.form.get("password")

    # password = str(hashlib.md5(password.encode("utf-8")).digest())

    user = Account.query.filter(AccountAssistant.username == username,
                                AccountAssistant.password == password).first()
    if user:
        login_user(user)

    return redirect("/admin")


    err_msg = ""
@app.route("/user-login", methods=['get', 'post'])
def user_login_exe():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        #password = str(hashlib.md5(password.encode("utf-8")).digest())

        user = Account.query.filter(AccountPatient.username == username,
                                    AccountPatient.password == password).first()

        if user:
            login_user(user)
            return redirect(request.args.get("next", "/"))
        else:
            err_msg = "Incorrect username or password!"

    return render_template("/login_user.html", err_msg=err_msg)

@app.route("/")

@app.route("/user-logout")
def user_logout_exe():
    logout_user()

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)