import chardet
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import dirbot.settings as settings
def conv(str):
    #return str.decode('gbk')
    code =  chardet.detect(str)['encoding'].lower()
    if code =='utf-8':
        str = str.decode('utf-8')
    else:
        str = str.decode('gbk')
    return str
def sendMail(mailto,subject,body,format='plain'):
        smtphost = settings.MAIL_HOST
        smtpuser = settings.MAIL_USER
        smtppass = settings.MAIL_PASS
        smtpfrom = settings.MAIL_FROM
        if isinstance(body,unicode):
            body = str(body)
        me= ("%s<"+smtpfrom+">") % (Header(smtpfrom,'utf-8'),)
        msg = MIMEText(body,format,'utf-8')
        if not isinstance(subject,unicode):
            subject = unicode(subject)
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = mailto
        msg["Accept-Language"]="zh-CN"
        msg["Accept-Charset"]="ISO-8859-1,utf-8"
        s = smtplib.SMTP()
        s.connect(smtphost)
        s.login(smtpuser,smtppass)
        s.sendmail(me, mailto, msg.as_string())
        s.close()
