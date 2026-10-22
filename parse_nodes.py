import requests
import random

def get_flag_emoji(code):
    """تبدیل کد ۲ حرفی کشور به ایموجی پرچم"""
    if len(code) != 2 or not code.isalpha():
        return code
    base = ord("🇦") - ord("A")
    flag = chr(base + ord(code[0].upper())) + chr(base + ord(code[1].upper()))
    return flag

# پورت‌های مجاز برای N.tls
NOTLS_PORTS = [80, 8080, 8880, 2052, 2082, 2086, 2095]

# ایموجی یکسان برای همه کانفیگ‌های N.tls
NOTLS_EMOJI = "🛡️"

url = "https://raw.githubusercontent.com/FoolVPN-ID/Nautica/refs/heads/main/proxyList.txt"
response = requests.get(url)
response.raise_for_status()

lines = response.text.strip().split("\n")

# ساخت لیست معتبر از همه لاین‌ها (فرمت خام CSV: ip,port,country,dc)
valid_raw = []
for line in lines:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) >= 4:
        valid_raw.append(parts)

# نیاز به حداقل 150 نود داریم (100 + 50)
num_to_select = min(150, len(valid_raw))
random_nodes = random.sample(valid_raw, num_to_select)

# ---- 100 کانفیگ معمولی (فرمت اصلی) ----
regular_nodes = []
for parts in random_nodes[:100]:
    ip     = parts[0]
    port   = parts[1]
    name   = parts[2]
    dc     = parts[3]
    country_code = name[:2].upper()
    server_name  = name[2:] if len(name) > 2 else name
    display_name = f"{get_flag_emoji(country_code)}{server_name}"
    regular_nodes.append(f"{ip}:{port}#{display_name}_{dc}")

with open("nodes.txt", "w", encoding="utf-8") as f:
    for node in regular_nodes:
        f.write(f"{node}\n")

# ---- 50 کانفیگ N.tls (فرمت جدید) ----
notls_nodes = []
for parts in random_nodes[100:150]:
    ip   = parts[0]
    name = parts[2]           # مثلاً DE یا HOS
    dc   = parts[3]           # مثلاً HOS-512604

    # تبدیل پورت به یکی از پورت‌های مجاز (رندوم)
    new_port = random.choice(NOTLS_PORTS)

    # استخراج کد کشور و ساخت ایموجی پرچم
    country_code = name[:2].upper()
    flag_emoji   = get_flag_emoji(country_code)

    # فرمت: ip:port#🌍🛡️CC_(N.tls)DC
    notls_nodes.append(f"{ip}:{new_port}#{flag_emoji}{NOTLS_EMOJI}{country_code}_(N.tls){dc}")

with open("nodes_notls.txt", "w", encoding="utf-8") as f:
    for node in notls_nodes:
        f.write(f"{node}\n")

print(f"Done!")
print(f"  Total available : {len(valid_raw)}")
print(f"  nodes.txt       : {len(regular_nodes)} configs (original format)")
print(f"  nodes_notls.txt : {len(notls_nodes)} configs (N.tls format)")
