import urllib.request
import re
import ssl

# Bỏ qua lỗi SSL certificate nếu có
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

SOURCES = [
    "https://cdn.jsdelivr.net/gh/abpvn/abpvn@master/filter/abpvn-hosts.txt",
    "https://raw.githubusercontent.com/bigdargon/hostsVN/master/option/hostsVN-adguard.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt"
]

domains = set()

for url in SOURCES:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            lines = response.read().decode('utf-8', errors='ignore').splitlines()
            for line in lines:
                line = line.strip()
                if not line or line.startswith(('#', '!', '[')):
                    continue
                cleaned = re.sub(r'^(0\.0\.0\.0|127\.0\.0\.1|\|\|)', '', line)
                cleaned = re.sub(r'(\^|\$).*', '', cleaned).strip()
                if cleaned and '.' in cleaned and not cleaned.startswith('.'):
                    domains.add(cleaned)
    except Exception as e:
        print(f"Lỗi fetch {url}: {e}")

with open("blocklist.txt", "w", encoding="utf-8") as f:
    f.write("! Title: My Custom Blocklist\n\n")
    for domain in sorted(domains):
        f.write(f"||{domain}^\n")

print(f"Done: {len(domains)} domains")

