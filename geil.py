import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Die komplette Logik läuft ohne Neuladen direkt im Browser ab
html_reine_web_app = """
<div style="text-align: center; margin-bottom: 20px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 250px; transition: 0.3s; font-family: sans-serif;">
        🎙️ Assistent starten
    </button>
    <p id="status" style="color: #555; font-family: sans-serif; margin-top: 15px; font-weight: bold; font-size: 16px;">Bereit. Klicke zum Starten.</p>
    
    <!-- Hier blenden wir die Antworten direkt auf der Seite ein -->
    <div id="antwort-box" style="margin-top: 20px; padding: 15px; border-radius: 8px; font-family: sans-serif; font-weight: bold; display: none;"></div>
</div>

<script>
const btn = document.getElementById('mic-btn');
const status = document.getElementById('status');
const antwortBox = document.getElementById('antwort-box');

const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {
    status.innerText = "Browser blockiert Sprachsteuerung. Bitte Safari (iPad) oder Chrome (PC) nutzen.";
} else {
    const rec = new Recognition();
    rec.lang = 'de-DE';
    rec.interimResults = false;
    
    let warteAufBefehl = false;
    let aktivGeklickt = false;

    // 1. Funktion für den Piepton
    function machPiep() {
        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => osc.stop(), 250);
    }

    // 2. Funktion für die Sprachausgabe (Siri/Google Stimme)
    function sprich(text) {
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
    }

    btn.addEventListener('click', () => {
        aktivGeklickt = true;
        try { rec.start(); } catch(e) {}
        status.innerText = "💤 Warte auf Aktivierung... (Sage 'Okay Garmin')";
        btn.style.backgroundColor = "#ffa500"; 
        antwortBox.style.display = "none";
    });
    
    rec.onresult = (e) => {
        const gehoert = e.results[0][0].transcript.toLowerCase();
        
        // STUFE 1: Wartet auf das Aktivierungswort
        if (!warteAufBefehl) {
            if (gehoert.includes("okay garmin") || gehoert.includes("ok garmin") || gehoert.includes("okay gar")) {
                machPiep(); // Macht NUR den Piepton
                warteAufBefehl = true;
                status.innerText = "👂 Ich höre... Sprich jetzt deinen Befehl!";
                btn.style.backgroundColor = "#2baf2b"; 
                rec.stop(); // Stoppt kurz, damit onend Stufe 2 frisch startet
            } else {
                setTimeout(() => { try { rec.start(); } catch(e) {} }, 200);
            }
        } 
        // STUFE 2: Verarbeitet den Befehl direkt im Browser OHNE NEULADEN
        else {
            status.innerText = "Gehört: '" + gehoert + "'";
            warteAufBefehl = false; 
            
            let antwortText = "";
            let boxFarbe = "#e2e2e2";
            let textFarbe = "#333";

            // Deine Befehle direkt in JavaScript geprüft
            if (gehoert.includes("hallo")) {
                antwortText = "Hallo wie kann ich dir helfen";
                boxFarbe = "#d4edda"; // Grün
                textFarbe = "#155724";
            } else if (gehoert.includes("fick dich")) {
                antwortText = "dich auch";
                boxFarbe = "#fff3cd"; // Gelb/Orange
                textFarbe = "#856404";
            } else if (gehoert.includes("lukas")) {
                antwortText = "nein nicht lukas";
                boxFarbe = "#f8d7da"; // Rot
                textFarbe = "#721c24";
            } else if (gehoert.includes("schule")) { // DEIN NEUER BEFEHL HIER
                antwortText = "Hölle gefunden 48°27'22.2 Nord 12°21'35.9 Ost";
                boxFarbe = "#f8d7da"; // Rot
                textFarbe = "#721c24";
            } else if (gehoert.includes("beenden")) {
                antwortText = "programm wird beendet";
                boxFarbe = "#d1ecf1"; // Blau
                textFarbe = "#0c5460";
                aktivGeklickt = false;
                rec.stop();
                status.innerText = "🛑 Assistent beendet.";
                btn.style.backgroundColor = "#ff4b4b";
            }

            // Antwort anzeigen und laut sprechen
            if (antwortText) {
                antwortBox.innerText = antwortText;
                antwortBox.style.backgroundColor = boxFarbe;
                antwortBox.style.color = textFarbe;
                antwortBox.style.display = "block";
                sprich(antwortText);
            }

            // Nach der Antwort direkt wieder zurück in den Standby (Warten auf Garmin)
            if (gehoert !== "beenden") {
                setTimeout(() => {
                    status.innerText = "💤 Warte auf Aktivierung... (Sage 'Okay Garmin')";
                    btn.style.backgroundColor = "#ffa500";
                    try { rec.start(); } catch(e) {}
                }, 2000);
            }
        }
    };
    
    // Hält das Mikrofon dauerhaft aktiv
    rec.onend = () => {
        if (aktivGeklickt) {
            setTimeout(() => { try { rec.start(); } catch(e) {} }, 200);
        }
    };
    rec.onerror = () => {
        if (aktivGeklickt) {
            setTimeout(() => { try { rec.start(); } catch(e) {} }, 200);
        }
    };
}
</script>
"""

# Zeigt die blitzschnelle Web-Komponente auf deiner Streamlit-Seite an
st.components.v1.html(html_reine_web_app, height=250)
