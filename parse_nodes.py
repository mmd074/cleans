import requests
import json

# دریافت محتوای فایل از GitHub
url = "https://raw.githubusercontent.com/tadesomika/ALVA/refs/heads/main/active.txt"

try:
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.strip().split('\n')
    
    # پردازش هر خط
    nodes = []
    for i, line in enumerate(lines, 1):
        parts = line.strip().split()
        if len(parts) >= 2:
            ip = parts[-2]  # عدد قبل از آخر
            port = parts[-1]  # عدد آخر
            nodes.append({
                "ip": ip,
                "port": int(port),
                "name": f"گره {i}"
            })
    
    # ذخیره در فایل JSON
    with open('nodes.json', 'w', encoding='utf-8') as f:
        json.dump(nodes, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تعداد {len(nodes)} گره با موفقیت پردازش شد")
    
except Exception as e:
    print(f"❌ خطا: {e}")
