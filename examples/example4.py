def fibonacci(n):
    # Basis-Fälle
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    # Rekursiver Aufruf
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# Test des Codes: Die ersten 10 Fibonacci-Zahlen ausgeben
print("Die ersten 10 Fibonacci-Zahlen:")
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")