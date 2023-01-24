
from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import client, search_client, client_name_list
from django.shortcuts import render
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("base.html")


@views.route('/index', methods=['GET'])
def index():
    return render_template("index.html")


@views.route('/vente_client', methods=['GET'])
def vente_client():
    if request.method == 'GET':
        data = request.args.get('id')
        year = request.form.get('year')
        c = client(data, year)
        # c.find_exercice()
        c.etat_vente()
        c.etat_achat()
        c.reglement()
        c.reg_paye()
        c.info_reg()
        return [c.display_etat_vente(), c.display_etat_achat(), c.difference(), c.ret_reg(), c.ret_paye(), c.info_reg(), c.ret_inf()]


@ views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('client')
        sc = search_client(name)

        return render_template('info.html', count=len(sc.search()), result=sc.search())

    else:
        # return render_template("login.html")
        return render_template("login.html", result=client_name_list.name_list(), count=len(client_name_list.name_list()))


@ views.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('fn')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        if len(email) < 4:
            flash('email must be greater than 4 letters.', category='error')
        elif len(firstname) < 2:
            flash('firstname must be greater than 3 caracters.', category='error')
        elif password1 != password:
            flash('password don\'t match.', category='error')
        elif len(password) < 7:
            flash('pasword must be at least 7 caracters.', category='error')
        elif True:
            flash('Account created!', category='success')

    return render_template("sign_up.html")


@views.route('/doughnuts')
def doughnuts():
    return render_template("doughnuta.html")
