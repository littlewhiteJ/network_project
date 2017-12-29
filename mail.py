from email.mime.text import MIMEText
import smtplib

def email_(msg, to_addr, password):    
    from_addr = 'christ_j@yeah.net'
    me = 'hello' + '<' + from_addr + '>'
    title = 'welcome register in our record app\nif it is yourself who did this\njust delete it\nanaway we create a code for you\nit is '
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
