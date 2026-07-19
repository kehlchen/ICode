class Bankkonto:
    def __init__(self, inhaber, startguthaben=0.0):
        self.inhaber = inhaber
        self.kontostand = startguthaben
        self.transaktionen = []

    def einzahlen(self, betrag):
        if betrag > 0:
            self.kontostand += betrag
            self.transaktionen.append(f"+ {betrag} EUR eingezahlt")
            return True
        return False

    def abheben(self, betrag):
        if 0 < betrag <= self.kontostand:
            self.kontostand -= betrag
            self.transaktionen.append(f"- {betrag} EUR abgehoben")
            return True
        print(f"Meldung für {self.inhaber}: Deckung nicht ausreichend!")
        return False

    def kontoauszug(self):
        print(f"=== Kontoauszug für {self.inhaber} ===")
        for t in self.transaktionen:
            print(t)
        print(f"Aktueller Kontostand: {self.kontostand} EUR\n")

# Test des Codes
mein_konto = Bankkonto("Robin", 100.0)
mein_konto.einzahlen(50.0)
mein_konto.abheben(30.0)
mein_konto.abheben(200.0) # Schlägt fehl
mein_konto.kontoauszug()