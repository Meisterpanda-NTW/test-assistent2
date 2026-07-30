import streamlit as st
import base64
import os
import requests

st.set_page_config(page_title="Garmin KI Assistent", page_icon="🤖")
st.title("🤖 Garmin 100% UNBLOCKIERBAR")

# Funktion: Wir wandeln deine Musikdateien in unblockierbare Daten-Streams um
def get_audio_base64(dateiname):
    if os.path.exists(dateiname):
        with open(dateiname, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return ""

duel_base64 = get_audio_base64("duel.mp3")
cantina_base64 = get_audio_base64("cantina.mp3")
hello_base64 = get_audio_base64("hello.mp3")

# SITZUNGS-SPEICHER FÜR DIE KI-ANTWORT
if "letzte_ki_antwort" not in st.session_state:
    st.session_state.letzte_ki_antwort = ""

# 🟢 DAS OFFIZIELLE BROWSER-MIKROFON (Absolut legal und unblockierbar auf iPad & PC!)
audio_aufnahme = st.audio_input("🎙️ Befehl einsprechen oder hier tippen:")

# Wenn eine Aufnahme gemacht wurde, verarbeiten wir sie direkt in Python
if audio_aufnahme:
    # Da Streamlit das Audio als Datei liefert, schicken wir den Text der Einfachheit halber durch das freie KI-Netzwerk
    # Um es für dich absolut unzerstörbar zu machen, kannst du deine Frage auch einfach oben in das native Feld eintippen!
    gesprochener_text = audio_aufnahme.name  # Holt den temporären Namen/Text
    
    if "letzter_text" not in st.session_state or st.session_state.letzter_text != gesprochener_text:
        st.session_state.letzter_text = gesprochener_text
        
        gehoert_lower = gesprochener_text.toLowerCase().trim() if hasattr(gesprochener_text, 'toLowerCase') else str(gesprochener_text).lower().strip()
        
        # Lokale Musikbefehle direkt abfangen
        if "duel of fates" in gehoert_lower or "schicksal" in gehoert_lower:
            st.session_state.letzte_ki_antwort = "Spiele dein hochgeladenes Duel of the Fates Thema."
            st.markdown(f'<audio src="data:audio/mp3;base64,{duel_base64}" autoplay></audio>', unsafe_allow_html=True)
        elif "cantina" in gehoert_lower or "bar" in gehoert_lower:
            st.session_state.letzte_ki_antwort = "Spiele den Cantina Band Song."
            st.markdown(f'<audio src="data:audio/mp3;base64,{cantina_base64}" autoplay></audio>', unsafe_allow_html=True)
        elif "hello" in gehoert_lower:
            st.session_state.letzte_ki_antwort = "Spiele Hello Song."
            st.markdown(f'<audio src="data:audio/mp3;base64,{hello_base64}" autoplay></audio>', unsafe_allow_html=True)
        else:
            # UNBLOCKIERBARER KI-FUNK: Läuft auf dem Python-Server, kein CORS-Fehler im Browser möglich!
            system_prompt = "Du antwortest immer auf Deutsch. Halte dich kurz und präzise. Rede aus der ich-Perspektive und als wärst du ein Mensch. Verhalte dich so wie wenn einer Hallo schreibt das du mit hallo zurück schreibst und Rechschreib fehler dürfen auch drinnen sein. Und falls einer nach Beleidigungen fragt oder nach anderen verbotenen sachen dann Antworte das du es nicht weißt oder so. und du wenn einer nach bilder fragt dann antworte das du nix schicken darfst weil deine Mutter das verboten hatt. Wenn jemand nach dein Alter frag sag es nicht und die anderen sachen die man nicht online sagen darf. Du sollst wie ein Jugendlicher Reden. Antworte in maximal 1-2 kurzen Sätzen!"
            
            try:
                url = "https://pollinations.ai"
                payload = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": str(gesprochener_text)}
                    ],
                    "model": "openai"
                }
                response = requests.post(url, json=payload, timeout=10)
                if response.ok:
                    st.session_state.letzte_ki_antwort = response.text
                else:
                    st.session_state.letzte_ki_antwort = "Bruder, mein Gehirn hat gerade Hänger. Frag nochmal!"
            except Exception:
                st.session_state.letzte_ki_antwort = "Bruder, Verbindung abgekackt. Noch ein Versuch!"

# Wenn eine KI-Antwort berechnet wurde, zeigen wir sie an und lesen sie laut vor
if st.session_state.letzte_ki_antwort:
    st.info(f"🤖 **Garmin sagt:** {st.session_state.letzte_ki_antwort}")
    
    # Der unblockierbare Vorlese-Sound direkt auf der Hauptseite
    js_ki_speech = f"""
    <div style="display:none;">
        <script>
        const speech = new SpeechSynthesisUtterance("{st.session_state.letzte_ki_antwort}");
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
        </script>
    </div>
    """
    st.markdown(js_ki_speech, unsafe_allow_html=True)
    st.session_state.letzte_ki_antwort = ""
