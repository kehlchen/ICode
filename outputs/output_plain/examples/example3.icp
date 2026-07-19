def text_analyse(text):
    # Satzzeichen manuell entfernen
    satzzeichen = ".,!?;:()\"'"
    bereinigter_text = ""
    for zeichen in text.lower():
        if zeichen not in satzzeichen:
            bereinigter_text += zeichen
        else:
            bereinigter_text += " " # Durch Leerzeichen ersetzen

    # Text in Wörter zerlegen
    woerter = bereinigter_text.split()
    
    # Häufigkeit zählen
    waehler = {}
    for wort in woerter:
        if wort in waehler:
            waehler[wort] += 1
        else:
            waehler[wort] = 1
            
    return waehler

# Test des Codes
beispiel_text = "Python ist super, weil Python einfach zu lernen ist!"
ergebnis = text_analyse(beispiel_text)
print("Wort-Häufigkeiten:")
for wort, anzahl in ergebnis.items():
    print(f"- {wort}: {anzahl}x")