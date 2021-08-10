from requests import get
import smtplib
from xsmtplib.xsmtplib import SMTP
from email.mime.multipart import MIMEMultipart
import json
from email.mime.text import MIMEText

url_file = 'https://docs.google.com/spreadsheets/d/1ItmvKY7Ihc95pt91TucsqgysoCqwqPehZzooG8LyiJU/edit#gid=0'


def sendGmail(fromaddr, toaddr, password,
              email_body, dir_ip):
    # Build the email
    # msg = MIMEText(email_body)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    # msg['Subject'] = email_subject + file_name
    print(' Subject: ', "[IP Camilo] se ha actualizado la ip - " + dir_ip)
    msg['Subject'] = "[IP Camilo] se ha actualizado la ip - " + dir_ip

    email_body = 'nueva ip: ' + dir_ip + '\n\n' + email_body

    try:
        # attach the body with the msg instance
        msg.attach(MIMEText(email_body, 'plain'))

        # open the file to be sent
        # attachment = open(path_file + file_name, "rb")

        # instance of MIMEBase and named as p
        # p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        # p.set_payload((attachment).read())

        # encode into base64
        # encoders.encode_base64(p)

        # p.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

        # attach the instance 'p' to instance 'msg'
        # msg.attach(p)

        # creates SMTP session
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
        except Exception as e:
            print('\n Maldita sea!, en esta red hay un puto proxy. \n >> Probando de otra forma XD...')
            s = SMTP(host='smtp.gmail.com', port=587,
                     proxy_host='bbvaproxy.co.igrupobbva',
                     proxy_port=7209, timeout=4)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(fromaddr, password)

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, toaddr, text)

        # terminating the session
        s.quit()
        print(" from: %s" % fromaddr)
        print(" to: %s" % toaddr)

    except Exception as e:
        print("\n ERROR! >> Something went wrong when sending the email %s" % fromaddr)
        print(e)


def get_ip():
    ip = {'ip': str(get('https://api.ipify.org').text)}
    return ip


def main():
    fromaddr = "aguilarcamiloa@gmail.com"
    toaddr = "dianaald446@gmail.com"

    with open('./key/gkey.json', "r") as f:
        p = f.read()
    key_mail = json.loads(p)['gmail_key']

    email_body = 'Correo enviado automáticamente...'

    # verifica iṕ
    ip = get_ip()

    # ip anterior
    with open('./data/ip.json', "r") as f:
        p = f.read()
    ip_ant = json.loads(p)['ip']

    # si hubo cambio envia correo
    if ip['ip'] != ip_ant:
        print("Hubo cambio de ip! " + ip['ip'])
        sendGmail(fromaddr, toaddr, key_mail, email_body,
                  dir_ip=ip['ip'])

        # actualiza archivo con la ip
        with open('./data/ip.json', 'w') as f:
            json.dump(ip, f)
    else:
        print('La ip no ha cambiado')

    print('\n Done!')


if __name__ == '__main__':
    main()
