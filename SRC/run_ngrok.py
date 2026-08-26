import os
import sys
from pyngrok import ngrok

def start_tunnel(port=5000, authtoken=None):
    """
    Expose local Flask server running at http://127.0.0.1:port to a public HTTPS URL via ngrok.
    """
    if authtoken:
        print(f"[NGROK] Setting ngrok authtoken...")
        ngrok.set_auth_token(authtoken)
    elif "NGROK_AUTHTOKEN" in os.environ:
        ngrok.set_auth_token(os.environ["NGROK_AUTHTOKEN"])
        
    print(f"[NGROK] Tunneling port {port}...")
    try:
        public_url = ngrok.connect(port)
        print("\n" + "="*60)
        print(f"🚀 AI HEALTH SYNC IS LIVE VIA NGROK TUNNEL!")
        print(f"Public URL: {public_url}")
        print(f"Local URL:  http://127.0.0.1:{port}")
        print("="*60 + "\n")
        return public_url
    except Exception as e:
        print(f"[ERROR] Could not start ngrok tunnel: {e}")
        print("Tip: Sign up at https://ngrok.com/ to get your free authtoken and run:")
        print("  py -3.12 -c \"from pyngrok import ngrok; ngrok.set_auth_token('YOUR_TOKEN')\"")
        return None

if __name__ == "__main__":
    token = sys.argv[1] if len(sys.argv) > 1 else None
    start_tunnel(5000, token)
