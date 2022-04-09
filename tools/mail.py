import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mail:
	def __init__(self, addressFrom = None, password = None, addressTo = None):
		super(Mail, self).__init__()
		self.addressFrom = addressFrom;
		self.password = password;

		if addressTo:
			self.addressTo = addressTo;

	def send(self, name, text, textType = "plain"):
		msg = MIMEMultipart("alternative");
		msg["Subject"] = name;
		msg["From"] = self.addressFrom;
		msg["To"] = self.addressTo;
		msg.attach(MIMEText(text, textType));

		s = smtplib.SMTP_SSL("smtp.gmail.com");
		s.login(self.addressFrom, self.password);
		s.sendmail(self.addressFrom, self.addressTo, msg.as_string());
		s.quit();

	def to(self, addressTo):
		self.addressTo = addressTo;
		return self.send;