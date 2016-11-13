import requests
from lxml import etree
import time

from email.mime.text import MIMEText
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename
from email.utils import COMMASPACE, formatdate


def send_mail(send_from, send_to, subject, text, server, pwd, files=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.login(send_from, pwd)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

def len_of_lis(url):
    content = requests.get(url).text
    dom = etree.HTML(content)
    lis = dom.xpath('//ul[@class="r-else clearfix"]/li')
    return len(lis)

def main():
    url = 'https://www.douyu.com/pis'
    while True:
        l = len_of_lis(url)
        if l == 3:
            send_mail(send_from='lty1856@163.com', send_to=['421934806@qq.com'],
                      subject='p online', text='online', server='smtp.163.com',
                      pwd='637695ty')
            break
        time.sleep(600)
