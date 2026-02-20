import requests

url = "https://raw.githubusercontent.com/tadesomika/ALVA/refs/heads/main/active.txt"

response = requests.get(url)
lines = response.text.strip().split("\n")

with open("nodes.txt", "w", encoding="utf-8") as f:
    for i, line in enumerate(lines, 1):
        parts = line.strip().split()
        if len(parts) >= 2:
            ip = parts[-2]
            port = parts[-1]
            f.write(f'{{"ip": "{ip}", "port": {port}, "name": "گره {i}"}},\n')

print(f"Done! {len(lines)} lines processed.")
