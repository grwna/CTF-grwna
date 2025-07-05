#!/usr/bin/env python3

import pyshark
import base64
import re
import sys
from tqdm import tqdm

def reconstruct_secret_file(pcap_file_path, output_file_path):
    """
    Analyzes a pcap file to reconstruct a file exfiltrated via UDP packets.

    This version includes a fix to handle Base64 strings with missing padding,
    which was causing an "Incorrect padding" error.
    """
    print(f"[+] Analyzing {pcap_file_path}, this may take a moment...")
    
    file_bytes_map = {}
    udp_payload_regex = re.compile(r'pos:(\d+):data:([a-zA-Z0-9+/=]+)')

    try:
        capture = pyshark.FileCapture(
            pcap_file_path,
            display_filter='udp.dstport == 1337'
        )

        for packet in tqdm(capture, desc="Processing packets"):
            try:
                payload_hex = packet.data.data
                payload_bytes = bytes.fromhex(payload_hex)
                payload_str = payload_bytes.decode('utf-8')

                match = udp_payload_regex.search(payload_str)
                if match:
                    position = int(match.group(1))
                    b64_data = match.group(2)
                    
                    missing_padding = len(b64_data) % 4
                    if missing_padding != 0:
                        b64_data += '=' * (4 - missing_padding)
                    decoded_byte = base64.b64decode(b64_data)
                    file_bytes_map[position] = decoded_byte

            except (AttributeError, UnicodeDecodeError):
                continue
            except base64.binascii.Error as e:
                print(f"\n[!] Warning: Skipping malformed base64 data '{b64_data}' at position {position}. Error: {e}")
                continue

        capture.close()

    except FileNotFoundError:
        print(f"[!] ERROR: The file '{pcap_file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")
        sys.exit(1)

    if not file_bytes_map:
        print("[!] No data could be extracted. Please check the pcap file and filter.")
        return

    print("\n[+] Reconstructing the file from extracted bytes...")

    if file_bytes_map:
        max_position = max(file_bytes_map.keys())
        file_size = max_position + 1
        
        reconstructed_data = bytearray(file_size)
        
        for position, byte_value in file_bytes_map.items():
            if position < file_size: # Sanity check
                reconstructed_data[position] = byte_value[0]

        with open(output_file_path, "wb") as f_out:
            f_out.write(reconstructed_data)
            
        print(f"[SUCCESS] File successfully reconstructed and saved to '{output_file_path}'")
    else:
        print("[!] Could not reconstruct file as no data was found.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python solve.py <path_to_pcap_file>")
        pcap_file = 'epilogue.pcap'
        print(f"[*] No file provided, defaulting to '{pcap_file}'")
    else:
        pcap_file = sys.argv[1]
        
    output_file = 'secret_reconstructed.txt'
    reconstruct_secret_file(pcap_file, output_file)

