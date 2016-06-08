from threading import Thread
from flask import current_app, render_template
from flask_mail import Mail, Message

mail = Mail()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message('[{prefix}] {subject}'.format(prefix=app.config['APP_NAME'], subject=subject),
                  sender=app.config['APP_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread
