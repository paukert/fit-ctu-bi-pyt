# Web application for managing polls

Python Programming course at FIT CTU (2020/2021).

Detailed description and `report.pdf` is written only in Czech.

## Webová aplikace pro dotazníky
- pro jednoduchou instalaci nezbytných závislostí je připraven soubor `environment.yml`
  - `conda env create -f environment.yml` - vytvoří prostředí z připraveného souboru
  - `conda activate bipyt` - spustí připravené prostředí
- před prvním spuštěním aplikace je potřeba inicializovat databázi pomocí `python manage.py migrate`
  - aplikace vytvoří testovacího uživatele se jménem `Admin` a heslem `Password`
  - pokud se do databáze vloží záznamy ze souboru `dml.sql` bude tento uživatel vlastníkem připravených anket
- celou aplikaci lze následně spustit z této složky (v níž je umístěn i tento `README.md` soubor) pomocí příkazu `python manage.py runserver`
  - aplikace bude pravděpodobně dostupná na adrese `http://127.0.0.1:8000/polls/`
- unit testy lze spustit pomocí příkazu `python manage.py test polls`
