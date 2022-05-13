import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.auth import admin_required
from app.db import db
from app.db.models import Transactions
from app.transactions.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

transactions = Blueprint('transactions', __name__,
                         template_folder='templates')


@transactions.route('/transactions', methods=['GET'], defaults={"page": 1})
@transactions.route('/transactions/<int:page>', methods=['GET'])
@login_required
@admin_required
def transactions_browse(page):
    page = page
    per_page = 1000
    pagination = Transactions.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    add_url = 'trans_mgmt.add_transaction'
    delete_url = ('trans_mgmt.delete_transaction', [('trans_id', ':id')])
    edit_url = ('trans_mgmt.edit_transaction', [('trans_id', ':id')])
    try:
        return render_template('browse_trnx.html', data=data, pagination=pagination, add_url=add_url,
                               delete_url=delete_url, edit_url=edit_url, Transactions=Transactions)
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
        # user = current_user
        list_of_transactions = []
        # calculate the balance for the user
        balance = 0.0
        with open(filepath, encoding='utf-8-sig') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                log.info(row['AMOUNT'])
                balance += row['AMOUNT']
                list_of_transactions.append(Transactions(row['AMOUNT'], row['TYPE']))

        current_user.transactions = list_of_transactions
        current_user.balance = balance
        print(current_user.balance)

        db.session.commit()
        log.info(current_user.balance)
        log.info("Uploaded CSV successfully")
        log.info(filename)
        return redirect(url_for('transactions.transactions_browse'))
    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)
