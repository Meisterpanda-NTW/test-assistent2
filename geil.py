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

def initialisiere_client():
    global aktueller_key_index
    if not API_KEYS:
        return None
    # Holt den aktuellen Key sicher aus der Liste heraus
    key = API_KEYS[aktueller_key_index]
    if "HIER_DEIN" in key:
        return None
    return genai.Client(api_key=key)

client = initialisiere_client()


def frage_ki(text):
    global client, aktueller_key_index
    for _ in range(len(API_KEYS)):
        if client is None:
            client = initialisiere_client()
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
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
                return None
        except Exception as e:
            return None
    return "Bruder, alle meine Schlüssel sind für heute voll. Geht gerade gar nicht mehr!"

# NATIVES STREAMLIT-MIKROFON
audio_datei = st.audio_input("🎙️ Drücke auf das Mikrofon und sprich deinen Befehl:")

if audio_datei:
    # Wir holen uns die eindeutige ID der Tondatei, um doppelte Verarbeitung beim Neuladen zu verhindern
    aufnahme_id = audio_datei.id if hasattr(audio_datei, 'id') else audio_datei.name
    
    if "letzte_aufnahme_id" not in st.session_state or st.session_state.letzte_aufnahme_id != aufnahme_id:
        st.session_state.letzte_aufnahme_id = aufnahme_id
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_datei) as source:
            audio_data = recognizer.record(source)
            try:
                gehoert_text = recognizer.recognize_google(audio_data, language="de-DE")
                st.write(f"🎤 **Verstanden:** {gehoert_text}")
                
                gehoert_lower = gehoert_text.lower().strip()
                
                # Musik-Befehle prüfen
                if "duel of fates" in gehoert_lower or "schicksal" in gehoert_lower:
                    st.session_state.ki_antwort = "Spiele dein hochgeladenes Duel of the Fates Thema."
                    st.markdown(f'<audio src="data:audio/mp3;base64,{duel_base64}" autoplay></audio>', unsafe_allow_html=True)
                elif "cantina" in gehoert_lower or "bar" in gehoert_lower:
                    st.session_state.ki_antwort = "Spiele den Cantina Band Song."
                    st.markdown(f'<audio src="data:audio/mp3;base64,{cantina_base64}" autoplay></audio>', unsafe_allow_html=True)
                elif "hello" in gehoert_lower:
                    st.session_state.ki_antwort = "Spiele Hello Song."
                    st.markdown(f'<audio src="data:audio/mp3;base64,{hello_base64}" autoplay></audio>', unsafe_allow_html=True)
                elif "beenden" in gehoert_lower or "stopp" in gehoert_lower:
                    st.session_state.ki_antwort = "Musik gestoppt."
                else:
                    # KI abfragen mit deinen rotierenden Keys
                    st.session_state.ki_antwort = frage_ki(gehoert_text)
                    
            except sr.UnknownValueError:
                st.session_state.ki_antwort = "Bruder, ich habe dich nicht verstanden. Sprich lauter!"
            except sr.RequestError:
                st.session_state.ki_antwort = "Verbindung zum Spracherkennungs-Server abgekackt!"

# Antwort anzeigen und über Siri laut vorlesen lassen
if st.session_state.ki_antwort:
    st.info(f"🤖 **Garmin sagt:** {st.session_state.ki_antwort}")
    
    # Der unblockierbare Vorlese-Sound direkt auf der Hauptseite verankert
    js_speech = f"""
    <div style="display:none;">
        <script>
        const speech = new SpeechSynthesisUtterance("{st.session_state.ki_antwort}");
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
        </script>
    </div>
    """
    st.markdown(js_speech, unsafe_allow_html=True)
    st.session_state.ki_antwort = ""



# Antwort anzeigen und über Siri laut vorlesen lassen
if st.session_state.ki_antwort:
    st.info(f"🤖 **Garmin sagt:** {st.session_state.ki_antwort}")
    
    # Der unblockierbare Vorlese-Sound direkt auf der Hauptseite verankert
    js_speech = f"""
    <div style="display:none;">
        <script>
        const speech = new SpeechSynthesisUtterance("{st.session_state.ki_antwort}");
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
        </script>
    </div>
    """
    st.markdown(js_speech, unsafe_allow_html=True)
    st.session_state.ki_antwort = ""
!"

# Antwort anzeigen und über Siri laut vorlesen lassen
if st.session_state.ki_antwort:
    st.info(f"🤖 **Garmin sagt:** {st.session_state.ki_antwort}")
    
    js_speech = f"""
    <script>
    const speech = new SpeechSynthesisUtterance("{st.session_state.ki_antwort}");
    speech.lang = 'de-DE';
    window.speechSynthesis.speak(speech);
    </script>
    """
    st.components.v1.html(js_speech, height=0, width=0)
    st.session_state.ki_antwort = ""
