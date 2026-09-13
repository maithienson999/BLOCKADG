import urllib.request

# Dùng thẳng trang chủ của ABPVN và link CDN để không bị GitHub chặn
SOURCES = [
    "https://abpvn.com/filter/abpvn-hosts.txt",
    "https://cdn.jsdelivr.net/gh/abpvn/abpvn@master/filter/abpvn-hosts.txt"
]

data = ""

for url in SOURCES:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode('utf-8', errors='ignore')
            # Nếu tải được nội dung dài (thành công) thì dừng vòng lặp
            if len(data) > 1000:
                print(f"Đã tải thành công từ: {url}")
                break
    except Exception as e:
        print(f"Lỗi khi tải từ {url}: {e}")

# Lưu thẳng nội dung gốc vào file, AdGuard Home tự đọc được hết
with open("blocklist.txt", "w", encoding="utf-8") as f:
    f.write("! Title: ABPVN Fixed Mirror\n\n")
    if data:
        f.write(data)
    else:
        f.write("! LỖI: Không thể kết nối đến máy chủ ABPVN.")

print("Hoàn tất!")
