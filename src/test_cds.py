import cdsapi

try:
    client = cdsapi.Client()
    print("=" * 50)
    print("✅ CDS API CONNECTED SUCCESSFULLY")
    print("=" * 50)
except Exception as e:
    print("❌ Connection Failed")
    print(e)