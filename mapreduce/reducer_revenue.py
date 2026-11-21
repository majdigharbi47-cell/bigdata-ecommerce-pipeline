#!/usr/bin/env python3
import sys
current_country = None
total_revenue = 0.0
for line in sys.stdin:
	line = line.strip()
	# Séparation sur la tabulation émise par le mapper
	country, revenue_str = line.split("\t")
	revenue = float(revenue_str)
	if current_country == country:
		total_revenue += revenue
	else:
		# Nouvelle clé détectée : émettre le résultat précédent
		if current_country:
			print(f"{current_country}\t{total_revenue:.2f}")
		current_country = country
		total_revenue = revenue
# Émettre le dernier pays
if current_country:
	print(f"{current_country}\t{total_revenue:.2f}")