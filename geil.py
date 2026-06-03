import streamlit as st
import base64
import os

st.set_page_config(page_title="Garmin Assistent", page_icon="🤖")
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

# Das HTML-System für den Browser
html_reine_web_app = """
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
    status.innerText = "Sprachsteuerung blockiert. Bitte Safari (iPad) oder Chrome (PC) nutzen!";
} else {
    const rec = new Recognition();
    rec.lang = 'de-DE';
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    let siriStimme = new SpeechSynthesisUtterance("");
    window.speechSynthesis.speak(siriStimme);

    const audioPlayer = new Audio();

    function machPiep() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => { osc.stop(); }, 200);
    }

    function spieleStarWars() {
        audioPlayer.pause(); 
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const melodie = [
            {f: 440.00, d: 0.5}, {f: 440.00, d: 0.5}, {f: 440.00, d: 0.5},
            {f: 349.23, d: 0.35}, {f: 523.25, d: 0.15}, {f: 440.00, d: 0.5},
            {f: 349.23, d: 0.35}, {f: 523.25, d: 0.15}, {f: 440.00, d: 0.6}
        ];
        let startZeit = ctx.currentTime;
        melodie.forEach((note) => {
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
        });
    }

    function spieleEchtesDuelOfFates() {
        window.speechSynthesis.cancel();
        const base64Data = "PLATZHALTER_DUEL_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        }
    }

    function spieleCantinaSong() {
        window.speechSynthesis.cancel();
        const base64Data = "PLATZHALTER_CANTINA_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        }
    }

    function spieleHello() {
        window.speechSynthesis.cancel();
        const base64Data = "PLATZHALTER_Hello_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        }
    }

    function sprich(text) {
        window.speechSynthesis.cancel(); 
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
    }

    function zeigeAntwort(text, bgFarbe, textFarbe) {
        antwortBox.innerText = text;
        antwortBox.style.backgroundColor = bgFarbe;
        antwortBox.style.color = textFarbe;
        antwortBox.style.display = "block";
    }

    btn.addEventListener('click', () => {
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(""));
        try { rec.start(); } catch(e) {}
        status.innerText = "🔊 Ich höre zu... Sprich jetzt deinen Befehl!";
        btn.style.backgroundColor = "#2baf2b"; 
        antwortBox.style.display = "none";
    });
    
    rec.onresult = async (e) => {
        const gehoert = e.results.transcript;
        const gehoertLower = gehoert.toLowerCase().trim();
        status.innerText = "Gehört: '" + gehoert + "'";
        
        let antwortText = "";
        let boxFarbe = "#e2e2e2";
        let textFarbe = "#333";
        let istMusik = false;

        if (gehoertLower.includes("okay garmin") || gehoertLower.includes("ok garmin") || gehoertLower.includes("okay gar")) {
            machPiep(); 
            
            const befehlRein = gehoertLower.replace(/okay garmin|ok garmin|okay gar/g, "").trim();
            
            // Deine komplette originale Befehlsliste
            if (gehoertLower.includes("hallo")) {
                antwortText = "Hallo wie kann ich dir helfen";
                boxFarbe = "#d4edda";
            } else if (gehoertLower.includes("fick dich")) {
                antwortText = "dich auch";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("lukas")) {
                antwortText = "nein nicht lukas";
                boxFarbe = "#f8d7da";
            } else if (gehoertLower.includes("kilyan")) {
                antwortText = "dummer sack";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("fick deine mutter")) {
                antwortText = "deine auch";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("video speichern")) {
                antwortText = "sieg heil";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("f*** deine mutter")) {
                antwortText = "deine auch";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("traubenzucker")) {
                antwortText = "schnupf mehr";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("sieg heil")) {
                antwortText = "heil hitler";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("schule")) { 
                antwortText = "Hölle gefunden 48°27'22.2 Nord 12°21'35.9 Ost";
                boxFarbe = "#f8d7da";
            } else if (gehoertLower.includes("star wars") || gehoertLower.includes("spiel musik") || gehoertLower.includes("imperium")) { 
                antwortText = "Möge die Macht mit dir sein.";
                boxFarbe = "#d1ecf1";
                spieleStarWars();
            } else if (gehoertLower.includes("duel of fates") || gehoertLower.includes("schicksal") || gehoertLower.includes("kampf")) { 
                antwortText = "Spiele dein hochgeladenes Duel of the Fates Thema.";
                boxFarbe = "#f8d7da";
                istMusik = true;
                spieleEchtesDuelOfFates(); 
            } else if (gehoertLower.includes("cantina") || gehoertLower.includes("song") || gehoertLower.includes("bar")) { 
                antwortText = "Spiele den Cantina Band Song.";
                boxFarbe = "#fff3cd";
                istMusik = true;
                spieleCantinaSong(); 
            } else if (gehoertLower.includes("hello")) { 
                antwortText = "Spiele Hello Song.";
                boxFarbe = "#fff3cd";
                istMusik = true;
                spieleHello(); 
            } else if (gehoertLower.includes("beenden") || gehoertLower.includes("stopp")) {
                antwortText = "Musik gestoppt.";
                boxFarbe = "#d1ecf1";
                audioPlayer.pause(); 
                rec.stop();
            } else if (befehlRein.length > 0) {
                status.innerText = "🤖 Garmin überlegt...";
                try {
                    const response = await fetch("https://pollinations.ai" + encodeURIComponent("Du bist Garmin, ein cooler, lustiger Sprachassistent. Antworte auf Deutsch und fasse dich extrem kurz in maximal 1 kurzen Satz! Frage: " + befehlRein));
                    antwortText = await response.text();
                    boxFarbe = "#d1ecf1"; 
                    textFarbe = "#0c5460";
                } catch (err) {
                    antwortText = "Das ist eine interessante Frage! Leider kann ich mein Gehirn gerade nicht erreichen.";
                    boxFarbe = "#fff3cd";
                }
            }

            if (antwortText) {
                zeigeAntwort(antwortText, boxFarbe, textFarbe);
                if (!istMusik) {
                    setTimeout(() => { sprich(antwortText); }, 250);
                }
            }
        } else {
            status.innerText = "Ignoriert (Kein 'Okay Garmin'): '" + gehoert + "'";
        }
        btn.style.backgroundColor = "#ff4b4b";
    };
    
    rec.onerror = () => { btn.style.backgroundColor = "#ff4b4b"; status.innerText = "Bereit fürs iPad. Klicke zum Sprechen."; };
    rec.onend = () => { btn.style.backgroundColor = "#ff4b4b"; };
}
</script>
"""

# Platzhalter austauschen
html_bereit = html_reine_web_app.replace("PLATZHALTER_DUEL_MUSIC", duel_base64).replace("PLATZHALTER_CANTINA_MUSIC", cantina_base64).replace("PLATZHALTER_Hello_MUSIC", hello_base64)
st.components.v1.html(html_bereit, height=270)
