import json
import random
import pdfkit

from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from peewee import fn
from playhouse.shortcuts import model_to_dict

from models import Tickets

app = Flask(__name__)
path_wkthmltopdf = r'D:\Apps\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stats')
def stats():
    return render_template('stats.html')


@app.route('/get-stats', methods=['GET'])
def get_stats():
    stats = {
        'ticket_type_distribution': {
            'adult': 0,
            'student': 0,
        },
        'location_distribution': [],
        'users_distribution': [],
        'movies_distribution': [],
    }

    # Get ticket type
    tickets = Tickets.select(Tickets.ticket_type, fn.COUNT(Tickets.ticket_type).alias('count')).group_by(Tickets.ticket_type)
    for ticket in tickets:
        stats['ticket_type_distribution'][ticket.ticket_type] = ticket.count

    # Location distribution
    tickets = Tickets.select(Tickets.row, Tickets.col, fn.COUNT(Tickets.id).alias('count')).group_by(Tickets.row, Tickets.col)
    tickets = [{'row': ticket.row, 'col': ticket.col, 'count': ticket.count} for ticket in tickets]
    stats['location_distribution'] = tickets

    # Users distribution
    tickets = Tickets.select(Tickets.name, fn.COUNT(Tickets.id).alias('count')).group_by(Tickets.cnp)
    tickets = [{'name': ticket.name, 'count': ticket.count} for ticket in tickets]
    stats['users_distribution'] = tickets

    # Movies distribution
    tickets = Tickets.select(Tickets.movies_id, fn.COUNT(Tickets.id).alias('count')).group_by(Tickets.movies_id)
    tickets = [{'name': ticket.movies_id.title, 'count': ticket.count} for ticket in tickets]
    stats['movies_distribution'] = tickets

    return jsonify(stats)


@app.route('/order/<int:order_id>')
def show_order(order_id):
    tickets = Tickets.select().where(Tickets.order_id == order_id)
    tickets = [model_to_dict(ticket, recurse=True) for ticket in tickets]
    return render_template('order.html', tickets=tickets)


@app.route('/print/<int:order_id>')
def print_order(order_id):
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
