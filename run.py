
import asyncio
import sys
import os

def load_module():
    try:
        # Try loading Android/Termux version first
        import m4
        return m4
    except ImportError:
        try:
            # If not found, try to import from the specific long name
            import m4 as m4_mod
            return m4_mod
        except ImportError:
            return None

async def start():
    m4 = load_module()
    if m4:
        try:
            await m4.main()
        except KeyboardInterrupt:
            print("\n[!] Stopped.")
        except AttributeError:
            # If main() is not directly accessible, try to find it
            print("[!] Error: main() function not found in m4 module.")
    else:
        print("[!] Error: m4 module (m4.so) not found.")
        print("[*] Please ensure m4.so or m4.cpython-313-aarch64-linux-android.so is in the same folder.")

if __name__ == "__main__":
    asyncio.run(start())
