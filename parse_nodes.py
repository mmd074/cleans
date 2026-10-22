import requests
import random

def get_flag_emoji(code):
    """تبدیل کد ۲ حرفی کشور به ایموجی پرچم"""
    if len(code) != 2 or not code.isalpha():
        return code
    base = ord("🇦") - ord("A")
    flag = chr(base + ord(code[0].upper())) + chr(base + ord(code[1].upper()))
    return flag

# پورت‌های مجاز برای NoTls
NOTLS_PORTS = [80, 8080, 8880, 2052, 2082, 2086, 2095]

# ایموجی یکسان برای همه کانفیگ‌های NoTls
NOTLS_EMOJI = "🛡️"

url = "https://raw.githubusercontent.com/FoolVPN-ID/Nautica/refs/heads/main/proxyList.txt"
response = requests.get(url)
response.raise_for_status()

lines = response.text.strip().split("\n")

# ساخت لیست معتبر و حذف ip:port تکراری
seen_ip_port = set()
valid_raw = []
for line in lines:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) >= 4:
        key = f"{parts[0]}:{parts[1]}"
        if key not in seen_ip_port:
            seen_ip_port.add(key)
            valid_raw.append(parts)

# shuffle کامل لیست
random.shuffle(valid_raw)

# ---- 150 کانفیگ معمولی (فرمت اصلی) ----
# اگه کل منبع کمتر از 150 بود، هر چقدر هست می‌آد
regular_raw = valid_raw[:150]
regular_nodes = []
regular_ip_ports = set()

for parts in regular_raw:
    ip   = parts[0]
    port = parts[1]
    name = parts[2]
    dc   = parts[3]
    key  = f"{ip}:{port}"
    country_code = name[:2].upper()
    server_name  = name[2:] if len(name) > 2 else name
    display_name = f"{get_flag_emoji(country_code)}{server_name}"
    regular_nodes.append(f"{ip}:{port}#{display_name}_{dc}")
    regular_ip_ports.add(key)

with open("nodes.txt", "w", encoding="utf-8") as f:
    for node in regular_nodes:
        f.write(f"{node}\n")

# ---- 50 کانفیگ NoTls (فرمت جدید) ----
# ip:port تکراری با دسته اول مجاز است ولی داخل این دسته تکراری نباشد
notls_raw = valid_raw[150:]  # ادامه لیست بعد از 150 تا
notls_nodes = []
notls_ip_ports = set()

for parts in notls_raw:
    if len(notls_nodes) >= 50:
        break
    ip   = parts[0]
    name = parts[2]
    dc   = parts[3]

    new_port = random.choice(NOTLS_PORTS)
    key = f"{ip}:{new_port}"

    # اگه همین ip:port_جدید قبلاً توی این دسته بوده، skip
    if key in notls_ip_ports:
        continue

    notls_ip_ports.add(key)
    country_code = name[:2].upper()
    flag_emoji   = get_flag_emoji(country_code)
    notls_nodes.append(f"{ip}:{new_port}#{flag_emoji}{NOTLS_EMOJI}{country_code}_(NoTls){dc}")

with open("nodes_notls.txt", "w", encoding="utf-8") as f:
    for node in notls_nodes:
        f.write(f"{node}\n")

print(f"Done!")
print(f"  Total unique     : {len(valid_raw)}")
print(f"  nodes.txt        : {len(regular_nodes)} configs (original format)")
print(f"  nodes_notls.txt  : {len(notls_nodes)} configs (NoTls format)")
