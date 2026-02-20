import requests

url = "https://raw.githubusercontent.com/tadesomika/ALVA/refs/heads/main/active.txt"

response = requests.get(url)
response.raise_for_status()
lines = response.text.strip().split("\n")

with open("nodes.txt", "w", encoding="utf-8") as f:
    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 4:
            continue  # اگر لاین ناقص بود، ردش می‌کنیم

        ip = parts[0]          # بخش اول
        port = parts[1]        # بخش دوم
        name = parts[2]        # بخش سوم (نام گره، مثل CA)
        dc = parts[3]          # بخش چهارم (دیتاسنتر، مثل OVHcloud)

        # فرمت مورد نظر: part1:part2#part3_part4
        f.write(f"{ip}:{port}#{name}_{dc}\n")

print(f"Done! {len(lines)} lines processed.")
