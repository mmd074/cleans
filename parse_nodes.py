import requests
import random

def get_flag_emoji(code):
    """تبدیل کد ۲ حرفی کشور به ایموجی پرچم"""
    if len(code) != 2 or not code.isalpha():
        return code  # اگر کد معتبر نبود، همون متن اصلی
    
    # کدهای ASCII را به Regional Indicator تبدیل می‌کند
    base = ord("🇦") - ord("A")
    flag = chr(base + ord(code[0].upper())) + chr(base + ord(code[1].upper()))
    return flag

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
        
        # استخراج ۲ حرف اول برای پرچم و بقیه نام سرور
        country_code = name[:2].upper()
        server_name = name[2:] if len(name) > 2 else name
        
        # اضافه کردن پرچم فقط اگر ۲ حرف معتبر باشد
        display_name = f"{get_flag_emoji(country_code)}{server_name}"
        
        valid_nodes.append(f"{ip}:{port}#{display_name}_{dc}")

# انتخاب کاملاً رندوم 150 تا
num_to_select = min(150, len(valid_nodes))
random_nodes = random.sample(valid_nodes, num_to_select)

# ذخیره در فایل
with open("nodes.txt", "w", encoding="utf-8") as f:
    for node in random_nodes:
        f.write(f"{node}\n")

print(f"Done! {len(valid_nodes)} total, {len(random_nodes)} random selected.")
