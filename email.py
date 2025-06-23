from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from . import config
  

def send(subject : str, message : str, smtp_config : dict = None):
  if not smtp_config:
    smtp_config = config.load()