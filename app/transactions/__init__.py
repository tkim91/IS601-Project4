import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Transactions
from app.transactions.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

transactions = Blueprint('transactions', __name__,
                        template_folder='templates')


@transactions.route('/transactions', methods=['GET'], defaults={"page": 1})
@transactions.route('/transactions/<int:page>', methods=['GET'])
def transactions_browse(page):
    page = page
    per_page = 1000
    pagination = Transactions.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_transactions.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)


@transactions.route('/transactions/upload', methods=['POST', 'GET'])
@login_required
def transactions_upload():
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("csv")

        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        #user = current_user
        list_of_transactions = []
        #calculate the balance for the user
        balance = 0
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                log.info(row['AMOUNT'])
                balance += int(row['AMOUNT'])
                list_of_transactions.append(Transactions(row['AMOUNT'],row['TYPE']))


        current_user.transactions = list_of_transactions
        current_user.balance = balance
        print(current_user.balance)
        log.info(current_user.balance)
        log.info("Uploaded CSV successfully")
        log.info(filename)
        db.session.commit()

        return redirect(url_for('auth.dashboard'))

    try:
        return render_template('templates/upload.html', form=form)
    except TemplateNotFound:
        abort(404)