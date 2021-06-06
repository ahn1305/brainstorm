
import smtplib

def send_email(user_code,email):
# Python code to illustrate Sending mail from
# your Gmail account

	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)

	# start TLS for security
	s.starttls()

	# Authentication
	s.login("ab7710850@gmail.com", "cr712345")


	SUBJECT = "Otp from Brainstrom"   
	TEXT = f"your brainstrom login otp is {user_code}"



	# message to be sent
	message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)



	# sending the mail
	s.sendmail("ab7710850@gmail.com", f"{email}", message)

	# terminating the session
	s.quit()
