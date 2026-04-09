import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.notifications.observer import ObservateurColis
from app.models.colis import Colis

class NotificateurEmail(ObservateurColis):
    def __init__(self):
        self.expediteur = os.getenv("EMAIL_EXPEDITEUR", "")
        self.mot_de_passe = os.getenv("EMAIL_MOT_DE_PASSE", "")
        self.smtp_serveur = os.getenv("SMTP_SERVEUR", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))

    def notifier(self, colis: Colis, ancien_statut: str) -> None:
        if not self.expediteur or not self.mot_de_passe:
            print(f"[EMAIL SIMULÉ] Colis {colis.id} : {ancien_statut} → {colis.statut.value}")
            return
        try:
            self._envoyer_email(colis, ancien_statut)
        except Exception as e:
            print(f"[ERREUR EMAIL] {e}")

    def _envoyer_email(self, colis: Colis, ancien_statut: str) -> None:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Mise à jour de votre colis {colis.id[:8]}"
        message["From"] = self.expediteur
        message["To"] = colis.adresse_expediteur

        corps = f"""
        Bonjour,

        Votre colis a été mis à jour :
        - Identifiant : {colis.id}
        - Description : {colis.description}
        - Ancien statut : {ancien_statut}
        - Nouveau statut : {colis.statut.value}
        - Destination : {colis.adresse_destination}

        Merci de votre confiance.
        """

        message.attach(MIMEText(corps, "plain"))

        with smtplib.SMTP(self.smtp_serveur, self.smtp_port) as serveur:
            serveur.starttls()
            serveur.login(self.expediteur, self.mot_de_passe)
            serveur.sendmail(self.expediteur, colis.adresse_expediteur, message.as_string())
            print(f"[EMAIL ENVOYÉ] Colis {colis.id[:8]} → {colis.statut.value}")