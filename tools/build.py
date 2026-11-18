#!/usr/bin/env python3
"""Rakentaa Ylläs Kajon markkinointisivuston HTML-sivut (fi + en).

Sisältö on tässä tiedostossa: muokkaa tekstejä, palautteita tai linkkejä ja aja
    python3 tools/build.py
Sivut kirjoitetaan repon juureen (suomi) ja en/-kansioon (englanti).
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://venstedt.github.io/yllaskajo-site"  # vaihdetaan, jos tulee oma verkkotunnus

AIRBNB = {"fi": "https://www.airbnb.fi/rooms/1505850569308831000",
          "en": "https://www.airbnb.com/rooms/1505850569308831000"}
BOOKING = {"fi": "https://www.booking.com/hotel/fi/yllas-kajo.fi.html",
           "en": "https://www.booking.com/hotel/fi/yllas-kajo.en-gb.html"}
EMAIL = "yllaskajo@gmail.com"
INSTAGRAM = "https://www.instagram.com/yllaskajo/"
FACEBOOK = "https://www.facebook.com/profile.php?id=61579861190695"
MAP = "https://www.google.com/maps/search/?api=1&query=Yll%C3%A4s%20Kajo%2C%20Yll%C3%A4sj%C3%A4rvi"

# Sivut: avain -> (fi-tiedosto, en-tiedosto)
PAGES = {
    "home": ("index.html", "index.html"),
    "cabin": ("mokki.html", "cabin.html"),
    "summer": ("kesa.html", "summer.html"),
    "winter": ("talvi.html", "winter.html"),
    "book": ("varaa.html", "book.html"),
}
NAV = {
    "fi": {"home": "Etusivu", "cabin": "Mökki", "summer": "Kesä & syksy", "winter": "Talvi", "book": "Varaa"},
    "en": {"home": "Home", "cabin": "The cabin", "summer": "Summer & autumn", "winter": "Winter", "book": "Book"},
}
DOCK = {
    "fi": {"home": "Etusivu", "cabin": "Mökki", "summer": "Kesä", "winter": "Talvi", "book": "Varaa"},
    "en": {"home": "Home", "cabin": "Cabin", "summer": "Summer", "winter": "Winter", "book": "Book"},
}

ICONS = {
    "home": '<path d="m3 10 9-7 9 7"/><path d="M5 9v12h14V9"/><path d="M9 21v-8h6v8"/>',
    "cabin": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/><path d="M16 6V3h2v5"/>',
    "summer": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "winter": '<path d="M12 2v20M4 6l16 12M20 6 4 18"/><path d="m9 3 3 3 3-3M9 21l3-3 3 3"/>',
    "book": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/><path d="m9 15 2 2 4-4"/>',
    "gondola": '<path d="M2 4l20 4"/><path d="M12 6v4"/><rect x="6" y="10" width="12" height="10" rx="3"/><path d="M6 15h12"/>',
    "ski": '<circle cx="15" cy="4" r="2"/><path d="m4 20 16-4"/><path d="m8 14 3-5 4 2 2 4"/><path d="m11 9-3 2"/>',
    "sauna": '<path d="M8 3c-1 1.5 1 2.5 0 4M12 3c-1 1.5 1 2.5 0 4M16 3c-1 1.5 1 2.5 0 4"/><path d="M4 11h16v9H4z"/><path d="M4 15h16"/>',
    "people": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2c2.8.4 5 2.6 5 5.8"/>',
    "ev": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "pet": '<circle cx="5" cy="10" r="2"/><circle cx="9" cy="5" r="2"/><circle cx="15" cy="5" r="2"/><circle cx="19" cy="10" r="2"/><path d="M8 17c0-2.8 1.8-5 4-5s4 2.2 4 5-1.8 3-4 3-4-.2-4-3z"/>',
    "work": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    "bike": '<circle cx="6" cy="17" r="3.5"/><circle cx="18" cy="17" r="3.5"/><path d="M6 17 9.5 9h6l2.5 8M9.5 9 12 17h-6M14 5h2.5l-1 4"/>',
    "pin": '<path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="18" cy="6" r=".8" fill="currentColor" stroke="none"/>',
    "facebook": '<path d="M14 21v-8h3l.5-4H14V7c0-1.2.4-2 2-2h1.7V1.4A22 22 0 0 0 15.2 1C12.7 1 11 2.5 11 5.3V9H8v4h3v8z" fill="currentColor" stroke="none"/>',
}


def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def img(name, alt, prefix, size="", cls="", eager=False):
    """Kuva assets/img-kansiosta; size '' = 1600px, '-800' = 800px."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{prefix}assets/img/{name}{size}.jpg" '
            f'srcset="{prefix}assets/img/{name}-800.jpg 800w, {prefix}assets/img/{name}.jpg 1600w" '
            f'sizes="(min-width: 860px) 50vw, 100vw" alt="{escape(alt)}" {load} decoding="async">')


