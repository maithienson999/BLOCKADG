import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Chỉ lấy duy nhất link gốc của ABPVN
URL = "https://raw.githubusercontent.com/abpvn/abpvn/master/filter/abpvn-hosts.txt"

domains = set()

try:
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        for line in content.splitlines():
            line = line.strip()
            # Bắt đúng dòng bắt đầu bằng "0.0.0.0 " của ABPVN
            if line.startswith('0.0.0.0 '):
                domain = line.replace('0.0.0.0 ', '').strip()
                if domain:
                    domains.add(domain)
except Exception as e:
    print(f"Lỗi khi tải ABPVN: {e}")

# Xuất chuẩn format cho AdGuard Home
with open("blocklist.txt", "w", encoding="utf-8") as f:
    f.write("! Title: ABPVN List\n\n")
    for d in sorted(domains):
        f.write(f"||{d}^\n")

print(f"Thành công: Đã tạo file với {len(domains)} domains từ ABPVN.")
