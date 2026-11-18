# Ylläs Kajo – markkinointisivusto

Kaksikielinen (fi/en) staattinen sivusto GitHub Pagesiin. Tyyli noudattaa Ylläs Kajon mökkikirjaa.

- Suomenkieliset sivut: juuri (`index.html`, `mokki.html`, `kesa.html`, `talvi.html`, `varaa.html`)
- Englanninkieliset sivut: `en/`
- Tekstit, palautteet ja linkit: `tools/build.py`
- Tyylit: `assets/site.css`, kuvat: `assets/img/`

## Muokkaus

1. Muokkaa sisältöä tiedostossa `tools/build.py`.
2. Aja `python3 tools/build.py` – sivut päivittyvät.
3. Commitoi ja pushaa.

Luonnosvaiheessa sivuilla on `noindex` ja LUONNOS-merkki; ne poistetaan ennen julkaisua.
