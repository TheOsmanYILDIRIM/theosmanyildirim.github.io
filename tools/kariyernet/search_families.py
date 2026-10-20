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
    """Bounded coverage across cities AND career families, not one family at a time."""
    names=list(FAMILIES)
    queries=[]
    for i in range(max(0,min(limit,40))):
        city=PLACES[i % len(PLACES)]
        family=FAMILIES[names[i % len(names)]]
        term=family[(i // (len(PLACES)*len(names))) % len(family)]
        queries.append(f"{term} {city}")
    return queries
