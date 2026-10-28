import re
import tldextract
from urllib.parse import urlparse
from rapidfuzz import fuzz

BRANDS = ["bkash", "nagad", "rocket", "upay"]
OFFICIAL = {"bkash.com", "nagad.com.bd", "dutchbanglabank.com", "upaybd.com"}
WORDS = ["offer", "bonus", "verify", "login", "update",
         "gift", "prize", "free", "claim", "secure"]

def check_url(url):
    url = url.strip()
    score, reasons = 0, []

    if url.lower().startswith("http://"):
        score += 1
        reasons.append("No HTTPS")
    if not url.lower().startswith(("http://", "https://")):
        url = "https://" + url

    host = urlparse(url).hostname or ""
    ext = tldextract.extract(url)

    if ext.registered_domain in OFFICIAL:
        return {"verdict": "LOOKS OK", "score": 0,
                "reasons": ["Official domain"]}

    if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", host):
        score += 3
        reasons.append("IP address used instead of domain")
    if "@" in url:
        score += 2
        reasons.append("'@' symbol in link")
    if ext.subdomain.count(".") >= 2:
        score += 1
        reasons.append("Too many subdomains")
    if "-" in ext.domain:
        score += 1
        reasons.append("Hyphen in domain")

    found = [w for w in WORDS if w in url.lower()]
    if found:
        score += min(len(found), 2)
        reasons.append("Suspicious words: " + ", ".join(found))

    for b in BRANDS:
        if b in ext.domain or b in ext.subdomain:
            score += 3
            reasons.append(f"Brand '{b}' used in unofficial domain")
            break
        if fuzz.ratio(ext.domain, b) >= 80:
            score += 3
            reasons.append(f"Domain looks like '{b}' (typo trick)")
            break

    verdict = ("DANGEROUS" if score >= 5
               else "SUSPICIOUS" if score >= 3 else "LOOKS OK")
    return {"verdict": verdict, "score": score,
            "reasons": reasons or ["No red flags found"]}