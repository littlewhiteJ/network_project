from email.mime.text import MIMEText
import smtplib

def email_(msg, to_addr, password):
    title = 'your mail is used to sign in our app\'s server <day day up record> \n if it is not you(oh mny lovely boy) did this\n you cannot see this email\n you cannot see this email\n you cannot see this email\n :) \n else your code to sign in successfully is \n'
    msg = title + msg
    msg = MIMEText(msg, 'plain', 'utf-8')
    from_addr = '1500012873@pku.edu.cn'
    smtp_server = 'smtp.pku.edu.cn'
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
