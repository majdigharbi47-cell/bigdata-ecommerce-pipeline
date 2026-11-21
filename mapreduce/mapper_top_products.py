#!/usr/bin/env python3
import sys
import csv
reader = csv.reader(sys.stdin)
for row in reader:
	try:
		# Ignorer lignes malformées ou en-tête
		if len(row) < 8 or row[0] == "InvoiceNo":
			continue
		invoice_no = row[0]
		description = row[2]
		quantity = row[3]
		# Ignorer factures annulées (commençant par C)
		if invoice_no.startswith("C"):
			continue
		qty = float(quantity)
		# Ignorer quantités invalides
		if qty <= 0:
			continue
		# Nettoyer le nom du produit (enlever espaces et tabs)
		description = description.strip().replace("\t", " ")
		if description:
			# Émission: Produit [tab] Quantité
			print(f"{description}\t{qty}")
	except (ValueError, IndexError):
		# Ignorer erreurs de parsing
		continue
