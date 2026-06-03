import streamlit as st
import base64
import os
import urllib.request
import json

st.set_page_config(page_title="Garmin KI Assistent", page_icon="🤖")
st.title("🤖 Garmin KOSTENLOSER KI-Assistent")

# Funktion: Wir wandeln die Musikdateien in unblockierbare Daten-Streams um
def get_audio_base64(dateiname):
    if os.path.exists(dateiname):
        with open(dateiname, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return ""

duel_base64 = get_audio_base64("duel.mp3")
cantina_base64 = get_audio_base64("cantina.mp3")
hello_base64 = get_audio_base64("hello.mp3")

# DIE RETTUNG: Wir holen uns den gesprochenen Befehl absolut sicher direkt aus der Web-Adresse!
query_params = st.query_params
sprach_input = query_params.get("speech", "")

# Falls eine Antwort generiert wurde, merken wir sie uns im Session State
if "ki_antwort" not in st.session_state:
    st.session_state.ki_antwort = ""

if sprach_input:
    befehl = sprach_input.lower().strip()
    
    # Prüfen, ob es einer deiner festen Spezial-Befehle oder Lieder ist:
    ist_spezial = False
    for wort in ["hallo", "fick dich", "lukas", "kilyan", "fick deine mutter", "video speichern", "f*** deine mutter", "traubenzucker", "sieg heil", "schule", "star wars", "spiel musik", "imperium", "duel of fates", "schicksal", "kampf", "cantina", "song", "bar", "hello"]:
        if wort in befehl:
            ist_spezial = True
            break
            
    # Wenn es KEIN fester Befehl ist, fragen wir die Gratis-KI!
    if not ist_spezial and len(befehl) > 0 and "ki_antwort_bereit" not in st.session_state:
        try:
            url = "https://pollinations.ai"
            prompt = f"Du bist Garmin, ein cooler, lustiger Sprachassistent. Antworte auf Deutsch und fasse dich extrem kurz in maximal 1 kurzen Satz! Frage: {sprach_input}"
            
            req = urllib.request.Request(
                url + urllib.parse.quote(prompt), 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req) as response:
                st.session_state.ki_antwort = response.read().decode('utf-8')
                st.session_state.ki_antwort_bereit = True
        except Exception as e:
            st.session_state.ki_antwort = "Ich konnte die Gratis-KI gerade nicht erreichen."
            st.session_state.ki_antwort_bereit = True
# Das HTML-System für den Browser (Sendet Daten unblockierbar über die Web-Adresse)
html_reine_web_app = f"""
<div style="text-align: center; margin-bottom: 20px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 14px 28px; font-size: 18px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 260px; transition: 0.3s; font-family: sans-serif;">
        🎙️ Befehl einsprechen
    </button>
    <p id="status" style="color: #555; font-family: sans-serif; margin-top: 15px; font-weight: bold; font-size: 15px;">Bereit fürs iPad. Klicke zum Sprechen.</p>
    
    <div id="antwort-box" style="margin-top: 20px; padding: 15px; border-radius: 8px; font-family: sans-serif; font-weight: bold; display: none; font-size: 16px;"></div>
</div>

<script>
const btn = document.getElementById('mic-btn');
const status = document.getElementById('status');
const antwortBox = document.getElementById('antwort-box');
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {{
    status.innerText = "Sprachsteuerung blockiert.";
}} else {{
    const rec = new Recognition();
    rec.lang = 'de-DE';

    let siriStimme = new SpeechSynthesisUtterance("");
    window.speechSynthesis.speak(siriStimme);

    const audioPlayer = new Audio();

    function machPiep() {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => {{ osc.stop(); }}, 200);
    }}

    function spieleStarWars() {{
        audioPlayer.pause(); 
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const melodie = [
            {{f: 440.00, d: 0.5}}, {{f: 440.00, d: 0.5}}, {{f: 440.00, d: 0.5}},
            {{f: 349.23, d: 0.35}}, {{f: 523.25, d: 0.15}}, {{f: 440.00, d: 0.5}},
            {{f: 349.23, d: 0.35}}, {{f: 523.25, d: 0.15}}, {{f: 440.00, d: 0.6}}
        ];
        let startZeit = ctx.currentTime;
        melodie.forEach((note) => {{
            const osc = ctx.createOscillator();
            const gainNode = ctx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.value = note.f;
            gainNode.gain.setValueAtTime(0.3, startZeit);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startZeit + note.d);
            osc.connect(gainNode);
            gainNode.connect(ctx.destination);
            osc.start(startZeit);
            osc.stop(startZeit + note.d);
            startZeit += note.d + 0.05;
        }});
    }}

    function spieleEchtesDuelOfFates() {{
        window.speechSynthesis.cancel();
        const base64Data = "{duel_base64}";
        if (base64Data.length > 0) {{
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {{}});
        }}
    }}

    function spieleCantinaSong() {{
        window.speechSynthesis.cancel();
        const base64Data = "{cantina_base64}";
        if (base64Data.length > 0) {{
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {{}});
        }}
    }}

    function spieleHello() {{
        window.speechSynthesis.cancel();
        const base64Data = "{hello_base64}";
        if (base64Data.length > 0) {{
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {{}});
        }}
    }}

    function sprich(text) {{
        window.speechSynthesis.cancel(); 
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
    }}

    btn.addEventListener('click', () => {{
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(""));
        try {{ rec.start(); }} catch(e) {{}}
        status.innerText = "🔊 Ich höre zu... Sprich jetzt deinen Befehl!";
        btn.style.backgroundColor = "#2baf2b"; 
        antwortBox.style.display = "none";
    }});
    
    rec.onresult = (e) => {{
        const gehoert = e.results[0][0].transcript;
        const gehoertLower = gehoert.toLowerCase().trim();
        status.innerText = "Gehört: '" + gehoert + "'";
        
        let antwortText = "";
        let boxFarbe = "#e2e2e2";
        let textFarbe = "#333";

        if (gehoertLower.includes("okay garmin") || gehoertLower.includes("ok garmin") || gehoertLower.includes("okay gar")) {{
            machPiep(); 
            
            // Lokale Befehle direkt prüfen
            if (gehoertLower.includes("hallo")) {{
                antwortText = "Hallo wie kann ich dir helfen";
                boxFarbe = "#d4edda";
            }} else if (gehoertLower.includes("fick dich")) {{
                antwortText = "dich auch";
                boxFarbe = "#fff3cd";
            }} else if (gehoertLower.includes("lukas")) {{
                antwortText = "nein nicht lukas";
                boxFarbe = "#f8d7da";
            }} else if (gehoertLower.includes("kilyan")) {{
                antwortText = "dummer sack";
                boxFarbe = "#fff3cd";
            }} else if (gehoertLower.includes("fick deine mutter")) {{
                antwortText = "deine auch";
                boxFarbe = "#fff3cd";
            }} else if (gehoertLower.includes("video speichern")) {{
                antwortText = "sieg heil";
                boxFarbe = "#fff3cd";
            }} else if (gehoertLower.includes("f*** deine mutter")) {{
                antwortText = "deine auch";
                boxFarbe = "#fff3cd";
            }} else if (gehoertLower.includes("traubenzucker")) {{
                antwortText = "schnupf mehr";
                boxFarbe = "#fff3cd";
            }} else if (gehoertLower.includes("sieg heil")) {{
                antwortText = "heil hitler";
                boxFarbe = "#fff3cd";
            }} else if (gehoertLower.includes("schule")) {{ 
                antwortText = "Hölle gefunden 48°27'22.2 Nord 12°21'35.9 Ost";
                boxFarbe = "#f8d7da";
            }} else if (gehoertLower.includes("star wars") || gehoertLower.includes("spiel musik") || gehoertLower.includes("imperium")) {{ 
                antwortText = "Möge die Macht mit dir sein.";
                boxFarbe = "#d1ecf1";
                spieleStarWars();
            }} else if (gehoertLower.includes("duel of fates") || gehoertLower.includes("schicksal") || gehoertLower.includes("kampf")) {{ 
                antwortText = "Spiele dein hochgeladenes Duel of the Fates Thema.";
                boxFarbe = "#f8d7da";
                spieleEchtesDuelOfFates(); 
            }} else if (gehoertLower.includes("cantina") || gehoertLower.includes("song") || gehoertLower.includes("bar")) {{ 
                antwortText = "Spiele den Cantina Band Song.";
                boxFarbe = "#fff3cd";
                spieleCantinaSong(); 
            }} else if (gehoertLower.includes("hello")) {{ 
                antwortText = "Spiele Hello Song.";
                boxFarbe = "#fff3cd";
                spieleHello(); 
            }} else if (gehoertLower.includes("beenden") || gehoertLower.includes("stopp")) {{
                antwortText = "Musik gestoppt.";
                boxFarbe = "#d1ecf1";
                audioPlayer.pause(); 
                rec.stop();
            }} else {{
                // REINER KI-WEG: Keine Übereinstimmung gefunden -> Text über die URL an Python übergeben!
                const befehlRein = gehoertLower.replace(/okay garmin|ok garmin|okay gar/g, "").trim();
                if (befehlRein.length > 0) {{
                    status.innerText = "🤖 Übermittle an KI...";
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set("speech", befehlRein);
                    window.parent.location.href = url.toString();
                    return;
                }}
            }}
        }}

        if (antwortText) {{
            antwortBox.innerText = antwortText;
            antwortBox.style.backgroundColor = boxFarbe;
            antwortBox.style.color = textFarbe;
            antwortBox.style.display = "block";
            if (!gehoertLower.includes("duel of fates") && !gehoertLower.includes("cantina") && !gehoertLower.includes("hello")) {{
                setTimeout(() => {{ sprich(antwortText); }}, 250);
            }}
        }}
        btn.style.backgroundColor = "#ff4b4b";
    }};
    
    rec.onerror = () => {{ btn.style.backgroundColor = "#ff4b4b"; }};
    rec.onend = () => {{ btn.style.backgroundColor = "#ff4b4b"; }};
}}
</script>
"""

# Wenn eine lokale Antwort da ist oder ein Lied läuft, zeigen wir den Status an
if sprach_input and not st.session_state.ki_antwort:
    st.info(f"Letzter verarbeiteter Befehl: '{{sprach_input}}'")

# Wenn eine KI-Antwort von Python generiert wurde, spielen wir sie ab und LÖSCHEN den URL-Parameter direkt wieder
if st.session_state.ki_antwort:
    st.success(st.session_state.ki_antwort)
    
    # JavaScript löscht den URL-Parameter ?speech=..., damit es beim manuellen Neuladen nicht in Endlosschleife spricht
    js_ki_speech = f"""
    <script>
    // URL säubern ohne die Seite neu zu laden
    const url = new URL(window.parent.location.href);
    url.searchParams.delete("speech");
    window.parent.history.replaceState({{}}, document.title, url.toString());

    window.parent.document.getElementById('antwort-box').innerText = "{st.session_state.ki_antwort}";
    window.parent.document.getElementById('antwort-box').style.backgroundColor = "#d1ecf1";
    window.parent.document.getElementById('antwort-box').style.color = "#0c5460";
    window.parent.document.getElementById('antwort-box').style.display = "block";
    
