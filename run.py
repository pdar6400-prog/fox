
import asyncio
try:
    import m4
    if __name__ == "__main__":
        try:
            asyncio.run(m4.main())
        except KeyboardInterrupt:
            print("\n[!] Stopped.")
except ImportError:
    print("[!] Error: m4.so file not found.")
