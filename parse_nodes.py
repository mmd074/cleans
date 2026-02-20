import requests
import random

url = "https://raw.githubusercontent.com/tadesomika/ALVA/refs/heads/main/active.txt"

response = requests.get(url)
response.raise_for_status()
lines = response.text.strip().split("\n")

# ساخت لیست معتبر از همه لاین‌ها
valid_nodes = []
for line in lines:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) >= 4:
        ip = parts[0]
        port = parts[1]
        name = parts[2]
        dc = parts[3]
        valid_nodes.append(f"{ip}:{port}#{name}_{dc}")

# انتخاب کاملاً رندوم 150 تا (اگر کمتر از 150 تا باشد همه را می‌گیرد)
num_to_select = min(150, len(valid_nodes))
random_nodes = random.sample(valid_nodes, num_to_select)

# ذخیره در فایل
with open("nodes.txt", "w", encoding="utf-8") as f:
    for node in random_nodes:
        f.write(f"{node}\n")

print(f"Done! {len(valid_nodes)} total, {len(random_nodes)} random selected.")
