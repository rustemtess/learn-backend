#!/usr/bin/env python3
"""
Simple script to generate a secure secret key for your application
"""
import secrets

def generate_secret_key(length=32):
    """Generate a secure random secret key"""
    return secrets.token_hex(length)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated Secret Key:")
    print(secret_key)
    print("\nAdd this to your .env file:")
    print(f"SECRET_KEY={secret_key}")
    print("\nOr set it as environment variable in Vercel")
