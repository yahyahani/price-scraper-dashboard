# 📊 Price Scraper Dashboard

Een leerproject: een Python web scraper die boekendata verzamelt van
[books.toscrape.com](https://books.toscrape.com) (een legale oefen-site voor scraping),
opslaat in een SQLite database, en visualiseert in een interactief Streamlit dashboard.

Het dashboard ondersteunt **Nederlands, Engels en Arabisch** (inclusief RTL-layout).

> 🇳🇱 Nederlands | 🇬🇧 [English](#-price-scraper-dashboard-en) | 🇸🇦 [العربية](#-لوحة-تحكم-سحب-الأسعار-ar)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-red)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- 🕷️ **Web scraper** (`requests` + `BeautifulSoup`) met paginatie en beleefde delays
- 🗄️ **SQLite database** voor persistente opslag, inclusief historische data
- 📈 **Interactief dashboard** (Streamlit + Plotly): filters, zoeken, prijsgeschiedenis per item
- 🌐 **Meertalig** (NL / EN / AR) met automatische RTL-layout voor Arabisch
- ⏰ **Optionele scheduler** om automatisch periodiek te scrapen
- 🧩 **Uitbreidbare architectuur** — voeg makkelijk een nieuwe scraper toe (vacatures, nieuws, etc.)

## 📁 Projectstructuur

```
price-scraper-dashboard/
├── main.py                # Entry point: runt de scraper
├── requirements.txt
├── scraper/
│   ├── scraper.py          # Scraping logica (books.toscrape.com)
│   └── database.py         # SQLite database laag
├── dashboard/
│   ├── app.py               # Streamlit dashboard
│   └── i18n.py              # Vertaal-helper
├── locales/
│   ├── nl.json
│   ├── en.json
│   └── ar.json
└── data/
    └── scraper.db           # Wordt automatisch aangemaakt
```

## 🚀 Installatie & gebruik (macOS)

```bash
# 1. Clone de repository
git clone https://github.com/<jouw-gebruikersnaam>/price-scraper-dashboard.git
cd price-scraper-dashboard

# 2. Maak een virtual environment (aanbevolen)
python3 -m venv venv
source venv/bin/activate

# 3. Installeer dependencies
pip install -r requirements.txt

# 4. Run de scraper (verzamelt data)
python main.py

# 5. Start het dashboard
streamlit run dashboard/app.py
```

Het dashboard opent automatisch in je browser op `http://localhost:8501`.

### Automatisch periodiek scrapen

```bash
python main.py --schedule --interval 6   # elke 6 uur
```

## 🧩 Een nieuwe scraper toevoegen

Dit project is gemaakt om uit te breiden naar andere databronnen (bv. vacatures of nieuws):

1. Maak een nieuw bestand, bv. `scraper/jobs_scraper.py`
2. Schrijf een functie die een lijst van `dict`s teruggeeft met de keys:
   `source, category, title, price, currency, availability, url`
   (gebruik `None` voor velden die niet van toepassing zijn, bv. `price` bij vacatures)
3. Importeer en roep die functie aan in `main.py`
4. Klaar — het dashboard en de database werken automatisch met de nieuwe data

## 🛠️ Gebruikte technologieën

| Onderdeel | Technologie |
|---|---|
| Scraping | `requests`, `BeautifulSoup4` |
| Database | `sqlite3` (Python standaardbibliotheek) |
| Dashboard | `Streamlit`, `Plotly`, `pandas` |
| Scheduling | `schedule` |

## 📜 Licentie

MIT — vrij te gebruiken voor leren en eigen projecten.

## ⚖️ Over verantwoord scrapen

Deze scraper gebruikt [books.toscrape.com](https://books.toscrape.com), een website die
specifiek gemaakt is om scraping te oefenen. Check bij andere websites altijd het
`robots.txt` bestand en de gebruiksvoorwaarden voordat je ze scraapt, en gebruik
altijd redelijke delays tussen requests.

---

<a id="-price-scraper-dashboard-en"></a>
## 📊 Price Scraper Dashboard (EN)

A learning project: a Python web scraper that collects book data from
[books.toscrape.com](https://books.toscrape.com) (a legal scraping sandbox site),
stores it in a SQLite database, and visualizes it in an interactive Streamlit dashboard.

The dashboard supports **Dutch, English, and Arabic** (including RTL layout).

### Features

- 🕷️ Web scraper (`requests` + `BeautifulSoup`) with pagination and polite delays
- 🗄️ SQLite database for persistent storage, including historical data
- 📈 Interactive dashboard (Streamlit + Plotly): filters, search, per-item price history
- 🌐 Multi-language (NL / EN / AR) with automatic RTL layout for Arabic
- ⏰ Optional scheduler for automatic periodic scraping
- 🧩 Extensible architecture — easily add a new scraper (jobs, news, etc.)

### Installation & usage (macOS)

```bash
git clone https://github.com/<your-username>/price-scraper-dashboard.git
cd price-scraper-dashboard

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python main.py                       # run the scraper once
streamlit run dashboard/app.py       # launch the dashboard
```

For automatic periodic scraping:

```bash
python main.py --schedule --interval 6
```

### Adding a new scraper

1. Create a new file, e.g. `scraper/jobs_scraper.py`
2. Write a function that returns a list of `dict`s with keys:
   `source, category, title, price, currency, availability, url`
3. Import and call it from `main.py`
4. Done — the dashboard and database automatically support the new data

### Responsible scraping

This scraper targets [books.toscrape.com](https://books.toscrape.com), a website built
specifically for scraping practice. For other websites, always check `robots.txt` and
the terms of service first, and use reasonable delays between requests.

### License

MIT — free to use for learning and personal projects.

---

<a id="-لوحة-تحكم-سحب-الأسعار-ar"></a>
## 📊 لوحة تحكم سحب الأسعار (AR)

مشروع تعليمي: أداة سحب بيانات بلغة Python تجمع بيانات الكتب من موقع
[books.toscrape.com](https://books.toscrape.com) (موقع تدريبي قانوني مخصص لتعلم سحب البيانات)،
تخزّنها في قاعدة بيانات SQLite، وتعرضها في لوحة تحكم تفاعلية باستخدام Streamlit.

تدعم اللوحة **اللغات: الهولندية، الإنجليزية، والعربية** (مع دعم تلقائي للكتابة من اليمين لليسار).

### المميزات

- 🕷️ أداة سحب بيانات (`requests` + `BeautifulSoup`) مع دعم الصفحات المتعددة وفواصل زمنية مهذبة
- 🗄️ قاعدة بيانات SQLite لتخزين دائم، تشمل البيانات التاريخية
- 📈 لوحة تحكم تفاعلية (Streamlit + Plotly): فلاتر، بحث، تاريخ السعر لكل عنصر
- 🌐 دعم تعدد اللغات (هولندي / إنجليزي / عربي) مع تخطيط تلقائي من اليمين لليسار للعربية
- ⏰ جدولة اختيارية للسحب التلقائي الدوري
- 🧩 بنية قابلة للتوسيع — يمكن إضافة أداة سحب جديدة بسهولة (وظائف، أخبار، إلخ)

### التثبيت والاستخدام (macOS)

```bash
git clone https://github.com/<اسم-المستخدم>/price-scraper-dashboard.git
cd price-scraper-dashboard

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python main.py                       # تشغيل أداة السحب مرة واحدة
streamlit run dashboard/app.py       # تشغيل لوحة التحكم
```

للسحب التلقائي الدوري:

```bash
python main.py --schedule --interval 6
```

### إضافة أداة سحب جديدة

1. أنشئ ملفًا جديدًا، مثل `scraper/jobs_scraper.py`
2. اكتب دالة تُرجع قائمة من القواميس (`dict`) تحتوي على المفاتيح:
   `source, category, title, price, currency, availability, url`
3. استورد الدالة واستخدمها في `main.py`
4. تم — ستعمل لوحة التحكم وقاعدة البيانات تلقائيًا مع البيانات الجديدة

### السحب المسؤول للبيانات

تستهدف هذه الأداة موقع [books.toscrape.com](https://books.toscrape.com)، وهو موقع مُصمم
خصيصًا للتدريب على سحب البيانات. بالنسبة للمواقع الأخرى، تحقق دائمًا من ملف `robots.txt`
وشروط الاستخدام أولاً، واستخدم فواصل زمنية معقولة بين الطلبات.

### الترخيص

MIT — حر الاستخدام للتعلم والمشاريع الشخصية.
