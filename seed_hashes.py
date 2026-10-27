#!/usr/bin/env python3
"""
seed_hashes.py - Generates correct Werkzeug password hashes for seed data.
Run this script ONCE to generate hashes, then update seed.sql accordingly.

Usage: python seed_hashes.py
"""

from werkzeug.security import generate_password_hash, check_password_hash

accounts = [
    ("admin@alumni.example.com",   "Admin@1234",   "admin"),
    ("alice.johnson@example.com",  "Alumni@1234",  "alumni"),
    ("bob.smith@example.com",      "Alumni@1234",  "alumni"),
    ("carol.white@example.com",    "Alumni@1234",  "alumni"),
    ("david.lee@example.com",      "Alumni@1234",  "alumni"),
    ("eve.martin@example.com",     "Alumni@1234",  "alumni"),
    ("frank.chen@example.com",     "Alumni@1234",  "alumni"),
    ("grace.patel@example.com",    "Alumni@1234",  "alumni"),
    ("henry.kim@example.com",      "Alumni@1234",  "alumni"),
    ("irene.wang@example.com",     "Alumni@1234",  "alumni"),
    ("james.davis@example.com",    "Alumni@1234",  "alumni"),
    ("kate.brown@example.com",     "Student@1234", "student"),
    ("liam.jones@example.com",     "Student@1234", "student"),
    ("mia.taylor@example.com",     "Student@1234", "student"),
    ("noah.wilson@example.com",    "Student@1234", "student"),
    ("olivia.moore@example.com",   "Student@1234", "student"),
]

print("-- Generated password hashes for seed data")
print("-- Copy these UPDATE statements and run them AFTER seed.sql\n")

for email, password, role in accounts:
    hashed = generate_password_hash(password)
    print(f"UPDATE Users SET password_hash='{hashed}' WHERE email='{email}';")
    # Verify immediately
    assert check_password_hash(hashed, password), f"Hash verification failed for {email}"

print("\n-- All hashes verified successfully.")
