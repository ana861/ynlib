def SendEmail(recipients, sender, subject, body, attachments = None):

	# Import smtplib for the actual sending function
	import smtplib

	# Import the email modules we'll need
	from email.mime.text import MIMEText

	msg = MIMEText(body)

	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = ','.join(recipients)

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP('localhost')
	s.sendmail(sender, recipients, msg.as_string())
	s.quit()




class Email(object):
	u"""\
	Send email.
	recipients = ('post@example.com', 'another@example.com')
	"""

	def __init__(self):
		self.recipients = []
		self.CC = []
		self.BCC = []
		self.sender = ''
		self.sendername = ''
		self.subject = ''
		self.body = ''
		self.attachments = []

	def send(self):
		
		# Import smtplib for the actual sending function
		import smtplib, os
		from email.MIMEMultipart import MIMEMultipart
		from email.MIMEBase import MIMEBase
		from email.MIMEText import MIMEText
		from email.Utils import COMMASPACE, formatdate
		from email import Encoders

		# Import the email modules we'll need
		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText
		
		msg = MIMEMultipart()
		msg['Subject'] = self.subject
		msg['From'] = self.sender
		msg['To'] = ','.join(self.recipients)
		if self.CC:
			msg['Cc'] = ','.join(self.CC)
		msg.attach(MIMEText(self.body))
		
		for f in self.attachments:
			part = MIMEBase('application', "octet-stream")
			part.set_payload(open(f.path, "rb").read())
			Encoders.encode_base64(part)
			if f.filename:
				part.add_header('Content-Disposition', 'attachment; filename="%s"' % f.filename)
			else:
				part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
			msg.attach(part)
		
		s = smtplib.SMTP('localhost')
		
		from sets import Set
		recipients = Set(self.recipients)
		recipients.update(self.CC)
		recipients.update(self.BCC)
		
		s.sendmail(self.sender, list(recipients), msg.as_string())
		s.quit()

	def attachFile(self, path, filename = None):
		self.attachments.append(EmailAttachment(path, filename))

class EmailAttachment(object):
	def __init__(self, path, filename = None):
		self.path = path
		self.filename = filename
	
	
	#%s %s' % (buy.localized('invoice'), os.path.basename(order.invoicePDFpath()))