def bubble_sort(liste):
    n = len(liste)
    # Durchlaufe alle Listenelemente
    for i in range(n):
        # Letzte i Elemente sind bereits sortiert
        for j in range(0, n - i - 1):
            # Wenn das aktuelle Element größer ist als das nächste, tauschen
            if liste[j] > liste[j + 1]:
                liste[j], liste[j + 1] = liste[j + 1], liste[j]
    return liste

# Test des Codes
unsortiert = [64, 34, 25, 12, 22, 11, 90]
print("Original:", unsortiert)
print("Sortiert:", bubble_sort(unsortiert))