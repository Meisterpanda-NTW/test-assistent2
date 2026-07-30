import streamlit as st
import base64
import os
import time
import speech_recognition as sr
import google.genai as genai
from google.genai import types
import google.genai.errors

st.set_page_config(page_title="Garmin KI Assistent", page_icon="🤖")
st.title("🤖 Garmin REINER KI-ASSISTENT")

# HIER DEINE EIGENEN GOOGLE GEMINI SCHLÜSSEL EINTRAGEN:
API_KEYS = [
    "AQ.Ab8RN6Ld69Gz_Fbbj0fC-WCFh3W-zvy8O_9427zfsCicJcGkhA",
    "AQ.Ab8RN6I2k3elYSE-o4jUQKn0GZFJWn6cYDxC6lH5FjVwtxdPUw",  # optional, falls du ein 2. Konto hast
    "AQ.Ab8RN6LnllSVLqIREnCKC9J6MGggedHcqGgo144ArtCl_pK06w",
    "AQ.Ab8RN6JxNkBfYtLIzEZKgIsD7R2wGQzMeUJ1_i3DCTnUv1kJqQ"
]

aktueller_key_index = 0

def get_audio_base64(dateiname):
    if os.path.exists(dateiname):
        with open(dateiname, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return ""

duel_base64 = get_audio_base64("duel.mp3")
cantina_base64 = get_audio_base64("cantina.mp3")
hello_base64 = get_audio_base64("hello.mp3")

if "ki_antwort" not in st.session_state:
    st.session_state.ki_antwort = ""

# HIER BOMBENFEST REPARIERT: Holt den Key ohne gefährliche .startswith() Prüfung
def initialisiere_client():
    global aktueller_key_index
    if not API_KEYS or len(API_KEYS) == 0:
        return None
    key = API_KEYS[aktueller_key_index]
    if "HIER_DEIN" in str(key):
        return None
    # HIER REPARIERT: Nutzt die korrekte Schreibweise für die neue Google-Bibliothek!
    return genai.Client(api_key=key)

client = initialisiere_client()


# Deine originalen Minecraft-Bot Charakter-Anweisungen
# Deine originalen Minecraft-Bot Charakter-Anweisungen
def frage_ki(text):
    global client, aktueller_key_index
    for _ in range(len(API_KEYS)):
        if client is None:
            client = initialisiere_client()
        if client is None:
            return "Bitte trage deine Gemini API-Keys oben im Python-Code ein!"
        try:
            # HIER PERFEKT AUF GEMINI 3.5 FLASH UMGESTELLT!
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "Du antwortest immer auf Deutsch. Halte dich kurz und präzise. "
                        "Rede aus der ich-Perspektive und als wärst du ein Mensch. "
                        "Verhalte dich so wie wenn einer Hallo schreibt das du mit hallo zurück schreibst und Rechschreib fehler dürfen auch drinnen sein. "
                        "Und falls einer nach Beleidigungen fragt oder nach anderen verbotenen sachen dann Antworte das du es nicht weißt oder so. "
                        "und du wenn einer nach bilder fragt dann antworte das du nix schicken darfst weil deine Mutter das verboten hatt. "
                        "Wenn jemand nach dein Alter frag sag es nicht und die anderen sachen die man nicht online sagen darf."
                        "Du sollst wie ein Jugendlicher Reden. Antworte in maximal 1-2 kurzen Sätzen!"
                    )
                ),
            )
            return response.text
        except google.genai.errors.ClientError as e:
            if e.code == 429:
                aktueller_key_index = (aktueller_key_index + 1) % len(API_KEYS)
                client = initialisiere_client()
                time.sleep(1)
                continue
            else:
                return f"API-Fehler: {e}"
        except Exception as e:
            # Falls bei dem einen Key ein Serverfehler (503) kommt, rotieren wir hier auch sofort zum nächsten Schlüssel!
            aktueller_key_index = (aktueller_key_index + 1) % len(API_KEYS)
            client = initialisiere_client()
            time.sleep(1)
            continue
    return "Bruder, alle meine Schlüssel sind für heute voll. Geht gerade gar nicht mehr!"

    st.session_state.ki_antwort = ""
