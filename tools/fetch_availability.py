#!/usr/bin/env python3
"""Hakee Ylläs Kajon varaukset iCal-kalentereista ja kirjoittaa assets/availability.json.

Kalenterien osoitteet luetaan ympäristömuuttujasta ICAL_URLS (yksi tai useampi
osoite, eroteltuna rivinvaihdolla, välilyönnillä tai pilkulla). GitHub Actions
-työnkulku antaa sen repon salaisuudesta, joten osoite ei päädy julkiseen repoon.

Tiedostoon kirjoitetaan vain varatut yöt päivämäärinä. Vieraiden nimiä,
tapahtumien otsikoita tai muita tietoja ei tallenneta.

Paikallinen testi tiedostosta:
    ICAL_URLS=file:///polku/kalenteri.ics python3 tools/fetch_availability.py
"""
import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "availability.json"
LOCAL = ZoneInfo("Europe/Helsinki")
MONTHS_AHEAD = 13  # sivulla voi selata 12 kk eteenpäin


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "yllaskajo-availability/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def unfold(text):
    return re.sub(r"\r?\n[ \t]", "", text).splitlines()


def parse_value(params, value):
    """Palauttaa (päivä, onko_kellonaika) paikallisessa ajassa."""
    value = value.strip()
    if re.fullmatch(r"\d{8}", value):
        return date(int(value[:4]), int(value[4:6]), int(value[6:8])), False
    m = re.fullmatch(r"(\d{8})T(\d{6})(Z?)", value)
    if not m:
        raise ValueError(value)
    dt = datetime.strptime(m[1] + m[2], "%Y%m%d%H%M%S")
    if m[3]:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        tz = re.search(r"TZID=([^;:]+)", params)
        try:
            dt = dt.replace(tzinfo=ZoneInfo(tz[1].strip('"')) if tz else LOCAL)
        except Exception:
            dt = dt.replace(tzinfo=LOCAL)
    return dt.astimezone(LOCAL).date(), True


def events(text):
    """Tuottaa (alkupäivä, loppupäivä) -parit, loppu ei sisälly (= lähtöpäivä)."""
    ev = None
    for line in unfold(text):
        if line == "BEGIN:VEVENT":
            ev = {}
        elif line == "END:VEVENT" and ev is not None:
            if ev.get("STATUS", "").upper() != "CANCELLED" and "DTSTART" in ev:
                start, timed = parse_value(*ev["DTSTART"])
                if "DTEND" in ev:
                    end, _ = parse_value(*ev["DTEND"])
                else:
                    end = start + timedelta(days=1)
                if end <= start:  # saman päivän tapahtuma varaa kyseisen yön
                    end = start + timedelta(days=1)
                yield start, end
            ev = None
        elif ev is not None and ":" in line:
            name, value = line.split(":", 1)
            key, _, params = name.partition(";")
            if key in ("DTSTART", "DTEND"):
                ev[key] = (params, value)
            elif key == "STATUS":
                ev[key] = value.strip()


def main():
    urls = [u for u in re.split(r"[\s,]+", os.environ.get("ICAL_URLS", "")) if u]
    if not urls:
        sys.exit("ICAL_URLS puuttuu")
    today = datetime.now(LOCAL).date()
    first = today.replace(day=1)
    y, m = divmod(first.month - 1 + MONTHS_AHEAD, 12)
    last = date(first.year + y, m + 1, 1)

    nights = set()
    for url in urls:
        for start, end in events(fetch(url)):
            d = max(start, first)
            while d < min(end, last):
                nights.add(d)
                d += timedelta(days=1)

    # Yhdistetään peräkkäiset yöt jaksoiksi [saapuminen, lähtö).
    ranges = []
    for d in sorted(nights):
        if ranges and ranges[-1][1] == d:
            ranges[-1][1] = d + timedelta(days=1)
        else:
            ranges.append([d, d + timedelta(days=1)])
    data = {"booked": [[a.isoformat(), b.isoformat()] for a, b in ranges]}

    old = None
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text(encoding="utf-8"))
        except ValueError:
            pass
    if old and old.get("booked") == data["booked"]:
        print("Ei muutoksia:", len(ranges), "varausjaksoa")
        return
    data["updated"] = datetime.now(LOCAL).isoformat(timespec="minutes")
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("Kirjoitettu", OUT.relative_to(ROOT), "–", len(ranges), "varausjaksoa")


if __name__ == "__main__":
    main()
