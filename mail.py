from email.mime.text import MIMEText
import smtplib

def email_(msg, to_addr, password):    
    from_addr = 'christ_j@yeah.net'
    me = 'hello' + '<' + from_addr + '>'
    title = 'verify your email address\nTo finish setting up our app\'s account, we just need to make sure this email address is yours.\nyou may be asked to enter this security code:\n'
    msg = title + msg
    msg = MIMEText(msg, 'plain', 'utf-8')
    msg['Subject'] = 'welcome register'
    msg['From'] = me
    msg['To'] = to_addr
    smtp_server = 'smtp.yeah.net'
    server = smtplib.SMTP_SSL(smtp_server, 587)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(me, [to_addr], msg.as_string())
    server.quit()
