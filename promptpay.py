def crc16_ccitt(data: str) -> str:
    data_bytes = data.encode('utf-8')
    crc = 0xFFFF
    for byte in data_bytes:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = (crc << 1)
            crc &= 0xFFFF
    return f"{crc:04X}"

def generate_payload(target: str, amount: float = None) -> str:
    # Clean target
    target = target.replace("-", "").replace(" ", "").strip()
    
    # Format target based on length
    if len(target) == 10 and target.startswith('0'):
        # Mobile number: pad 00 + 66 + 9 digits -> 13 chars
        formatted_target = "0066" + target[1:]
        account_info = "0016A000000677010111" + f"0113{formatted_target}"
    elif len(target) == 13:
        # National ID: 13 chars
        account_info = "0016A000000677010111" + f"0213{target}"
    else:
        raise ValueError("Invalid PromptPay ID. Must be 10-digit mobile number or 13-digit National ID.")
        
    payload = [
        "000201",  # Payload Format Indicator (Version 01)
        "010212" if amount else "010211",  # Point of Initiation Method (11 = Static, 12 = Dynamic)
        f"29{len(account_info):02d}{account_info}",  # Merchant Account Information (PromptPay ID)
        "5303764",  # Transaction Currency (764 = THB)
    ]
    
    if amount is not None:
        amount_str = f"{amount:.2f}"
        payload.append(f"54{len(amount_str):02d}{amount_str}")
        
    payload.append("5802TH")  # Country Code
    
    payload_str = "".join(payload) + "6304"
    crc_val = crc16_ccitt(payload_str)
    return payload_str + crc_val
