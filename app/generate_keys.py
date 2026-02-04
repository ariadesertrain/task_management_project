"""
Generate RSA Key Pair for FIPS-Compliant JWT Authentication

This script generates a 2048-bit RSA key pair for use with RS256 JWT tokens.
RS256 (RSA with SHA-256) is FIPS 140-2 approved.

Output:
    - keys/private_key.pem  (Keep this SECRET!)
    - keys/public_key.pem   (Safe to share)

FIPS Compliance Notes:
- Uses 2048-bit RSA keys (FIPS minimum)
- SHA-256 is FIPS-approved (FIPS 180-4)
- RSA is FIPS-approved (FIPS 186-4)
- cryptography library can be FIPS-validated
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from pathlib import Path


def generate_rsa_keys(key_size: int = 2048, keys_dir: str = "keys"):
    """
    Generate RSA key pair for JWT signing.
    
    Args:
        key_size: Size of RSA key in bits (minimum 2048 for FIPS)
        keys_dir: Directory to store key files
    """
    
    print(f"Generating {key_size}-bit RSA key pair...")
    print("This may take a moment...\n")
    
    # Create keys directory if it doesn't exist
    keys_path = Path(keys_dir)
    keys_path.mkdir(exist_ok=True)
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Standard RSA exponent
        key_size=key_size,      # 2048 bits minimum for FIPS
        backend=default_backend()
    )
    
    # Serialize private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,  # PKCS#8 format
        encryption_algorithm=serialization.NoEncryption()  # No password protection
    )
    
    # Generate public key from private key
    public_key = private_key.public_key()
    
    # Serialize public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Write private key to file
    private_key_path = keys_path / "private_key.pem"
    private_key_path.write_bytes(private_pem)
    print(f"✅ Private key saved to: {private_key_path}")
    print("   ⚠️  KEEP THIS SECRET! Never commit to version control!")
    
    # Write public key to file
    public_key_path = keys_path / "public_key.pem"
    public_key_path.write_bytes(public_pem)
    print(f"✅ Public key saved to: {public_key_path}")
    print("   ℹ️  Safe to share with services that verify tokens\n")
    
   
    print("\n" + "="*60)
    print("RSA Key Pair Generated Successfully!")
    print("="*60)
    print("\nFIPS Compliance:")
    print(f"  • Algorithm: RSA-{key_size}")
    print("  • Hash: SHA-256")
    print("  • Standard: FIPS 186-4 (RSA)")
    print("  • Standard: FIPS 180-4 (SHA-256)")
    print("\nSecurity Reminders:")
    print("  • Add 'keys/' to .gitignore")
    print("  • Never commit private_key.pem to version control")
    print("  • Back up private key securely")
    print("  • In production, use HSM or key management service")
    print("\nNext Steps:")
    print("  1. Add 'keys/' to your .gitignore file")
    print("  2. Update your config.py to use RS256")
    print("  3. Install PyJWT: pip install pyjwt cryptography")
    print("  4. Test your authentication endpoints")


if __name__ == "__main__":
    generate_rsa_keys()