# ---------------------------------------------------------------------------
# Asiakaspalautteet. Päivitä kauden lopussa: lisää rivi, aja build.py.
# "text" on näytettävä ote; en-versio on käännös, merkitään "translated".
# ---------------------------------------------------------------------------
REVIEWS = [
    {"name": "Elisa", "country": {"fi": "Suomi", "en": "Finland"}, "source": "Booking.com", "date": None,
     "tags": ["home", "cabin"],
     "fi": "Kaikesta näki, että varustelu on mietitty niin kuin itselle. Kerrankin mökki, jota ei tarvitse siivota heti loman aluksi.",
     "en": "You could tell the equipment was chosen as if for themselves. Finally a cabin you don't need to clean at the start of your holiday."},
    {"name": "Sanna", "country": None, "source": "Airbnb", "date": {"fi": "lokakuu 2026", "en": "October 2026"},
     "tags": ["home"],
     "fi": "Majoittaja on erittäin ystävällinen ja vastaa nopeasti. Kohde on siisti, toimiva ja hyvin varusteltu. Tulemme mielellämme uudestaan.",
     "en": "The host is very friendly and replies quickly. The place is clean, practical and well equipped. We'd love to come back."},
    {"name": "Jenni", "country": {"fi": "Suomi", "en": "Finland"}, "source": "Booking.com", "date": None,
     "tags": ["home", "cabin"],
     "fi": "Sijainti on loistava! Mökki on kodikas, siisti ja hyvin varusteltu. Lattialämmitys tuntui viileän päivän jälkeen suorastaan luksukselta, ja saunassa sai hyvät löylyt.",
     "en": "The location is great! The cabin is cosy, clean and well equipped. After a chilly day the underfloor heating felt like pure luxury, and the sauna was excellent."},
    {"name": "Tapio", "country": None, "source": "Airbnb", "date": {"fi": "heinäkuu 2026", "en": "July 2026"},
     "tags": ["summer"],
     "fi": "Siisti ja käytännöllinen mökki rauhallisella paikalla lähellä Ylläksen hiihtokeskusta.",
     "en": "A clean and practical cabin in a peaceful spot close to the Ylläs ski resort."},
    {"name": "Susanna", "country": {"fi": "Suomi", "en": "Finland"}, "source": "Booking.com", "date": None,
     "tags": ["summer", "cabin"],
     "fi": "Mökissä hyvä varustelu ja sängyissä uni maittoi. Sähköauton lataus plussaa. Ladulle ja talvipyöräreitille vajaan puolen kilometrin matka.",
     "en": "Well equipped, and we slept really well. EV charging is a plus. The ski track and winter cycling route are less than half a kilometre away."},
    {"name": "Beate", "country": None, "source": "Airbnb", "date": {"fi": "tammikuu 2026", "en": "January 2026"},
     "tags": ["winter"],
     "fi": "Meillä oli erittäin mukavat 10 päivää, välillä jopa −30 asteen pakkasessa. Ylläsjärvi on talvella erittäin mukava, ja lähistöllä on monia talviaktiviteetteja.",
     "en": "We had a wonderful 10 days, at times in temperatures as low as −30°C. Ylläsjärvi is lovely in winter, with plenty of winter activities nearby."},
    {"name": "Manon", "country": None, "source": "Airbnb", "date": {"fi": "marraskuu 2025", "en": "November 2025"},
     "tags": ["winter", "home"],
     "fi": "Erittäin hyvä, käytännöllinen ja hyvin varusteltu majoitus lähellä rinteitä. Valtteri on erittäin reagoiva majoittaja ja hyvä neuvonantaja – suosittelen!",
     "en": "A very good, practical and well-equipped place close to the slopes. Valtteri is a very responsive host with great advice – recommended!"},
    {"name": "Lauri", "country": {"fi": "Suomi", "en": "Finland"}, "source": "Booking.com", "date": None,
     "tags": ["winter"],
     "fi": "Avain odotti numerolukkoboksissa ja mökki oli saapuessa siisti ja lämmin. Sijainti on erinomainen.",
     "en": "The key was waiting in the lock box and the cabin was clean and warm when we arrived. Excellent location."},
]

T = {
    "fi": {
        "lang_switch": "EN", "lang_switch_label": "In English",
        "skip": "Siirry sisältöön",
        "book_btn": "Varaa",
        "check_dates": "Tarkista vapaat päivät",
        "see_cabin": "Katso mökki",
        "rating_airbnb": "Airbnb · 5 arviota",
        "rating_booking": "Booking.com · 9 arviota",
        "rating_location": "Sijainti (Booking)",
        "rating_host": "Majoittaja (Booking)",
        "reviews_eyebrow": "Vieraiden palautteet",
        "reviews_title": "Mitä vieraamme sanovat",
        "reviews_lead": "Otteita Airbnb- ja Booking.com-arvosteluista.",
        "read_airbnb": "Kaikki arviot Airbnb:ssä",
        "read_booking": "Kaikki arviot Bookingissa",
        "translated": "",
        "cta_title": "Varaa lomasi Ylläs Kajoon",
        "cta_text": "Näet vapaat päivät ja hinnat Airbnb:ssä ja Booking.comissa. Kysy rohkeasti myös suoraan meiltä – vastaamme yleensä tunnin sisällä.",
        "ask": "Kysy meiltä",
        "mail_subject": "Varauskysely Ylläs Kajo",
        "footer_tag": "Tunturien rauhaa • Lapin elämyksiä",
        "footer_hosts": "Majoittajina Riikka & Valtteri",
        "draft": "LUONNOS",
    },
    "en": {
        "lang_switch": "FI", "lang_switch_label": "Suomeksi",
        "skip": "Skip to content",
        "book_btn": "Book",
        "check_dates": "Check availability",
        "see_cabin": "See the cabin",
        "rating_airbnb": "Airbnb · 5 reviews",
        "rating_booking": "Booking.com · 9 reviews",
        "rating_location": "Location (Booking)",
        "rating_host": "Hosts (Booking)",
        "reviews_eyebrow": "Guest reviews",
        "reviews_title": "What our guests say",
        "reviews_lead": "Excerpts from Airbnb and Booking.com reviews, translated into English.",
        "read_airbnb": "All reviews on Airbnb",
        "read_booking": "All reviews on Booking.com",
        "translated": "Translated",
        "cta_title": "Book your stay at Ylläs Kajo",
        "cta_text": "See available dates and prices on Airbnb and Booking.com. You're also welcome to ask us directly – we usually reply within an hour.",
        "ask": "Ask us",
        "mail_subject": "Booking enquiry Ylläs Kajo",
        "footer_tag": "Fellside tranquillity • Lapland adventures",
        "footer_hosts": "Hosted by Riikka & Valtteri",
        "draft": "DRAFT",
    },
}


def href(lang, key, cur_lang):
    """Linkki sivulle `key` kielellä `lang`, kun ollaan kielen `cur_lang` sivulla."""
    fname = PAGES[key][0 if lang == "fi" else 1]
    if lang == cur_lang:
        return fname
    return ("en/" + fname) if lang == "en" else ("../" + fname)


def reviews_block(lang, tag=None, limit=None):
    t = T[lang]
    items = [r for r in REVIEWS if tag is None or tag in r["tags"]]
    if limit:
        items = items[:limit]
    cards = []
    for r in items:
        meta = [r["source"]]
        if r["date"]:
            meta.append(r["date"][lang])
        who = r["name"] + (f', {r["country"][lang]}' if r["country"] else "")
        tr = f' · {t["translated"]}' if t["translated"] else ""
        cards.append(f'''<article class="review">
    <div class="stars" aria-hidden="true">★★★★★</div>
    <blockquote>”{escape(r[lang])}”</blockquote>
    <footer><strong>{escape(who)}</strong><span>{" · ".join(meta)}{tr}</span></footer>
</article>''')
    return f'''<section id="palautteet" aria-labelledby="reviews-title">
    <p class="eyebrow">{t["reviews_eyebrow"]}</p>
    <h2 class="title" id="reviews-title">{t["reviews_title"]}</h2>
    <p class="lead">{t["reviews_lead"]}</p>
    <div class="reviews" tabindex="0">
        {"".join(cards)}
    </div>
    <div class="review-sources">
        <a class="btn btn-line" href="{AIRBNB[lang]}" target="_blank" rel="noopener">★ 5,0 · {t["read_airbnb"]}</a>
        <a class="btn btn-line" href="{BOOKING[lang]}" target="_blank" rel="noopener">9,2 · {t["read_booking"]}</a>
    </div>
</section>'''


