import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

import twilio
from twilio.rest import Client


# --- Twilio secrets ---
TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_FROM = st.secrets["TWILIO_WHATSAPP_FROM"]

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# Fonction d'envoi WhatsApp
def envoyer_whatsapp(to_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_=TWILIO_WHATSAPP_FROM, body=message, to=f"whatsapp:{to_number}"
    )


# Charger les zones à risque
zones = gpd.read_file("data/zones_inondables.geojson")

# Créer une carte centrée sur Dakar
map = folium.Map(location=[14.6928, -17.4467], zoom_start=12)

# Ajouter les zones inondables
folium.GeoJson(
    zones,
    name="Zones inondables",
    style_function=lambda x: {
        "fillColor": "blue",
        "color": "red",
        "weight": 1,
        "fillOpacity": 0.4,
    },
).add_to(map)

# Affichage Streamlit
st.title("Alertes Inondations - Prototype")
st.write("Carte interactive des zones à risque")
st_data = st_folium(map, width=700, height=500)

# Bouton pour "recevoir alertes"
numero_test = "+221781751168"
message = "🌊 Alerte ! Zones inondables à surveiller ! Consulte la carte ici: https://senflood.streamlit.app"
if st.button("Je veux recevoir des alertes"):
    envoyer_whatsapp(numero_test, message)
    st.success("Merci ! Votre demande a été enregistrée (simulation MVP)")
