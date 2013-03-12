#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys                                     # pour disposer de sys.excepthook
import logging                                 # of course
from logging.handlers import SMTPHandler       # of course
import smtplib                                 # envoi d'email
from email.utils import formatdate             # génère la date d'envoi du mail
from email.mime.text import MIMEText           # construction de email
import traceback                               # permettra de formater l'exception

# Pour les besoins de ce script: permet d'intercepter ces exceptions afin de clarifier
#  les causes d'un éventuel échec de l'envoi du email
from smtplib import SMTPAuthenticationError, SMTPSenderRefused, SMTPRecipientsRefused
from socket import gaierror, error, herror


# Paramètres d'envoi du email. Editez selon vos besoins
# Vous trouverez ces informations dans les paramètres de configuration
#  de votre client mail (outlook, thunderbird, etc..)

Host = None                    # Ex: "smtp.gmail.com"
Port = None                    # Ex: 587
Secure = "ssl"                 # ("ssl"/ None) En cas de doute, laisser "ssl"
From = None                    # Ex: "monemail@google.com"
To = None                      # Ex: "trucmuche@labas.com"
Username = None                # Ex: "monemail@google.com"; None si pas d'authentification
Password = None                # Ex: "mon!super?mot!de&passe"; None si pas d'authentification

# check si les paramètres d'envoi existent
for var in [Host, Port, From, To]:
    if not var:
        print u"\n!!! Noubliez pas d'éditer les paramètres d'envoi du mail, en début de fichier!!!\n"
        sys.exit(1)

# check si 'Port' est un entier
if not isinstance(Port, int):
    try:
        Port = int(Port)
    except ValueError:
        print u"\n 'Port' doit être un entier"
        sys.exit(1)

if Secure == "ssl":
    Secure = ()


# ++++++++++++++++++++++++++++++++++++++++++++++
# On hérite de SMTPHandler pour réécrire 'emit'
# ++++++++++++++++++++++++++++++++++++++++++++++

class SMTPHandler_unicode(SMTPHandler):

    def emit(self, record):
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT # 25
            smtp = smtplib.SMTP(self.mailhost, port, timeout = 30)
            msg = self.format(record)

            # Au moment de la création de l'objet par MIMEText, si msg est de type unicode,
            #  il sera encodé selon _charset, sinon il sera laissé tel quel
            message = MIMEText(msg, _charset = "utf-8")

            # On ajoute les headers nécessaires. S'il sont de type unicode,
            #  ils seront encodés selon _charset
            message.add_header("Subject", self.getSubject(record))
            message.add_header("From", self.fromaddr)
            message.add_header("To", ",".join(self.toaddrs))
            message.add_header("Date", formatdate())

            if self.username:
                if self.secure is not None:
                    smtp.ehlo()
                    smtp.starttls(*self.secure)
                    smtp.ehlo()
                smtp.login(self.username, self.password)

            # Envoi du message proprement encodé
            smtp.sendmail(self.fromaddr, self.toaddrs, message.as_string())

            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise

        # +++++++ Rajouté pour clarifier les motifs d'un éventuel échec de l'envoi du email +++++++++
        except SMTPAuthenticationError:
            print u"\nErreur d'authentification! Vérifiez les paramètres: 'Host', 'Port', 'Secure', 'Username' et 'Password'\n"
            sys.exit(1)
        except (SMTPSenderRefused, SMTPRecipientsRefused):
            print u"\nErreur d'expéditeur ou de destinataire! Vérifiez 'From' et 'To'\n"
            sys.exit(1)
        except (gaierror, error, herror) as e:
            print u"\nErreur de connexion! Vérifiez 'Host' et 'Port'\n"
            sys.exit(1)
        # +++++++++++++++++++++++++      Fin rajouts      ++++++++++++++++++++++++++++++++

        except:
            self.handleError(record)

if __name__ == '__main__':

    # +++++++++++++++++++
    # Création du logger
    # +++++++++++++++++++

    nom_loggeur = "test_nsfw"

    # On crée un logger et on met le niveau à critique:
    #  il ne tiendra compte que des logs de ce niveau
    logger = logging.getLogger(nom_loggeur)
    logger.setLevel(logging.CRITICAL)

    # On crée le handler en lui passant les paramètres
    # nécessaire à l'envoie d'un mail
    mail_handler = SMTPHandler_unicode(
        (Host, Port),
        From,
        [To],
        u"Bonjour Mr Freud, %s a encore repéré des pensées génantes" % nom_loggeur,
        credentials = (Username, Password),
        secure = Secure )

    # On met le handler à "critique".
    # Il enverra donc par mail les messages de ce niveau
    mail_handler.setLevel(logging.CRITICAL)

    # On définit un formatter: date, nom du logger, niveau, message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # on associe le formatter au handler:
    # c'est lui qui formattera les logs de ce handler
    mail_handler.setFormatter(formatter)

    # ... et on associe le handler au logger:
    #  il utilisera ce handler, qui émettra les logs critiques
    logger.addHandler(mail_handler)


    # +++++++++++++++++++++++++++++++++++
    # Customizszsation de sys.excepthook
    # +++++++++++++++++++++++++++++++++++

    # la fonction qui remplacera sys.excepthook
    def en_cas_de_plantage(type_except, value, tb):

        # Mise en forme de l'exception. Retourne la trace
        #  sous forme de str avec numéros de lignes et tout
        trace = "".join(traceback.format_exception(type_except, value, tb))

        print u"J'envoie un mail avec le traceback ..."

        # On loggue l'exception au niveau "critique",
        #  elle sera donc envoyée par email
        logger.critical(u"Erreur inattendue:\n%s", trace)

        print u"Mail envoyé!"

        # ... et on laisse le script se planter...
        sys.__excepthook__(type_except, value, tb)

    # on remplace sys.excepthook, et le tour est joué
    sys.excepthook = en_cas_de_plantage


    # +++++++++++++++++++++++++++++++++++++++++++++++++++
    # L'exception perso dont vous êtes tellement fier(e)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++

    class NotSafeForWorkError(Exception):
        """
        Exception soulevée si une pensée est NSFW
        """
        def __init__(self, msg):
            self.msg = u"Danger! %s est NSFW." % msg

        def __str__(self):
            return self.msg.encode("utf-8")


    # +++++++++++++++++++
    # Le coeur du script
    # +++++++++++++++++++

    # liste des pensées proscrites
    # (échantillon, elle est beaucoup plus longue que ça en réalité)
    NSFW = ["cul", "seins", "sametmax"]

    # boucle de censure qui soulève une exception si une pensée déconne
    for pensee in ["pause", "pipi", "sametmax"]:
        if pensee in NSFW:
            raise NotSafeForWorkError(pensee)
        print u"%s est SFW" % pensee

    #sortie:
    ## pause est SFW
    ## pipi est SFW
    ## Traceback (most recent call last):
    ##   File "censure_setm3.py", line 30, in <module>
    ##     raise NotSafeForWorkError(pensee)
    ## __main__.NotSafeForWorkError: Danger! sametmax est NSFW.