def cta_block(lang):
    t = T[lang]
    return f'''<aside class="cta" aria-labelledby="cta-title">
    <h2 id="cta-title">{t["cta_title"]}</h2>
    <p>{t["cta_text"]}</p>
    <div class="hero-actions">
        <a class="btn" href="{AIRBNB[lang]}" target="_blank" rel="noopener">Airbnb</a>
        <a class="btn" href="{BOOKING[lang]}" target="_blank" rel="noopener">Booking.com</a>
        <a class="btn btn-ghost" href="mailto:{EMAIL}?subject={t["mail_subject"].replace(" ", "%20")}">{icon("mail")}{t["ask"]}</a>
    </div>
</aside>'''


def trust_block(lang):
    t = T[lang]
    return f'''<div class="trust" aria-label="Arviot">
    <a href="{AIRBNB[lang]}" target="_blank" rel="noopener"><strong>★ 5,0</strong><span>{t["rating_airbnb"]}</span></a>
    <a href="{BOOKING[lang]}" target="_blank" rel="noopener"><strong>9,2</strong><span>{t["rating_booking"]}</span></a>
    <div><strong>9,7</strong><span>{t["rating_location"]}</span></div>
    <div><strong>10</strong><span>{t["rating_host"]}</span></div>
</div>'''


def hero(title, lead, image, prefix, pill=None, actions="", short=False, winter_image=None):
    cls = "hero short" if short else "hero"
    data = ""
    if winter_image:
        data = (f' data-summer="{prefix}assets/img/{image}.jpg" '
                f'data-winter="{prefix}assets/img/{winter_image}.jpg"')
    p = f'<span class="pill">{pill}</span>' if pill else ""
    return f'''<header class="{cls}" style="background-image:url('{prefix}assets/img/{image}.jpg')"{data}>
    <div class="hero-inner">
        {p}
        <h1>{title}</h1>
        <p class="hero-lead">{lead}</p>
        <div class="hero-actions">{actions}</div>
    </div>
</header>'''


# ---------------------------------------------------------------------------
# Sivujen sisältö
# ---------------------------------------------------------------------------

def page_home(lang, p):
    t = T[lang]
    fi = lang == "fi"
    actions = (f'<a class="btn btn-dark" href="{href(lang, "book", lang)}">{icon("book")}{t["check_dates"]}</a>'
               f'<a class="btn btn-ghost" href="{href(lang, "cabin", lang)}">{t["see_cabin"]}</a>')
    features = [
        ("gondola", "1 km gondolille" if fi else "1 km to the gondola",
         "Ylläksen gondolihissin ala-asema noin kilometrin päässä." if fi else "The Ylläs gondola base station is about a kilometre away."),
        ("ski", "Ladut ja polut ovelta" if fi else "Trails from the door",
         "Hiihtoladulle ja pyöräreitille alle puoli kilometriä." if fi else "Ski tracks and bike routes less than 500 m away."),
        ("sauna", "Oma sauna ja takka" if fi else "Private sauna & fireplace",
         "Puulämmitteinen takka, sauna ja lattialämmitys." if fi else "Wood-burning fireplace, sauna and underfloor heating."),
        ("people", "Tilaa kuudelle" if fi else "Sleeps six",
         "Makuuhuone alakerrassa ja parvella vuoteet neljälle." if fi else "A bedroom downstairs and beds for four on the loft."),
        ("ev", "Sähköauton lataus" if fi else "EV charging",
         "Latauspaikka pihassa, 10 € / 12 h." if fi else "Charger in the yard, €10 per 12 h."),
        ("pet", "Lemmikit tervetulleita" if fi else "Pets welcome",
         "Sohvalle löytyy suojat koiraystävää varten." if fi else "Sofa covers provided for your four-legged friend."),
    ]
    extras = (["Kaksi etätyöpistettä", "Kuivauskaappi", "Lukittava varasto pyörille ja kelkoille",
               "Suksien voiteluteline", "Terassi ja hiiligrilli", "Siivous sisältyy hintaan", "Ilmainen WiFi"]
              if fi else
              ["Two remote-work desks", "Drying cabinet", "Lockable storage for bikes and snowmobiles",
               "Ski waxing stand", "Terrace and charcoal grill", "Cleaning included", "Free WiFi"])
    feat_html = "".join(
        f'<div class="feature"><span class="feature-icon">{icon(i)}</span><div><strong>{a}</strong><span>{b}</span></div></div>'
        for i, a, b in features)
    extras_html = "".join(f"<li>{e}</li>" for e in extras)

    summer_card = f'''<a class="season" data-season="summer" href="{href(lang, "summer", lang)}" style="background-image:url('{p}assets/img/bikepark-800.jpg')">
        <div class="season-copy"><span class="pill">{"Kesä & syksy" if fi else "Summer & autumn"}</span>
        <h3>{"Polkuja, tuntureita ja yötöntä yötä" if fi else "Trails, fells and the midnight sun"}</h3>
        <p>{"Bikepark, vaellus, ruska ja kesäillan sauna." if fi else "Bike park, hiking, autumn colours and a summer-night sauna."}</p>
        <span class="more">{"Tutustu kesään" if fi else "Discover summer"} →</span></div></a>'''
    winter_card = f'''<a class="season" data-season="winter" href="{href(lang, "winter", lang)}" style="background-image:url('{p}assets/img/revot_3-800.jpg')">
        <div class="season-copy"><span class="pill">{"Talvi" if fi else "Winter"}</span>
        <h3>{"Rinteet, ladut ja revontulet" if fi else "Slopes, ski tracks and northern lights"}</h3>
        <p>{"Laskettelua, hiihtoa ja kaamoksen sinisiä hetkiä." if fi else "Downhill, cross-country skiing and the blue hours of polar night."}</p>
        <span class="more">{"Tutustu talveen" if fi else "Discover winter"} →</span></div></a>'''

    gallery = [("yllas-kajo-32", "Olohuone ja takka" if fi else "Living room with fireplace", "wide"),
               ("yllas-kajo-28", "Keittiö ja ruokapöytä" if fi else "Kitchen and dining table", ""),
               ("yllas-kajo-6", "Makuuhuone" if fi else "Bedroom", ""),
               ("yllas-kajo-8", "Sauna" if fi else "Sauna", ""),
               ("kajo_valot", "Ylläs Kajo talvi-illassa" if fi else "Ylläs Kajo on a winter evening", "")]
    gal_html = "".join(
        f'<a class="{c}" href="{href(lang, "cabin", lang)}#galleria">{img(n, a, p, "-800")}</a>' for n, a, c in gallery)

    dist = [("1 km", "Gondoli, Ylläs Ski Resort" if fi else "Gondola, Ylläs Ski Resort"),
            ("1,3 km", "Ylläsjärven ravintolat ja palvelut" if fi else "Ylläsjärvi restaurants and services"),
            ("8 km", "Äkäslompolon kylä" if fi else "Äkäslompolo village"),
            ("37 km", "Kittilän lentokenttä" if fi else "Kittilä airport"),
            ("36 km", "Kolarin rautatieasema" if fi else "Kolari railway station")]
    dist_html = "".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in dist)

    return f'''{hero("Ylläs Kajo",
                 "Kodikas paritalohuoneisto rauhassa, mutta lähellä kaikkea: gondolille kilometri, ladut ja polut lähes ovelta, oma sauna ja takka." if fi else
                 "A cosy semi-detached cabin in a quiet spot, yet close to everything: 1 km to the gondola, trails almost from the door, a private sauna and fireplace.",
                 "yllas-kajo-11", p, pill="Ylläsjärvi · Lappi" if fi else "Ylläsjärvi · Finnish Lapland",
                 actions=actions, winter_image="drone_1")}
<main id="sisalto">
{trust_block(lang)}
<section aria-labelledby="features-title">
    <p class="eyebrow">{"Mökki lyhyesti" if fi else "At a glance"}</p>
    <h2 class="title" id="features-title">{"Kaikki mitä lomalla tarvitsee" if fi else "Everything you need for a great holiday"}</h2>
    <div class="features">{feat_html}</div>
    <ul class="extras">{extras_html}</ul>
</section>
<section aria-labelledby="seasons-title" style="padding-top:0">
    <p class="eyebrow">{"Milloin tulisit?" if fi else "When will you come?"}</p>
    <h2 class="title" id="seasons-title">{"Ylläs on upea ympäri vuoden" if fi else "Ylläs is beautiful all year round"}</h2>
    <div class="seasons" id="seasons">{summer_card}{winter_card}</div>
</section>
<section class="intro" aria-labelledby="intro-title">
    {img("yllas-kajo-36", "Ylläs Kajon mökkikirja ja avaimet pöydällä" if fi else "Ylläs Kajo welcome book and keys on the table", p, "-800")}
    <div>
        <p class="eyebrow">{"Tervetuloa" if fi else "Welcome"}</p>
        <h2 class="title" id="intro-title">{"Pohjoisen rauhaa" if fi else "The peace of the North"}</h2>
        <blockquote>{"Tämä mökki päätyi meille rakkaudesta pohjoisen rauhaan, tuntureihin ja hiljaisuuteen. Olemme varustelleet sen niin kuin itsellemme, jotta voit vain saapua, rentoutua ja antaa Lapin lumon viedä mukanaan." if fi else
        "We chose this cabin for our love of the peaceful North, the fells and the quiet. We have equipped it as if for ourselves, so you can simply arrive, unwind and let the magic of Lapland carry you away."}</blockquote>
        <p class="signature">– Riikka &amp; Valtteri</p>
    </div>
</section>
<section aria-labelledby="gallery-title" style="padding-top:0">
    <p class="eyebrow">{"Kuvat" if fi else "Photos"}</p>
    <h2 class="title" id="gallery-title">{"Tutustu Ylläs Kajoon" if fi else "Take a look inside"}</h2>
    <div class="gallery">{gal_html}</div>
    <a class="btn btn-line gallery-more" href="{href(lang, "cabin", lang)}#galleria">{"Katso kaikki kuvat" if fi else "See all photos"} →</a>
</section>
{reviews_block(lang, limit=6)}
<section aria-labelledby="loc-title">
    <p class="eyebrow">{"Sijainti" if fi else "Location"}</p>
    <h2 class="title" id="loc-title">{"Rauhallinen paikka Ylläsjärvellä" if fi else "A quiet spot in Ylläsjärvi"}</h2>
    <ul class="distances">{dist_html}</ul>
    <a class="btn btn-line" href="{MAP}" target="_blank" rel="noopener">{icon("pin")}{"Avaa kartalla" if fi else "View on map"}</a>
</section>
{cta_block(lang)}
</main>'''


