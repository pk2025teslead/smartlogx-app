#!/usr/bin/env python
"""
Generate a new Django secret key for production
"""
from django.core.management.utils import get_random_secret_key

print("New Django Secret Key:")
print(get_random_secret_key())
print("\nUse this in your Vercel environment variables!")