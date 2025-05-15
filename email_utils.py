import pythoncom
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import re
from docx import Document
from datetime import datetime
from docx2pdf import convert
import os
import smtplib
from email.message import EmailMessage
import os
import streamlit as st



def envoyer_email_resultat(destinataire, nom_patient, rapport_pdf_bytes):
    # Configuration de l'email
    message = EmailMessage()
    message["Subject"] = "Résultats de votre test médical"
    message["From"] = "votre-adresse@mail.com"
    message["To"] = destinataire

    corps = f"""
    Bonjour {nom_patient},

    Veuillez trouver ci-joint le rapport de votre test médical effectué récemment.
    
    Ce rapport contient les détails de l’analyse de votre radio pulmonaire. 
    Nous vous recommandons de consulter votre médecin traitant pour toute interprétation complémentaire.

    Merci pour votre confiance.

    Cordialement,
    L’équipe médicale
    """

    message.set_content(corps)

    # Joindre le PDF
    message.add_attachment(rapport_pdf_bytes, maintype="application", subtype="pdf", filename="Rapport_Medical.pdf")

    # Envoi via SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(st.secrets["email"]["user"], st.secrets["email"]["password"])
        smtp.send_message(message)

def is_valid_email(email):
    # Regular expression to validate email
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None


def generer_rapport_docx(nom, age, identifiant, resultat, probabilities,
                         date_exam=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         fichier_modele="model.docx"):

    fichier_sortie_docx = "rapport_du_test.docx"
    fichier_sortie_pdf = "rapport_du_test.pdf"

    doc = Document(fichier_modele)

    remplacements = {
        "[Nom à insérer]": nom,
        "[Âge à insérer]": str(age),
        "[identifiant]": str(identifiant),
        "[Date]": date_exam,
        "[COVID-19 / Pneumonia / Normal]": resultat
    }

    for para in doc.paragraphs:
        for key, val in remplacements.items():
            if key in para.text:
                para.text = para.text.replace(key, val)

        if "COVID-19 :" in para.text:
            para.text = f"COVID-19 : {probabilities[0]*100:.2f}%"
        elif "Pneumonie :" in para.text:
            para.text = f"Pneumonie : {probabilities[2]*100:.2f}%"
        elif "Normal :" in para.text:
            para.text = f"Normal : {probabilities[1]*100:.2f}%"

        if "[Texte ]" in para.text:
            if resultat == "COVID-19":
                para.text = "\tL'analyse suggère des signes de COVID-19. Une confirmation PCR est recommandée."
            elif resultat == "Pneumonie":
                para.text = "\tL'image montre des signes compatibles avec une pneumonie. Une consultation médicale est recommandée."
            else:
                para.text = "Aucun signe anormal détecté. Si des symptômes persistent, consultez un médecin."

    doc.save(fichier_sortie_docx)

    # 🔑 Initialisation COM obligatoire pour éviter l’erreur
    pythoncom.CoInitialize()
    convert(fichier_sortie_docx, fichier_sortie_pdf)
    pythoncom.CoUninitialize()

    # Lire le PDF en binaire
    with open(fichier_sortie_pdf, "rb") as f:
        pdf_bytes = f.read()

    os.remove(fichier_sortie_docx)
    os.remove(fichier_sortie_pdf)

    return pdf_bytes