def page_cabin(lang, p):
    fi = lang == "fi"
    spaces = [
        ("Nukkuminen" if fi else "Sleeping",
         ["Alakerran makuuhuone: parivuode" if fi else "Downstairs bedroom: double bed",
          "Parvi: 2 yhden hengen vuodetta ja vuodesohva" if fi else "Loft: 2 single beds and a sofa bed",
          "Yhteensä enintään 6 henkeä" if fi else "Up to 6 guests in total"]),
        ("Keittiö ja ruokailu" if fi else "Kitchen & dining",
         ["Täysin varusteltu keittiö" if fi else "Fully equipped kitchen",
          "Induktioliesi, uuni ja astianpesukone" if fi else "Induction hob, oven and dishwasher",
          "Jatkettava ruokapöytä 4–6 hengelle" if fi else "Extendable dining table for 4–6",
          "Kahvinkeitin ja vedenkeitin" if fi else "Coffee maker and kettle"]),
        ("Sauna ja kylpyhuone" if fi else "Sauna & bathroom",
         ["Kylpyhuone ja oma sauna" if fi else "Bathroom with private sauna",
          "Erillinen WC" if fi else "Separate toilet",
          "Pesukone" if fi else "Washing machine",
          "Kuivauskaappi eteisessä" if fi else "Drying cabinet by the entrance"]),
        ("Olohuone ja etätyö" if fi else "Living & remote work",
         ["Takka ja lattialämmitys" if fi else "Fireplace and underfloor heating",
          "Google TV / Chromecast ja nopea WiFi" if fi else "Google TV / Chromecast and fast WiFi",
          "Parvella kaksi työpistettä näytöin, näppäimistöin ja hiirin" if fi else "Two desks on the loft with monitors, keyboards and mice"]),
        ("Piha ja varasto" if fi else "Yard & storage",
         ["Oma terassi ja hiiligrilli" if fi else "Private terrace and charcoal grill",
          "Iso lukittava varasto pyörille ja moottorikelkoille" if fi else "Large lockable storage for bikes and snowmobiles",
          "Suksien voiteluteline ja kaksi pulkkaa" if fi else "Ski waxing stand and two sledges",
          "Puuvaja" if fi else "Woodshed"]),
        ("Saapuminen ja pysäköinti" if fi else "Arrival & parking",
         ["Itsenäinen sisäänkirjautuminen avainlaatikolla" if fi else "Self check-in with a key box",
          "Ilmainen pysäköinti kahdelle autolle" if fi else "Free parking for two cars",
          "Sähköauton lataus 10 € / 12 h" if fi else "EV charging €10 per 12 h"]),
    ]
    cards = "".join(f'<div class="fact-card"><h3>{h}</h3><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div>'
                    for h, items in spaces)
    groups = [
        ("Sisätilat" if fi else "Inside", [
            ("yllas-kajo-32", "Olohuone ja takka" if fi else "Living room and fireplace", "wide"),
            ("yllas-kajo-35", "Olohuone" if fi else "Living room", ""),
            ("yllas-kajo-30", "Keittiö" if fi else "Kitchen", ""),
            ("yllas-kajo-33", "Ruokapöytä" if fi else "Dining table", ""),
            ("yllas-kajo-6", "Makuuhuone" if fi else "Bedroom", ""),
            ("yllas-kajo-17", "Parven vuoteet" if fi else "Loft beds", ""),
            ("yllas-kajo-22", "Vuodesohva parvella" if fi else "Sofa bed on the loft", ""),
            ("yllas-kajo-21", "Etätyöpiste" if fi else "Remote-work desk", ""),
            ("yllas-kajo-8", "Sauna" if fi else "Sauna", ""),
        ]),
        ("Piha ja ympäristö" if fi else "Outside", [
            ("yllas-kajo-1", "Ylläs Kajo ja varasto kesällä" if fi else "Ylläs Kajo and storage in summer", "wide"),
            ("yllas-kajo-5", "Talo kesällä" if fi else "The house in summer", ""),
            ("yllas-kajo-2", "Lukittava varasto" if fi else "Lockable storage", ""),
            ("kajo_valot", "Talvi-ilta" if fi else "Winter evening", ""),
            ("revot_3", "Revontulet mökin yllä" if fi else "Northern lights above the cabin", ""),
        ]),
    ]
    gal = ""
    for h, items in groups:
        gal += f'<h3 style="margin:28px 0 12px;font-size:1.4rem">{h}</h3><div class="gallery">'
        gal += "".join(f'<a class="{c}" href="{p}assets/img/{n}.jpg">{img(n, a, p, "-800")}</a>' for n, a, c in items)
        gal += "</div>"
    return f'''{hero("Mökki" if fi else "The cabin",
                 "Noin 67 m² kodikasta tilaa kuudelle: sauna, takka, parvi ja kaikki mitä lomalla tarvitsee." if fi else
                 "Around 67 m² of cosy space for six: sauna, fireplace, a loft and everything you need for a holiday.",
                 "yllas-kajo-35", p, pill="Ylläs Kajo", short=True)}
<main id="sisalto">
<section aria-labelledby="spaces-title">
    <p class="eyebrow">{"Tilat ja varustelu" if fi else "Spaces & amenities"}</p>
    <h2 class="title" id="spaces-title">{"Varusteltu niin kuin itselle" if fi else "Equipped as if for ourselves"}</h2>
    <p class="lead">{"Siivous sisältyy hintaan, joten lomasi alkaa heti saapuessasi." if fi else "Cleaning is included, so your holiday starts the moment you arrive."}</p>
    <div class="facts">{cards}</div>
</section>
<section id="galleria" aria-labelledby="gal-title" style="padding-top:0">
    <p class="eyebrow">{"Galleria" if fi else "Gallery"}</p>
    <h2 class="title" id="gal-title">{"Kuvat" if fi else "Photos"}</h2>
    {gal}
</section>
{reviews_block(lang, tag="cabin")}
{cta_block(lang)}
</main>'''


