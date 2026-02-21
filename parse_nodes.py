import requests
import random
from datetime import datetime

def get_flag_emoji(code):
    if len(code) != 2 or not code.isalpha():
        return code
    base = ord("🇦") - ord("A")
    flag = chr(base + ord(code[0].upper())) + chr(base + ord(code[1].upper()))
    return flag

url = "https://raw.githubusercontent.com/tadesomika/ALVA/refs/heads/main/active.txt"

response = requests.get(url)
response.raise_for_status()
lines = response.text.strip().split("\n")

valid_nodes = []
for line in lines:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) >= 4:
        ip = parts[0]
        port = parts[1]
        name = parts[2]
        dc = parts[3]
        
        country_code = name[:2].upper()
        server_name = name[2:] if len(name) > 2 else name
        display_name = f"{get_flag_emoji(country_code)}{server_name}"
        
        valid_nodes.append(f"{ip}:{port}#{display_name}_{dc}")

num_to_select = min(150, len(valid_nodes))
random_nodes = random.sample(valid_nodes, num_to_select)

# نام فایل با timestamp (هر بار متفاوت)
timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M")
filename = f"nodes-{timestamp}.txt"

with open(filename, "w", encoding="utf-8") as f:
    for node in random_nodes:
        f.write(f"{node}\n")

# لینک اصلی را آپدیت کن (همیشه آخرین فایل)
with open("nodes.txt", "w", encoding="utf-8") as f:
    f.write(f"https://raw.githubusercontent.com/mmd074/cleans/main/{filename}\n")

print(f"Done! Created {filename}")
