# 🦠 Application de Détection COVID-19 à partir de Radiographies

Bienvenue dans cette application Streamlit basée sur un modèle ResNet18 entraîné pour détecter les cas de **COVID-19**, **Pneumonie** ou **Normaux** à partir d'une **radiographie pulmonaire**.

## 📌 Fonctionnalités

- 📤 Téléversement d'une image médicale (radiographie thoracique).
- 🧠 Analyse de l’image avec un modèle de deep learning.
- 📊 Prédiction avec pourcentages pour chaque classe (COVID, Normal, Pneumonie).
- 📄 Génération d'un rapport PDF personnalisé.
- 📧 Envoi du rapport directement par email.

---

## 🔧 Technologies utilisées

- [Streamlit](https://streamlit.io/) pour l’interface utilisateur
- [PyTorch](https://pytorch.org/) pour le modèle ResNet18
- [docx](https://python-docx.readthedocs.io/) & [docx2pdf](https://pypi.org/project/docx2pdf/) pour générer et convertir le rapport
- [SMTP](https://docs.python.org/3/library/smtplib.html) pour l’envoi des emails
- [dotenv](https://pypi.org/project/python-dotenv/) pour sécuriser les informations sensibles

---

## 🚀 Lancer l’application localement

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-nom/app-covid-detection.git
cd app-covid-detection
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Créer un fichier .env

Créez un fichier .env (à ne pas partager) contenant :
```bash
EMAIL_USER=ton_email@gmail.com
EMAIL_PASS=ton_mot_de_passe_application
```
💡 Utilisez un mot de passe d'application Gmail pour la sécurité.

### 4. Lancer Streamlit

```bash
streamlit run app.py
```

✅ **Exemples d'utilisation**
Remplir le formulaire utilisateur.

Télécharger une image radiographique.

Lancer l’analyse.

Télécharger ou envoyer le rapport.

🛡️ **Sécurité**
Les informations sensibles sont stockées dans le fichier .env (non versionné).

Le mot de passe d’application Gmail est recommandé.

Aucun email ni image n'est stocké côté serveur.

📬 **Contact**
Développé par Ton Aymen Riani
📧 Contact : aymenriani001@gmail.com


 