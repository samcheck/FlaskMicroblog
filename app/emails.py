from threading import Thread
from flask import render_template
from flask_mail import Message
from app import app, mail
from config import ADMINS

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    mail_thread = Thread(target=send_async_email, args=[app, msg])
    mail_thread.start()


def follower_notification(followed, follower):
    send_email("[picoblog] %s is now following you!" % follower.nickname,
               ADMINS, [followed.email],
               render_template("follower_email.txt", user=followed, follower=follower),
               render_template("follower_email.html", user=followed, follower=follower))
