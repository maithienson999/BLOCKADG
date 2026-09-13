import urllib.request

# Link AdGuard DNS filter chuẩn
URL = "https://adguardteam.github.io/HostlistsRegistry/assets/filter_16.txt"

try:
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read().decode('utf-8', errors='ignore')

    # Bê nguyên xi dữ liệu sang blocklist.txt
    with open("blocklist.txt", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Đã bê toàn bộ dữ liệu thành công!")
except Exception as e:
    print(f"Lỗi: {e}")
