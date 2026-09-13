import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Danh sách nguồn tải
SOURCES = [
    "https://raw.githubusercontent.com/bigdargon/hostsVN/master/option/hostsVN-adguard.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt"
]

# Bộ domain mặc định dự phòng (Đảm bảo list không bao giờ trống)
domains = {
    "doubleclick.net", "googleadservices.com", "adnxs.com", 
    "admicro.vn", "ants.vn", "eclick.vn", "ezoic.net"
}

# Tải thêm từ các nguồn online
for url in SOURCES:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            for line in content.splitlines():
                line = line.strip()
                if line.startswith('||') and '^' in line:
                    # Lấy domain từ dạng ||example.com^
                    d = line.replace('||', '').split('^')[0].strip()
                    if d and '.' in d:
                        domains.add(d)
    except Exception as e:
        print(f"Lỗi nguồn {url}: {e}")

# Ghi ra file theo chuẩn AdGuard Home
with open("blocklist.txt", "w", encoding="utf-8") as f:
    f.write("! Title: My DNS Blocklist\n\n")
    for d in sorted(domains):
        f.write(f"||{d}^\n")

print(f"Đã xuất thành công {len(domains)} domains.")