def page_summer(lang, p):
    fi = lang == "fi"
    blocks = [
        ("bikepark", "Pyöräily" if fi else "Mountain biking",
         "Ylläksen bikepark valittiin Suomen parhaaksi vuosina 2024 ja 2025. Maastopolut alkavat lähes ovelta, ja pyörät mahtuvat lukittavaan varastoon yön ajaksi." if fi else
         "The Ylläs bike park was voted Finland's best in 2024 and 2025. Trails start almost from the door, and bikes stay safe overnight in the lockable storage.",
         ["Gondoli ja bikepark noin 1 km päässä" if fi else "Gondola and bike park about 1 km away",
          "Maastopolut ja sorareitit Ylläksen ympäri" if fi else "Singletrack and gravel routes around Ylläs",
          "Pyörävuokraamot Ylläsjärvellä ja Äkäslompolossa" if fi else "Bike rentals in Ylläsjärvi and Äkäslompolo"],
         ("https://yllasbikepark.fi/" if fi else "https://yllasbikepark.fi/en",
          "Tutustu Ylläs Bike Parkiin" if fi else "Visit Ylläs Bike Park")),
        ("yllas-kajo-11", "Vaellus ja tunturit" if fi else "Hiking & fells",
         "Pallas-Yllästunturin kansallispuiston polut, tunturihuiput ja kirkkaat järvet ovat lyhyen matkan päässä. Keskikesällä aurinko ei laske lainkaan." if fi else
         "The trails, summits and clear lakes of Pallas-Yllästunturi National Park are a short trip away. In midsummer the sun doesn't set at all.",
         ["Päiväretket Ylläksen huipulle ja ympäristön tuntureille" if fi else "Day hikes to the Ylläs summit and nearby fells",
          "Polkujuoksua ja retkiä koko perheelle" if fi else "Trail running and family-friendly walks",
          "Uinti ja melonta Ylläsjärvellä" if fi else "Swimming and paddling on Lake Ylläsjärvi"]),
        ("yllas-kajo-1", "Kesäillat mökillä" if fi else "Summer evenings at the cabin",
         "Lämmitä sauna, grillaa terassilla ja nauti valoisasta yöstä. Rauhallinen piha on täydellinen pitkien kesäiltojen viettoon." if fi else
         "Heat up the sauna, grill on the terrace and enjoy the bright night. The peaceful yard is perfect for long summer evenings.",
         ["Oma terassi ja hiiligrilli" if fi else "Private terrace and charcoal grill",
          "Sauna aina käytettävissä" if fi else "Private sauna whenever you like",
          "Lemmikit tervetulleita" if fi else "Pets welcome"]),
        ("tunturi_5", "Ruska" if fi else "Ruska – autumn colours",
         "Syyskuussa tunturit hehkuvat punaisena ja kultaisena. Ruska on yksi Lapin kauneimmista ajoista vaeltaa, marjastaa ja sienestää." if fi else
         "In September the fells glow red and gold. Ruska is one of the most beautiful times in Lapland for hiking and picking berries and mushrooms.",
         ["Ruskavaellukset kansallispuistossa" if fi else "Autumn hikes in the national park",
          "Marjastus ja sienestys" if fi else "Berry and mushroom picking",
          "Ensimmäiset revontulet jo elo–syyskuussa" if fi else "First northern lights as early as August–September"]),
        ("yllas-kajo-21", "Etätyötä tunturissa" if fi else "Work from the fells",
         "Parvella on kaksi täysin varusteltua työpistettä. Tee työpäivä ja lähde illaksi polulle – pidempi oleskelu on kesällä helppo järjestää." if fi else
         "The loft has two fully equipped desks. Work during the day and hit the trail in the evening – longer summer stays are easy to arrange.",
         ["Kaksi työpistettä näytöin" if fi else "Two desks with monitors",
          "Nopea WiFi" if fi else "Fast WiFi",
          "Kysy viikkohintaa" if fi else "Ask about weekly rates"]),
    ]
    html = ""
    for i, (im, h, txt, items, *link) in enumerate(blocks):
        flip = " flip" if i % 2 else ""
        more = ""
        if link:
            url, label = link[0]
            more = f'<a class="btn btn-line split-link" href="{url}" target="_blank" rel="noopener">{label} →</a>'
        html += f'''<section class="split{flip}">
    {img(im, h, p, "-800")}
    <div><h2>{h}</h2><p>{txt}</p><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul>{more}</div>
</section>'''
    return f'''{hero("Kesä &amp; syksy Ylläksellä" if fi else "Summer &amp; autumn in Ylläs",
                 "Yötön yö, Suomen paras bikepark ja tunturipolut – kaikki kilometrin säteellä mökistä." if fi else
                 "The midnight sun, Finland's best bike park and fell trails – all within a kilometre or so of the cabin.",
                 "bike_1", p, pill="Kesäkuu–syyskuu" if fi else "June–September", short=True,
                 actions=f'<a class="btn btn-dark" href="{href(lang, "book", lang)}">{icon("book")}{T[lang]["check_dates"]}</a>')}
<main id="sisalto">
<section aria-labelledby="summer-title" style="padding-bottom:32px">
    <p class="eyebrow">{"Kesä Ylläs Kajossa" if fi else "Summer at Ylläs Kajo"}</p>
    <h2 class="title" id="summer-title">{"Valoisia öitä ja vapaita polkuja" if fi else "Bright nights and quiet trails"}</h2>
    <p class="lead">{"Kesällä Ylläs on rauhallinen ja luonto on lähellä. Kesäkaudella mökissä on hyvin tilaa myös lyhyemmille lomille." if fi else
    "In summer Ylläs is peaceful and nature is right outside. There's plenty of availability for shorter breaks too."}</p>
</section>
{html}
{reviews_block(lang, tag="summer")}
{cta_block(lang)}
</main>'''


