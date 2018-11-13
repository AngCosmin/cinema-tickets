import json
import random
import pdfkit

from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from playhouse.shortcuts import model_to_dict

from models import Tickets

app = Flask(__name__)
path_wkthmltopdf = r'D:\Apps\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/order/<int:order_id>')
def show_order(order_id):
    tickets = Tickets.select().where(Tickets.order_id == order_id)
    tickets = [model_to_dict(ticket, recurse=True) for ticket in tickets]
    return render_template('order.html', tickets=tickets)


@app.route('/print/<int:order_id>')
def print_order(order_id):
    print('Test')
    return send_from_directory('orders/', str(order_id) + '.pdf')


@app.route('/buy', methods=['POST'])
def buy():
    if len(request.data) == 0:
        return jsonify({'success': False})

    try:
        data = json.loads(request.data)
    except Exception:
        return jsonify({'success': False})

    order_id = random.randrange(100000000, 999999999)

    for person in data:
        if person['ticket_type'] == 'student' or person['ticket_type'] == 'elev':
            if not person['details']:
                return jsonify({
                    'success': False
                })

        Tickets.insert(
            name=person['name'],
            ticket_type=person['ticket_type'],
            cnp=person['cnp'],
            details=person['details'],
            row=person['row'],
            col=person['column'],
            order_id=order_id,
        ).execute()

    pdfkit.from_url('http://127.0.0.1:5000/order/' + str(order_id), 'orders/' + str(order_id) + '.pdf',
                    configuration=config)

    return jsonify({
        'success': True,
        'order_id': order_id,
    })


if __name__ == '__main__':
    app.run()
