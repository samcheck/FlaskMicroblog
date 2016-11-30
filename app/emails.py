from flask import render_template
from flask_mail import Message
from app import mail
from config import ADMINS

def send_email(subject, sender, recipients, text_body, html_body):
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def follower_notification(followed, follower):
    send_email("[picoblog] %s is now following you!" % follower.nickname,
               ADMINS, [followed.email],
               render_template("follower_email.txt", user=followed, follower=follower),
               render_template("follower_email.html", user=followed, follower=follower))