def page_winter(lang, p):
    fi = lang == "fi"
    blocks = [
        ("gondoli_1", "Laskettelu" if fi else "Downhill skiing",
         "Ylläs on yksi Suomen suurimmista hiihtokeskuksista. Gondolin ala-asemalle on mökiltä noin kilometri." if fi else
         "Ylläs is one of Finland's largest ski resorts. The gondola base station is about a kilometre from the cabin.",
         ["Ylläs Ski Resort Ylläsjärvi noin 1 km" if fi else "Ylläs Ski Resort Ylläsjärvi about 1 km",
          "Välinevuokraamot lähellä rinteitä" if fi else "Equipment rentals near the slopes",
          "Suksivarasto ja voiteluteline pihalla" if fi else "Ski storage and waxing stand in the yard"]),
        ("tunturi_1", "Hiihto" if fi else "Cross-country skiing",
         "Ylläksen laajat latuverkostot alkavat lähes ovelta: ladulle on alle puoli kilometriä. Latukahvilat palkitsevat matkalla." if fi else
         "The extensive Ylläs ski-track network starts almost at your door: the nearest track is under 500 m away. Trail cafés reward you along the way.",
         ["Latu alle 500 m päässä" if fi else "Ski track under 500 m away",
          "Talvipyöräreitit samoilta kulmilta" if fi else "Winter fat-bike routes nearby",
          "Kuivauskaappi märille varusteille" if fi else "Drying cabinet for wet gear"]),
        ("revot_3", "Revontulet ja kaamos" if fi else "Northern lights & polar night",
         "Kirkkaina öinä revontulet näkyvät suoraan pihalta. Joulukuun kaamoksessa päivät ovat sinisiä ja tunnelma on ainutlaatuinen." if fi else
         "On clear nights the aurora can be seen right from the yard. In December's polar night the days glow blue and the atmosphere is unique.",
         ["Pimeä, rauhallinen piha revontulien katseluun" if fi else "A dark, quiet yard for aurora watching",
          "Joulu ja uusivuosi Lapissa" if fi else "Christmas and New Year in Lapland",
          "Moottorikelkka- ja husky-safarit lähistöllä" if fi else "Snowmobile and husky safaris nearby"]),
        ("yllas-kajo-32", "Lämmin koti pakkasen jälkeen" if fi else "A warm home after the cold",
         "Takka, sauna ja lattialämmitys pitävät huolen, että −30 asteen päivän jälkeen on hyvä palata kotiin." if fi else
         "The fireplace, sauna and underfloor heating make coming home after a −30°C day a pleasure.",
         ["Takka ja polttopuut" if fi else "Fireplace and firewood",
          "Oma sauna" if fi else "Private sauna",
          "Sähköauton lataus pihassa" if fi else "EV charging in the yard"]),
    ]
    html = ""
    for i, (im, h, txt, items) in enumerate(blocks):
        flip = " flip" if i % 2 else ""
        html += f'''<section class="split{flip}">
    {img(im, h, p, "-800")}
    <div><h2>{h}</h2><p>{txt}</p><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></div>
</section>'''
    return f'''{hero("Talvi Ylläksellä" if fi else "Winter in Ylläs",
                 "Rinteet kilometrin päässä, latu lähes ovelta ja revontulet pihalla." if fi else
                 "Slopes a kilometre away, ski tracks almost from the door and northern lights in the yard.",
                 "tunturi_4", p, pill="Marraskuu–toukokuu" if fi else "November–May", short=True,
                 actions=f'<a class="btn btn-dark" href="{href(lang, "book", lang)}">{icon("book")}{T[lang]["check_dates"]}</a>')}
<main id="sisalto">
<section aria-labelledby="winter-title" style="padding-bottom:32px">
    <p class="eyebrow">{"Talvi Ylläs Kajossa" if fi else "Winter at Ylläs Kajo"}</p>
    <h2 class="title" id="winter-title">{"Lumen, valon ja hiljaisuuden aikaa" if fi else "A season of snow, light and silence"}</h2>
    <p class="lead">{"Kaamoksen sinisistä päivistä kevättalven aurinkoon – talvi on Ylläksellä pitkä ja monipuolinen." if fi else
    "From the blue days of polar night to the bright spring sun, winter in Ylläs is long and full of variety."}</p>
</section>
{html}
{reviews_block(lang, tag="winter")}
{cta_block(lang)}
</main>'''


