import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.base import MIMEBase
from email import encoders

def autoreply(toaddr):
	"""SEnd reply to contact submission."""

	fromaddr = "XXXX@gmail.com"
	msg = MIMEMultipart()

	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Contact django reply by admin(arbaz)"

	body = "Thanks for contacting us. We will get back to you after processing your submission.   Miss Gayathri S,admin, ONLINE GADGETS SHOPPING Django Project"

	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "XXXX")#"PASSWORD FOR FROMADDR")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
