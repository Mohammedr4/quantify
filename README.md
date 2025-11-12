# Quantify - Pro FinTech SaaS

Quantify is a "data-first" Investment Ledger and UK Capital Gains Tax engine. 
It solves the problem of tracking "True Total Return" and calculating tax liabilities using the complex UK "Section 104" pooling rules.

**Live Demo:** [https://getquantify.co.uk](https://getquantify.co.uk)

## 🚀 The Stack (The "Strong Base")

I built this using a "basics-first," high-quality architecture to ensure reliability and speed.

* **Backend:** Django 5 (Python), PostgreSQL
* **Frontend:** HTMX, TailwindCSS (No heavy JS framework, aiming for "snappy" server-side rendering)
* **Data Engine:** yfinance (Synchronous engine, ready for Celery scaling)
* **Testing:** Pytest, TDD (Test-Driven Development)
* **Infrastructure:** Railway, Gunicorn, WhiteNoise, CI/CD via GitHub Actions

## 🛠️ Key Features

* **High-Performance Ledger:** A transaction-based double-entry style system for tracking buys, sells, and fees.
* **UK Tax Console:** A custom-built financial engine that implements **UK Section 104 Share Pooling** logic to calculate allowable costs and realized gains.
* **"True Return" Analytics:** tracks performance based on cost-basis vs. current market value.
* **HTMX Calculators:** "Guest" tools that run complex math server-side without page reloads.

## 🏗️ Local Setup

1.  Clone the repo
2.  `python -m venv venv`
3.  `source venv/Scripts/activate`
4.  `pip install -r requirements.txt`
5.  `cp .env.example .env` (Configure secrets)
6.  `python manage.py migrate`
7.  `python manage.py runserver`

## 🧪 Testing

Run the TDD suite:
`python manage.py test apps.analysis`