import urllib.request
import re

SOURCES = [
    "https://raw.githubusercontent.com/abpvn/abpvn/master/filter/abpvn-hosts.txt",
    "https://raw.githubusercontent.com/bigdargon/hostsVN/master/option/hostsVN-adguard.txt"
]

domains = set()

for url in SOURCES:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            lines = response.read().decode('utf-8').splitlines()
            for line in lines:
                line = line.strip()
                if not line or line.startswith(('#', '!')):
                    continue
                cleaned = re.sub(r'^(0\.0\.0\.0|127\.0\.0\.1|\|\|)', '', line)
                cleaned = re.sub(r'(\^|\$).*', '', cleaned).strip()
                if cleaned and '.' in cleaned:
                    domains.add(cleaned)
    except Exception as e:
        print(f"Lỗi: {e}")

with open("blocklist.txt", "w", encoding="utf-8") as f:
    f.write("! Title: My Custom Blocklist\n\n")
    for domain in sorted(domains):
        f.write(f"||{domain}^\n")

print("Done")
