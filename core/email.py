import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class Email:
	""" Create and send an email
	"""
	def __init__(self, email_from, subject, content):
		self.msg = MIMEMultipart('alternative')
		self.msg['Subject'] = subject
		self.msg['From'] = email_from

		self.msg.attach(MIMEText(content, 'plain'))
		self.msg.attach(MIMEText(content, 'html'))

	def attach(self, file):
		with open(file, 'rb') as fp:
			img = MIMEImage(fp.read())

		self.msg.attach(img)

	def send(self, to):
		if type(to) == str:
			if ";" in to:
				to = to.split(";")
			elif "," in to:
				to = to.split(",")
			else:
				to = [to]

		self.msg['To'] = ", ".join(to)

		try:
			server = smtplib.SMTP('localhost')
			server.sendmail(self.msg['From'], to, self.msg.as_string())
			server.quit()
		except:
			logging.exception("We can't send the email")