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
