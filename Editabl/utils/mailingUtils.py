import smtplib

MAIL_ID = "editablServer@outlook.com"
PASSWORD = "editabl@BE02"
HOST = 'smtp.outlook.com'
PORT = 587


class Mailer:
    def __init__(self) -> None:
        self.messageTemplate = None
        self.fromAddr = MAIL_ID
        self.password = PASSWORD
        self.port = PORT
        self.host = HOST
        self.toAddrList = list()
        self.ccList = list()
        self.messageSubject = str()
        self.messageText = str()
        self.server = None

    def setTemplate(self) -> None:
        self.messageTemplate = "From: %s\r\n" % MAIL_ID \
                               + "To: %s\r\n" % ",".join(self.toAddrList) \
                               + "CC: %s\r\n" % ",".join(self.ccList) \
                               + "Subject: %s\r\n" % self.messageSubject \
                               + "\r\n" + self.messageText

    def __enter__(self):
        self.server = smtplib.SMTP(self.host, self.port)
        self.server.starttls()
        self.mailLogin()
        return self

    def __exit__(self, exc_type, exc_value, exc_trackback) -> None:
        self.server.quit()

    def mailLogin(self) -> None:
        self.server.login(self.fromAddr, self.password)

    def addToAddrList(self, toAddr) -> None:
        if isinstance(toAddr, list):
            toAddr = set(toAddr)
            self.toAddrList += list(toAddr)
        else:
            self.toAddrList.append(toAddr)
            self.toAddrList = list(set(self.toAddrList))

    def addToCCList(self, ccAddr) -> None:
        if isinstance(ccAddr, list):
            self.ccList += list(set(ccAddr))
        else:
            self.ccList.append(ccAddr)
            self.ccList = list(set(self.ccList))

    def setMessageSubject(self, subject) -> None:
        self.messageSubject = subject

    def setMessageText(self, message) -> None:
        self.messageText = message

    def _sendMail(self) -> None:
        self.server.sendmail(self.fromAddr, self.toAddrList, self.messageTemplate)

    def sendMail(self, toAddr, ccAddr='', subject='', message='') -> None:
        self.addToAddrList(toAddr)
        self.addToCCList(ccAddr)
        self.setMessageSubject(subject)
        self.setMessageText(message)
        self.setTemplate()
        self.toAddrList += self.ccList
        self._sendMail()
