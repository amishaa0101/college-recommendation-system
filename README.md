# College Recommendation System

A Flask web app that helps Gujarat engineering aspirants find colleges they can realistically get into, using ACPC (Admission Committee for Professional Courses) closing rank data.

Enter your ACPC merit rank, category and preferred program, and the app lists matching colleges sorted by closing rank, each marked **Safe**, **Moderate** or **Reach**. Click any college to see its address, contact details, facilities and tuition fees.

## Features

- **Search by rank**: filter by rank, category (Open, SC, ST, SEBC, EWS, TFWS) and program
- **Chance labels**, based on last year's closing rank:
  - Safe: the closing rank is 20% or more beyond your rank
  - Moderate: your rank is within the cut-off
  - Reach: your rank is up to 10% outside the cut-off
- **Search by college**: see every program at a college with category-wise closing ranks
- **College details page**: address, contact, email, website, district, hostel, mess, transport, fees
- **Feedback form** on the Contact page

## Tech stack

Python, Flask, pandas, Jinja2, HTML, CSS, JavaScript (Fetch API)

## Data

| File | Contents |
|---|---|
| `newcolleges2.csv` | ACPC 2023 closing ranks: 520 rows, 124 colleges, 74 programs |
| `ncdata.csv` | College details for 137 institutes |
| `previous_year_data.csv` | ACPC 2021 closing ranks, kept for upcoming trend analysis |
| `merit-wise-engineering-closure-2023...xlsx` | Original ACPC 2023 closure sheet (source of `newcolleges2.csv`) |
| `cdata.pdf` | Original ACPC college information booklet (source of `ncdata.csv`) |

The raw government PDF and Excel files were cleaned with the helper scripts `datacleaning.py`, `clean_csv_script.py`, `clean_csv_files.py` and `checkcolumn.py`.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Project structure

```
app.py              Flask routes and recommendation logic
templates/          Jinja2 pages (home, about, contact, college info, results table)
static/             CSS, JavaScript and images
*.csv / *.xlsx      Source and cleaned datasets
```

## Planned features

- Predictive analysis of cut-off trends using previous years' data
- Filters for district, fees and facilities
- Alerts for deadlines and scholarships
- Natural language chat interface
