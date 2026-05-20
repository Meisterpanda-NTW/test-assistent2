import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Die iPad-optimierte Version mit Audio-Freischaltung per Fingertipp
html_ipad_audio_fix = """
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

if (!Recognition) {
    status.innerText = "Sprachsteuerung blockiert. Bitte Safari auf dem iPad nutzen!";
} else {
    const rec = new Recognition();
    rec.lang = 'de-DE';
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    // DIE RETTUNG FÜR DAS IPAD:
    // Wir erstellen ein leeres Sprach-Objekt direkt beim Laden, um Safari zu tricksen
    let siriStimme = new SpeechSynthesisUtterance("");
    window.speechSynthesis.speak(siriStimme);

    function machPiep() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => osc.stop(), 200);
    }

    function sprich(text) {
        // Auf Apple-Geräten muss die Audio-Synthese direkt reaktiviert werden
        window.speechSynthesis.cancel(); 
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        speech.rate = 1.0;
        window.speechSynthesis.speak(speech);
    }

    // Beim iPad MUSS der Klick die Audio-Berechtigung erzwingen
    btn.addEventListener('click', () => {
        // Ein leerer Sprachbefehl direkt beim Fingertipp schaltet die iPad-Lautsprecher frei
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(""));
        
        machPiep(); 
        try { rec.start(); } catch(e) {}
        status.innerText = "🔊 Ich höre zu... Sprich jetzt deinen Befehl!";
        btn.style.backgroundColor = "#2baf2b"; 
        antwortBox.style.display = "none";
    });
    
    rec.onresult = (e) => {
        const gehoert = e.results[0][0].transcript.toLowerCase().trim();
        status.innerText = "Gehört: '" + gehoert + "'";
        
        let antwortText = "";
        let boxFarbe = "#e2e2e2";
        let textFarbe = "#333";

        if (gehoert.includes("okay garmin") || gehoert.includes("ok garmin") || gehoert.includes("okay gar")) {
            
            if (gehoert.includes("hallo")) {
                antwortText = "Hallo wie kann ich dir helfen";
                boxFarbe = "#d4edda";
                textFarbe = "#155724";
            } else if (gehoert.includes("fick dich")) {
                antwortText = "dich auch";
                boxFarbe = "#fff3cd";
                textFarbe = "#856404";
            } else if (gehoert.includes("lukas")) {
                antwortText = "nein nicht lukas";
                boxFarbe = "#f8d7da";
                textFarbe = "#721c24";
            } else if (gehoert.includes("schule")) {
                antwortText = "Hölle gefunden standort ist 48°27'22.2 Nord 12°21'35.9 Ost";
                boxFarbe = "#f8d7da";
                textFarbe = "#721c24";
            } else if (gehoert.includes("beenden")) {
                antwortText = "programm wird beendet";
                boxFarbe = "#d1ecf1";
                textFarbe = "#0c5460";
                status.innerText = "🛑 Assistent beendet.";
            } else {
                antwortText = "Aktiviert, aber Befehl nicht verstanden.";
                boxFarbe = "#e2e2e2";
            }
            
        } else {
            status.innerText = "Ignoriert (Kein 'Okay Garmin' im Satz): '" + gehoert + "'";
        }

        if (antwortText) {
            antwortBox.innerText = antwortText;
            antwortBox.style.backgroundColor = boxFarbe;
            antwortBox.style.color = textFarbe;
            antwortBox.style.display = "block";
            
            // Wir warten 100 Millisekunden, damit Safari Zeit zum Umschalten hat
            setTimeout(() => { sprich(antwortText); }, 100);
        }
        
        btn.style.backgroundColor = "#ff4b4b";
    };
    
    rec.onerror = () => {
        status.innerText = "Bereit. Klicke zum Sprechen.";
        btn.style.backgroundColor = "#ff4b4b";
    };
    rec.onend = () => {
        btn.style.backgroundColor = "#ff4b4b";
    };
}
</script>
"""

st.components.v1.html(html_ipad_audio_fix, height=260)
