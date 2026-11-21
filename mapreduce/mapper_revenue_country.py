#!/usr/bin/env python3
import csv
import sys

reader = csv.reader(sys.stdin)
for row in reader:
    try:
        # Ignorer les lignes malformées ou l'en-tête.
        if len(row) < 8 or row[0] == "InvoiceNo":
            continue

        invoice_no = row[0]
        quantity = row[3]
        unit_price = row[5]
        country = row[7]

        # Ignorer les factures annulées.
        if invoice_no.startswith("C"):
            continue

        qty = float(quantity)
        price = float(unit_price)

        # Validation des données.
        if qty <= 0 or price <= 0:
            continue

        revenue = qty * price
        # Émission clé-valeur tabulée pour Hadoop Streaming.
        print(f"{country}\t{revenue}")
    except ValueError:
        # Ignorer les erreurs de conversion (données corrompues).
        continue