def page_book(lang, p):
    t = T[lang]
    fi = lang == "fi"
    faq = [
        ("Miten Ylläs Kajoon pääsee?" if fi else "How do I get to Ylläs Kajo?",
         "Kittilän lentokentältä on 37 km ja Kolarin rautatieasemalta 36 km. Suosittelemme autoa; pihassa on ilmainen pysäköinti kahdelle autolle ja sähköauton latauspaikka." if fi else
         "Kittilä airport is 37 km away and Kolari railway station 36 km. We recommend a car; there is free parking for two cars and an EV charger in the yard."),
        ("Miten sisäänkirjautuminen toimii?" if fi else "How does check-in work?",
         "Sisäänkirjautuminen on klo 17 alkaen avainlaatikon avulla. Lähetämme tarkat saapumisohjeet ennen saapumistasi." if fi else
         "Self check-in from 5 pm with a key box. We'll send detailed arrival instructions before your stay."),
        ("Sisältyykö siivous hintaan?" if fi else "Is cleaning included?",
         "Kyllä, loppusiivous sisältyy hintaan." if fi else "Yes, final cleaning is included in the price."),
        ("Saako lemmikin ottaa mukaan?" if fi else "Can I bring a pet?",
         "Kyllä, lemmikit ovat tervetulleita erillisestä maksusta. Sohvalle löytyy suojat." if fi else
         "Yes, pets are welcome for an additional fee. Sofa covers are provided."),
        ("Sopiiko mökki lapsiperheille?" if fi else "Is the cabin suitable for families?",
         "Kyllä, kaikenikäiset lapset ovat tervetulleita, ja pihalla on kaksi pulkkaa. Huomaathan, että pinnasänkyä tai lisävuoteita ei ole saatavilla." if fi else
         "Yes, children of all ages are welcome and there are two sledges for the kids. Please note that cots and extra beds are not available."),
        ("Voiko mökillä tehdä etätöitä?" if fi else "Can I work remotely?",
         "Kyllä. Parvella on kaksi työpistettä näytöin, näppäimistöin ja hiirin, ja WiFi on nopea." if fi else
         "Yes. The loft has two desks with monitors, keyboards and mice, and the WiFi is fast."),
        ("Mihin pyörät tai sukset voi säilyttää?" if fi else "Where can I store bikes or skis?",
         "Pihalla on iso lukittava varasto pyörille ja moottorikelkoille sekä suksien voiteluteline." if fi else
         "There is a large lockable storage building in the yard for bikes and snowmobiles, plus a ski waxing stand."),
    ]
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)
    rules = (["Enintään 6 henkeä", "Hiljaisuus klo 22–07", "Juhlat ja tapahtumat kielletty",
              "Tupakointi kielletty", "Lemmikit sallittu lisämaksusta"] if fi else
             ["Maximum 6 guests", "Quiet hours 10 pm – 7 am", "No parties or events",
              "No smoking", "Pets allowed for a fee"])
    return f'''{hero("Varaa" if fi else "Book your stay",
                 "Valitse sinulle sopiva varauskanava tai kysy suoraan meiltä." if fi else
                 "Choose the booking site that suits you, or ask us directly.",
                 "tunturi_2", p, pill="Ylläs Kajo", short=True)}
<main id="sisalto">
<section aria-labelledby="channels-title">
    <p class="eyebrow">{"Varauskanavat" if fi else "Where to book"}</p>
    <h2 class="title" id="channels-title">{"Vapaat päivät ja hinnat" if fi else "Availability and prices"}</h2>
    <div class="channels">
        <a class="channel" href="{AIRBNB[lang]}" target="_blank" rel="noopener"><strong>Airbnb</strong><span>★ 5,0 · {"5 arviota" if fi else "5 reviews"}</span><span class="go">{"Varaa Airbnb:ssä" if fi else "Book on Airbnb"} →</span></a>
        <a class="channel" href="{BOOKING[lang]}" target="_blank" rel="noopener"><strong>Booking.com</strong><span>9,2 · {"9 arviota" if fi else "9 reviews"}</span><span class="go">{"Varaa Bookingissa" if fi else "Book on Booking.com"} →</span></a>
        <a class="channel" href="mailto:{EMAIL}?subject={t["mail_subject"].replace(" ", "%20")}"><strong>{"Kysy meiltä" if fi else "Ask us"}</strong><span>{EMAIL}</span><span class="go">{"Lähetä sähköpostia" if fi else "Send an email"} →</span></a>
    </div>
</section>
<section aria-labelledby="info-title" style="padding-top:0">
    <p class="eyebrow">{"Hyvä tietää" if fi else "Good to know"}</p>
    <h2 class="title" id="info-title">{"Saapuminen ja säännöt" if fi else "Arrival and house rules"}</h2>
    <div class="times">
        <div><span class="times-label">{"Saapuminen" if fi else "Check-in"}</span><span class="times-value">17:00</span></div>
        <div><span class="times-label">{"Lähtö" if fi else "Check-out"}</span><span class="times-value">11:00</span></div>
    </div>
    <ul class="extras">{"".join(f"<li>{r}</li>" for r in rules)}</ul>
</section>
<section aria-labelledby="faq-title" style="padding-top:0">
    <p class="eyebrow">{"Usein kysyttyä" if fi else "FAQ"}</p>
    <h2 class="title" id="faq-title">{"Kysymyksiä ja vastauksia" if fi else "Questions and answers"}</h2>
    <div class="faq faq-wrap">{faq_html}</div>
</section>
{cta_block(lang)}
</main>'''


META = {
    "home": {"fi": ("Ylläs Kajo – mökki Ylläsjärvellä, 1 km gondolille",
                    "Kodikas paritalohuoneisto kuudelle Ylläsjärvellä: oma sauna, takka, ladut ja polut ovelta, 1 km gondolille. Arvio 5,0 Airbnb:ssä."),
             "en": ("Ylläs Kajo – cabin in Ylläs, Lapland, 1 km from the gondola",
                    "A cosy cabin for six in Ylläsjärvi, Finnish Lapland: private sauna, fireplace, trails from the door, 1 km to the gondola. Rated 5.0 on Airbnb.")},
    "cabin": {"fi": ("Mökki ja varustelu | Ylläs Kajo", "Tilat, varustelu ja kuvat: makuuhuone ja parvi kuudelle, sauna, takka, etätyöpisteet ja lukittava varasto."),
              "en": ("The cabin | Ylläs Kajo", "Spaces, amenities and photos: bedroom and loft for six, sauna, fireplace, remote-work desks and lockable storage.")},
    "summer": {"fi": ("Kesä ja ruska Ylläksellä | Ylläs Kajo", "Kesäloma Ylläksellä: bikepark, vaellus, yötön yö ja ruska. Mökki 1 km gondolilta."),
               "en": ("Summer & autumn in Ylläs | Ylläs Kajo", "Summer in Ylläs, Lapland: bike park, hiking, the midnight sun and autumn colours. Cabin 1 km from the gondola.")},
    "winter": {"fi": ("Talvi Ylläksellä | Ylläs Kajo", "Laskettelu, hiihto ja revontulet: mökki 1 km gondolilta ja latu alle 500 m päässä."),
               "en": ("Winter in Ylläs | Ylläs Kajo", "Skiing and northern lights in Lapland: cabin 1 km from the gondola, ski tracks under 500 m away.")},
    "book": {"fi": ("Varaa | Ylläs Kajo", "Varaa Ylläs Kajo Airbnb:stä tai Booking.comista tai kysy suoraan majoittajilta."),
             "en": ("Book | Ylläs Kajo", "Book Ylläs Kajo on Airbnb or Booking.com, or ask the hosts directly.")},
}

