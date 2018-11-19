import os.path
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from ..config import setup as config


class Email:
	""" Create and send an email
	"""
	def __init__(self, email_from, subject, content=None):
		self.msg = MIMEMultipart('alternative')
		self.msg['Subject'] = subject
		self.msg['From'] = email_from

		if content is not None:
			self.set_content(content)

	def attach(self, file):
		with open(file, 'rb') as fp:
			if file[-4] == '.jpg' or file[-4] == '.gif' or file[-4] == '.png':
				img = MIMEImage(fp.read())
			else:
				img = MIMEApplication(fp.read())
				img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))

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
			server = smtplib.SMTP(config.SMTP['host'])
			server.sendmail(self.msg['From'], to, self.msg.as_string())
			server.quit()
		except:
			logging.exception("We can't send the email")

	def set_content(self, content):
		self.msg.attach(MIMEText(content, 'plain'))
		self.msg.attach(MIMEText(content, 'html'))