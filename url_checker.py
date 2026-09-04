from urllib.parse import urlparse
import ipaddress


# Common URL shortening services
URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "ow.ly",
    "buff.ly",
    "cutt.ly",
    "rb.gy",
    "shorturl.at",
}


# Keywords that can appear in suspicious URLs
SUSPICIOUS_KEYWORDS = {
    "login",
    "signin",
    "verify",
    "verification",
    "secure",
    "account",
    "update",
    "confirm",
    "password",
    "bank",
    "payment",
    "wallet",
    "refund",
    "claim",
    "prize",
    "reward",
}


# TLDs that are sometimes seen in suspicious/spam links.
# Having one of these does NOT mean the URL is malicious.
UNUSUAL_TLDS = {
    "xyz",
    "top",
    "click",
    "zip",
    "work",
    "live",
    "buzz",
    "icu",
    "tk",
    "ml",
    "ga",
    "cf",
}


def is_ip_address(hostname):
    """Check whether the hostname is an IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def analyze_url(url):
    """
    Analyze a URL using simple rule-based checks.

    Returns:
        score: risk score from 0 to 100
        signals: list of detected suspicious signals
    """

    score = 0
    signals = []

    # Remove accidental spaces
    url = url.strip()

    if not url:
        return 0, ["No URL was provided."]

    # Add https:// temporarily if the user forgot the scheme.
    # This makes urlparse able to understand domains like example.com.
    url_to_parse = url

    if "://" not in url_to_parse:
        url_to_parse = "https://" + url_to_parse

    parsed = urlparse(url_to_parse)

    hostname = parsed.hostname

    # --------------------------------------------------
    # 1. Check whether the URL has a valid hostname
    # --------------------------------------------------

    if not hostname:
        return 0, ["The URL format could not be understood."]

    hostname = hostname.lower()

    # --------------------------------------------------
    # 2. HTTP vs HTTPS
    # --------------------------------------------------

    if parsed.scheme.lower() == "http":
        signals.append(
            "HTTP is used instead of HTTPS, so the connection is not encrypted in the usual way."
        )
        score += 10

    elif parsed.scheme.lower() == "https":
        signals.append("HTTPS is used.")

    # --------------------------------------------------
    # 3. IP address instead of a normal domain
    # --------------------------------------------------

    if is_ip_address(hostname):
        signals.append(
            "The URL uses an IP address instead of a normal domain name."
        )
        score += 25

    # --------------------------------------------------
    # 4. URL shortener
    # --------------------------------------------------

    if hostname in URL_SHORTENERS:
        signals.append(
            "A URL shortening service is being used, which hides the final destination."
        )
        score += 25

    # --------------------------------------------------
    # 5. Suspicious keywords
    # --------------------------------------------------

    full_url = url.lower()

    found_keywords = []

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in full_url:
            found_keywords.append(keyword)

    if found_keywords:
        signals.append(
            "Potentially suspicious keywords found: "
            + ", ".join(sorted(found_keywords))
        )
        score += min(len(found_keywords) * 5, 20)

    # --------------------------------------------------
    # 6. Unusual TLD
    # --------------------------------------------------

    if "." in hostname:
        tld = hostname.split(".")[-1]

        if tld in UNUSUAL_TLDS:
            signals.append(
                f"The domain uses the .{tld} TLD, which can sometimes appear in suspicious links."
            )
            score += 10

    # --------------------------------------------------
    # 7. Excessive subdomains
    # --------------------------------------------------

    domain_parts = hostname.split(".")

    if len(domain_parts) >= 5:
        signals.append(
            "The domain contains an unusually large number of subdomains."
        )
        score += 10

    # --------------------------------------------------
    # 8. Punycode / encoded-looking domain
    # --------------------------------------------------

    if "xn--" in hostname:
        signals.append(
            "The domain contains punycode, which can sometimes be used to make domains look similar to legitimate ones."
        )
        score += 15

    # --------------------------------------------------
    # 9. Very long URL
    # --------------------------------------------------

    if len(url) > 200:
        signals.append(
            "The URL is unusually long."
        )
        score += 5

    # --------------------------------------------------
    # 10. Suspicious characters/patterns
    # --------------------------------------------------

    if "@" in url:
        signals.append(
            "The URL contains an '@' character, which can sometimes hide the actual destination."
        )
        score += 15

    if hostname.count("-") >= 3:
        signals.append(
            "The domain contains many hyphens, which can be a suspicious-looking pattern."
        )
        score += 5

    # --------------------------------------------------
    # 11. Many query parameters
    # --------------------------------------------------

    if parsed.query:
        parameter_count = parsed.query.count("&") + 1

        if parameter_count >= 5:
            signals.append(
                "The URL contains many query parameters."
            )
            score += 5

    # --------------------------------------------------
    # Final score
    # --------------------------------------------------

    score = min(score, 100)

    # If nothing suspicious was found
    if not signals:
        signals.append(
            "No obvious suspicious URL patterns were detected."
        )

    return score, signals