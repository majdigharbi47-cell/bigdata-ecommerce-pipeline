#!/usr/bin/env python3
import sys
import heapq
current_product = None
current_total = 0
# Tas de taille maximale 10 : (quantité, produit)
top_products = []
def add_to_top(product, qty):
    heapq.heappush(top_products, (qty, product))
    if len(top_products) > 10:
        heapq.heappop(top_products)  # Retire le plus petit
for line in sys.stdin:
    product, qty_str = line.strip().split()
    qty = float(qty_str)
    if current_product == product:
        current_total += qty
    else:
        if current_product:
            add_to_top(current_product, current_total)
        current_product = product
        current_total = qty
# Dernier produit
if current_product:
    add_to_top(current_product, current_total)
# Affichage trié décroissant
for qty, product in sorted(top_products, reverse=True):
    print(f"{product} {qty:.0f}")