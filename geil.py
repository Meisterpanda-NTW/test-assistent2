import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# iPad-Version: Piepton reagiert wieder direkt auf das gesprochene Wort
html_ipad_piep_fix = """
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

    // Trickst Safari aus, um die Audio-Ausgabe vorzubereiten
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
        window.speechSynthesis.cancel(); 
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        speech.rate = 1.0;
        window.speechSynthesis.speak(speech);
    }

    btn.addEventListener('click', () => {
        // Schaltet die iPad-Lautsprecher beim Berühren scharf
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(""));
        
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

        // Hier wird geprüft, ob du das Aktivierungswort gesagt hast
        if (gehoert.includes("okay garmin") || gehoert.includes("ok garmin") || gehoert.includes("okay gar")) {
            
            machPiep(); // DER PIEPTON KOMMT JETZT HIER (NUR WENN OKAY GARMIN GESAGT WURDE!)
            
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
                antwortText = "Hölle gefunden";
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
            
            // Wartet kurz den Piepton ab, bevor Siri spricht
            setTimeout(() => { sprich(antwortText); }, 250);
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

st.components.v1.html(html_ipad_piep_fix, height=260)
