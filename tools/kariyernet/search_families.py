"""CV-based bounded search families. No bypass; only public results and approved collector."""
from urllib.parse import urlencode
FAMILIES = {
 "mechanical": ["makine mühendisi","mechanical engineer","mekanik bakım mühendisi"],
 "manufacturing": ["imalat mühendisi","üretim mühendisi","üretim planlama mühendisi","proses mühendisi"],
 "design": ["mekanik tasarım mühendisi","SolidWorks","CAD CAM mühendisi","kalıp tasarım mühendisi"],
 "quality": ["kalite kontrol mühendisi","kalite güvence mühendisi","NDT"],
 "junior": ["yeni mezun makine mühendisi","yetiştirilmek üzere makine mühendisi"]
}
PLACES=["Kahramanmaraş","Gaziantep","Osmaniye","Adana","Kayseri","Malatya","Mersin","Ankara"]
def build_queries(limit=32):
    # Deterministic and bounded; alternate technology queries are explicit.
    return [f"{term} {city}" for family in FAMILIES.values() for term in family for city in PLACES][:limit]
