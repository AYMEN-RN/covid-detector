import streamlit as st
import email_utils as eu
import torchvision.transforms as transforms
import time
import torch
from PIL import Image
from torchvision.models import resnet18, ResNet18_Weights
import torch.nn as nn

if "acce" not in st.session_state:
    st.session_state.acce = False

# Affichage du logo de l'application
st.logo("image/LOGO.png", size="large")

# Création de deux colonnes pour l'interface utilisateur
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("image/LOGO.png", width=250)
    st.write("Bienvenue dans l'application de détection de COVID !")

with col2:
    with st.form("Contact form"):
        st.write("**Entrez vos informations :**")
        Name = st.text_input("**Nom complet :**")
        mail = st.text_input("**Votre email :** (ex: abc****@gmail.com)")
        age = st.number_input("**Votre âge :**", min_value=1, max_value=120, step=1)
        submit_button = st.form_submit_button("Confirmer")
        if submit_button:
            if eu.is_valid_email(mail) and Name and age:
                st.success(f"Merci {Name} ! Vos informations ont été soumises avec succès.")
                st.session_state.acce = True
            else:
                st.error("Veuillez fournir une adresse email valide, un nom et un âge.")


# Fonction pour charger le modèle de détection
@st.cache_resource
def load_model():
    model = resnet18(weights=ResNet18_Weights.DEFAULT)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 3)  # 3 classes : COVID-19, Normal, Pneumonie
    model.load_state_dict(torch.load("model/covid_model.pt", map_location=torch.device("cpu")))
    model.eval()
    return model

# Fonction pour prétraiter l'image avant de la passer au modèle
def preprocess_image(img):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    return transform(img).unsqueeze(0)  # Ajouter une dimension pour le batch (taille = 1)

st.image("image/image.png",use_container_width = True)
# Liste des classes prédictibles par le modèle
classes = ["COVID-19", "Normal", "Pneumonie"]

# Section pour télécharger et analyser une image
st.header("Téléchargez votre image")
uploaded_file = st.file_uploader("Téléchargez une radiographie", type=["png", "jpg", "jpeg"])

if st.button("Analyser") and st.session_state.acce and uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    input_tensor = preprocess_image(image)

    with st.spinner("Analyse de l'image..."):
        time.sleep(2)
        with torch.no_grad():
            model = load_model()
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)[0]
            predicted_class = torch.argmax(probabilities).item()

    # Enregistrer dans session_state
    st.session_state["probabilities"] = probabilities
    st.session_state["predicted_class"] = predicted_class
    st.session_state["rapport"] = eu.generer_rapport_docx(Name, age, 1234, classes[predicted_class], probabilities)

if "probabilities" in st.session_state:
    probabilities = st.session_state["probabilities"]
    predicted_class = st.session_state["predicted_class"]

    st.subheader(f":orange[_Le modèle prédit :_] {classes[predicted_class]}")
    st.write("la probabilité en pourcentage : ", int(probabilities[predicted_class]*100), " %")
    st.progress(int(probabilities[predicted_class].item() * 100))

    col3 , col4 = st.columns(2, gap="small", vertical_alignment="center")
    with col3 : 
        st.download_button(
            label="**Télécharger le rapport PDF**",
            data=st.session_state["rapport"],
            file_name="rapport_du_test.pdf",
            mime="application/pdf"
        )
    with col4 :
        if st.button("**Envoyer le rapport par email**"):
            try:
                eu.envoyer_email_resultat(mail, Name, st.session_state["rapport"])
                st.success("Le rapport a été envoyé avec succès à votre adresse email.")
            except Exception as e:
                st.error(f"Une erreur s'est produite lors de l'envoi de l'email : {type(e).__name__} - {str(e)}")

