# Kariyer.net public listing experiment

Runs on the isolated experiment branch only; does not touch portfolio pages.
Collects publicly accessible pages with robots.txt checks, sequential requests,
>=2 seconds between requests, no authentication, CAPTCHA avoidance or proxies.

Outputs a GitHub Actions artifact containing `jobs.json`, `jobs.csv`,
and `report.json`. Records require independent verification before applying:
a listed URL or JSON-LD is **not evidence that applications are currently open**.

Important: Some pages may block GitHub-hosted IP addresses, disallow automation,
or omit structured JobPosting data. These cases are recorded, not hidden.
No persistent scraping database, user identity, cookies or CV are stored.
Only manual/branch-push execution is configured, no periodic polling.