BUILDERS = {"home": page_home, "cabin": page_cabin, "summer": page_summer, "winter": page_winter, "book": page_book}

SCRIPT = """<script>
(() => {
    // Vieritys: sivuston sisäinen linkki avaa sivun alusta, Takaisin/Eteenpäin (selain tai hiiri)
    // palauttaa kohdan, jossa oltiin. Toimii myös upotetussa esikatselussa, joka säilyttää vierityksen.
    const store = {
        get: k => { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
        set: (k, v) => { try { sessionStorage.setItem(k, v); } catch (e) {} },
        del: k => { try { sessionStorage.removeItem(k); } catch (e) {} },
    };
    const here = location.pathname;
    const fromLink = store.get('yk-top') === here;
    store.del('yk-top');
    const saved = store.get('yk-scroll:' + here);
    const target = location.hash ? null : (fromLink ? 0 : (saved !== null ? +saved : null));
    if (target !== null) {
        let userMoved = false;
        ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(e =>
            window.addEventListener(e, () => { userMoved = true; }, { once: true, passive: true }));
        const go = () => { if (!userMoved) window.scrollTo({ top: target, left: 0, behavior: 'instant' }); };
        go();
        window.addEventListener('load', () => [0, 100, 300, 700].forEach(ms => setTimeout(go, ms)));
    }
    document.addEventListener('click', e => {
        const a = e.target.closest('a[href]');
        if (!a || a.target === '_blank' || a.origin !== location.origin || a.hash) return;
        store.set('yk-top', a.pathname);
    });
    let t;
    window.addEventListener('scroll', () => {
        clearTimeout(t);
        t = setTimeout(() => store.set('yk-scroll:' + here, String(Math.round(window.scrollY))), 150);
    }, { passive: true });
    const bar = document.querySelector('.topbar');
    const hero = document.querySelector('.hero');
    const onScroll = () => bar.classList.toggle('solid', !hero || window.scrollY > hero.offsetHeight - 80);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    // Kausi: touko–syyskuussa nostetaan kesä, muuten talvi.
    const month = new Date().getMonth() + 1;
    const summer = month >= 5 && month <= 9;
    if (hero && hero.dataset.winter && !summer) hero.style.backgroundImage = `url('${hero.dataset.winter}')`;
    const seasons = document.getElementById('seasons');
    if (seasons && !summer) seasons.prepend(seasons.querySelector('[data-season="winter"]'));
})();
</script>"""


def render(key, lang):
    fi_name, en_name = PAGES[key]
    p = "" if lang == "fi" else "../"
    t = T[lang]
    title, desc = META[key][lang]
    other = "en" if lang == "fi" else "fi"
    url_fi = f"{SITE_URL}/{fi_name}".replace("/index.html", "/")
    url_en = f"{SITE_URL}/en/{en_name}".replace("/index.html", "/")
    canonical = url_fi if lang == "fi" else url_en
    toplinks = "".join(
        f'<a href="{href(lang, k, lang)}"{" aria-current=\"page\"" if k == key else ""}>{NAV[lang][k]}</a>'
        for k in ("cabin", "summer", "winter", "book"))
    dock = "".join(
        f'<a href="{href(lang, k, lang)}" class="{"dock-book" if k == "book" else ""}"'
        f'{" aria-current=\"page\"" if k == key and k != "book" else ""}>{icon(k, "")}<span>{DOCK[lang][k]}</span></a>'
        for k in ("home", "cabin", "summer", "winter", "book"))
    body = BUILDERS[key](lang, p)
    ld = ""
    if key == "home":
        ld = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"VacationRental","name":"Ylläs Kajo","description":"{escape(desc)}","url":"{canonical}","image":"{SITE_URL}/assets/img/og.jpg","address":{{"@type":"PostalAddress","addressLocality":"Ylläsjärvi","postalCode":"95980","addressCountry":"FI"}},"containsPlace":{{"@type":"Accommodation","occupancy":{{"@type":"QuantitativeValue","maxValue":6}}}},"aggregateRating":{{"@type":"AggregateRating","ratingValue":"5.0","bestRating":"5","ratingCount":"5"}}}}</script>'''
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="robots" content="noindex">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="fi" href="{url_fi}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="x-default" href="{url_en}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{SITE_URL}/assets/img/og.jpg">
<meta property="og:locale" content="{"fi_FI" if lang == "fi" else "en_GB"}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f6f3ee">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{p}assets/site.css">
{ld}
</head>
<body>
<a class="skip" href="#sisalto">{t["skip"]}</a>
<div class="topbar">
    <a class="brand" href="{href(lang, "home", lang)}">Ylläs Kajo</a>
    <nav class="toplinks" aria-label="{"Päävalikko" if lang == "fi" else "Main menu"}">{toplinks}</nav>
    <a class="lang" href="{href(other, key, lang)}" hreflang="{other}" lang="{other}" aria-label="{t["lang_switch_label"]}">{t["lang_switch"]}</a>
    <a class="btn btn-dark btn-book" href="{href(lang, "book", lang)}">{t["book_btn"]}</a>
</div>
<span class="draft-note">{t["draft"]}</span>
{body}
<footer class="site-footer">
    <h2>Ylläs Kajo</h2>
    <p>{t["footer_tag"]}</p>
    <div class="social">
        <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram", "")}</a>
        <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{icon("facebook", "")}</a>
    </div>
    <p>{t["footer_hosts"]} · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p>Ylläsjärvi, {"Lappi" if lang == "fi" else "Finnish Lapland"}</p>
</footer>
<nav class="dock" aria-label="{"Sivut" if lang == "fi" else "Pages"}">{dock}</nav>
{SCRIPT}
</body>
</html>
'''


def main():
    (ROOT / "en").mkdir(exist_ok=True)
    for key, (fi_name, en_name) in PAGES.items():
        (ROOT / fi_name).write_text(render(key, "fi"), encoding="utf-8")
        (ROOT / "en" / en_name).write_text(render(key, "en"), encoding="utf-8")
    print("Built", len(PAGES) * 2, "pages")


if __name__ == "__main__":
    main()
