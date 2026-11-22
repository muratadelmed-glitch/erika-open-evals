# Public copy of the ERIKA world generator (pilot/vucut/dunya.py in the private repository).
# Generation code is byte-for-byte the same apart from the seed check and imports; `verify.py` checks that the
# copy reproduces the private generator on published reference seeds. Comments are in Turkish (original source).
"""İlkel dünya V0: gizli türler, çok tepeli özellik üreticileri, bireyler ve karşılaşma akışı. KESIFSEL / DEV_ONLY.

Plan: docs/eidra/plan/2026-11-21_DIJITAL_VUCUT_DUNYA_PLANI.md §2.

Hazır bilgi yok: tür, renk adı ve aile bu modülün GİZLİ kayıtlarıdır. ERIKA'ya yalnız `vucut.py`'nin ürettiği ham
duyu sayıları gider; gizli kayıtları yalnız `olcum.py` okur (sızıntı testi: testler/test_vucut.py).

Yapı (V0a; 2B hareket V0b'ye kaldı, plan §2 "alan" maddesi henüz yok):
  aile      aynı şekil + akraba renkler (aile başına 4 renk). Aile içinde iki tür.
  tür       kendi dokusu ve sesi; renkleri ailenin 4 renginden 3'ü, olasılıklar Dirichlet'ten (çok tepeli).
  gizli     "olası ama gösterilmemiş" varyant (hayal ölçümü): bazı türlerin, kardeş türün sahip olduğu bir rengi
  varyant   küçük olasılıkla vardır; o renkli bireyler akışta açılış anına kadar hiç görünmez.
  birey     tür örneği: sabit rengi, şekil üzerinde kişisel iz (birkaç piksel) ve doku/ses sapması vardır
            (epizodik bellek ölçümü M10: "o elma sarıydı").
  emekli    bazı bireyler yalnız akışın başında görünür (uzun süreli bellek ölçümü).
  sonuç     yenince enerji değişimi; tür başına iki değerli dağılım (her yemede yeniden çekilir).
  değişim   (isteğe bağlı, M6/M7) `degisim` kesrinde bir türün renk kuralı değişir: o türün eski bireyleri akıştan
            çıkar, başka bir ailenin renklerini taşıyan yeni bireyleri gelir. Varsayılan (None) dünya bit eşittir.
  koku/tat  (isteğe bağlı, `KULLANICI_KARARI_2026-11-22_TAT_VE_KOKU`; plan `2026-11-22_TAT_KOKU_PLANI.md`) tür kokusu
            ve tadı + birey sapması. Ayrı RNG'den; açık değilse hiçbir çekim yapılmaz (varsayılan dünya bit eşit).
  tek duyu  (isteğe bağlı, H-DB (b), plan §15) `tek_duyu_orani` kadar akış bireyi yalnız göz kanalıyla karşılanır:
            bakılır, dokunulmaz, dinlenmez. Atama ayrı bir RNG'den gelir ve (tür, emekli, yeni kural) katmanı içinde
            dengelenir; akış, bireyler ve duyu gürültüsü varsayılan dünyayla aynıdır (0 = bit eşit).
"""
import dataclasses
from dataclasses import dataclass

import numpy as np


GOZ = 5                      # göz yaması kenarı (piksel)
DOKU_BOYUT = 6
SES_BANT = 8
KOKU_BOYUT = 10
TAT_BOYUT = 5
SONUC_DEGERLERI = (-1.0, 0.0, 1.0, 2.0)
_TUZ = 0x5EED_0B0D


@dataclass(frozen=True)
class DunyaAyar:
    """Adlı dünya ayarları (ayar çalışması sonra; V0 değerleri koşudan önce yazıldı)."""
    n_aile: int = 3
    tur_aile: int = 2                 # aile başına tür
    aile_renk: int = 4                # aile başına akraba renk; tür bunlardan aile_renk − 1 tanesini taşır
    gizli_aile: int = 2               # ilk bu kadar ailedeki her türün bir gizli (olası, açılışa kadar gösterilmeyen) rengi var
    gizli_olasilik: float = 0.15      # gizli rengin dünyadaki olasılığı
    renk_alfa: float = 1.5            # tür renk olasılıkları Dirichlet(α) (çok tepeli, eşit değil)
    birey: int = 10                   # tür başına akış bireyi
    test_birey: int = 4               # tür başına yalnız ölçümde kullanılan (akışta hiç görülmeyen) birey
    iz_piksel: int = 3                # bireyin şekil üzerindeki kişisel izi (çevrilen piksel)
    iz_sapma: float = 0.08            # bireyin doku/ses sapması (std)
    emekli_orani: float = 0.3         # tür başına bu oranda birey yalnız akışın başında görünür
    emeklilik: float = 0.3            # emekliler bu kesirden sonra görünmez
    acilis: float = 0.7               # gizli renkli bireyler bu kesirde akışa girer
    karsilasma: int = 3000            # akış uzunluğu (karşılaşma)
    degisim: float | None = None      # M6/M7: bu kesirde `degisen_tur` türünün renk kuralı değişir (None = yok)
    kardes_vurgu: float | None = None # M3b: türün gizli renginin KARDEŞ türdeki görünür payı (None = Dirichlet'ten);
                                      # aynı tohumla iki değer = "gerçek dünya istatistiği" manipülasyonu
    tek_duyu_orani: float = 0.0       # H-DB (b): yalnız gözle karşılanan akış bireylerinin katman içi payı
    koku: bool = False                # burun: nesne oradayken (karanlıkta da) alınır
    tat: bool = False                 # dil: yalnız yerken (akıştaki karşılaşmada) alınır
    koku_aile: float = 0.0            # tür kokusunda aile ortak kokusunun payı (KULLANICI_KARARI_..._TAMAMLAMA_VE_TAT_SONUC)
    tat_sonuc: float = 0.0            # tadın, yemenin sonucuna (enerji değişimi) göre kayma ağırlığı (aynı karar)

    def __post_init__(self):
        if not (self.n_aile >= 2 and self.tur_aile == 2 and self.aile_renk >= 3):
            raise ValueError("n_aile ≥ 2, tur_aile = 2 (V0 kardeş yapısı), aile_renk ≥ 3")
        if not (0 <= self.gizli_aile <= self.n_aile and 0.0 < self.gizli_olasilik < 0.5):
            raise ValueError("gizli_aile ∈ [0, n_aile], gizli_olasilik ∈ (0, 0.5)")
        if not (0.0 < self.emeklilik < self.acilis < 1.0 and 0.0 <= self.emekli_orani < 1.0):
            raise ValueError("0 < emeklilik < acilis < 1, emekli_orani ∈ [0, 1)")
        if self.degisim is not None and not (self.acilis < self.degisim < 1.0 and self.gizli_aile < self.n_aile):
            raise ValueError("acilis < degisim < 1 ve değişen tür gizli varyantsız bir ailede olmalı")
        if self.kardes_vurgu is not None and not (0.0 < self.kardes_vurgu < 1.0):
            raise ValueError("kardes_vurgu ∈ (0, 1) ya da None")
        if not (0.0 <= self.koku_aile <= 1.0 and self.tat_sonuc >= 0.0):
            raise ValueError("koku_aile ∈ [0, 1], tat_sonuc ≥ 0")
        if (self.koku_aile > 0.0 and not self.koku) or (self.tat_sonuc > 0.0 and not self.tat):
            raise ValueError("koku_aile koku, tat_sonuc tat ister")
        if not (0.0 <= self.tek_duyu_orani <= 0.5):     # Codex 271.1: yalnız sınanan aralık; 1'e yakın oranda
            raise ValueError("tek_duyu_orani ∈ [0, 0.5]")  # katman yuvarlaması bütün akışı işaretleyebilir
        if self.birey < 3 or self.test_birey < 1 or self.karsilasma < 100 or self.iz_piksel < 1:
            raise ValueError("birey ≥ 3, test_birey ≥ 1, karsilasma ≥ 100, iz_piksel ≥ 1")

    @property
    def n_tur(self):
        return self.n_aile * self.tur_aile

    @property
    def degisen_tur(self):
        """Kuralı değişen tür: son ailenin ilk türü (gizli varyantı yok)."""
        return (self.n_aile - 1) * self.tur_aile

    @property
    def n_renk(self):
        return self.n_aile * self.aile_renk


def dev_seed(seed):
    """Public copy: any non-negative integer seed is accepted. (The private ERIKA repository restricts which
    seeds its own experiments may use; that policy is about our model's exposure, not about this generator.)"""
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError(f"seed must be a non-negative int: {seed!r}")
    return seed


def _palet(n, r):
    """n doygun renk, renk çemberinde eşit aralıklı (başlangıç açısı rastgele). Gri yok."""
    h0 = r.uniform(0.0, 1.0)
    out = []
    for i in range(n):
        h = (h0 + i / n) % 1.0
        k = (np.arange(3) * (1.0 / 3.0) + h) % 1.0          # basit HSV→RGB (s = 1, v = 0.9) üç dalga
        rgb = 0.9 * np.clip(np.abs(k * 6.0 - 3.0) - 1.0, 0.0, 1.0)
        out.append(rgb)
    return np.array(out)


def _sekiller(n, r, en_az_fark=8):
    """n ikili 5×5 desen (10–14 açık piksel), ikişer ikişer Hamming ≥ en_az_fark."""
    out = []
    while len(out) < n:
        m = np.zeros(GOZ * GOZ, bool)
        m[r.choice(GOZ * GOZ, int(r.integers(10, 15)), replace=False)] = True
        if all(int((m != o).sum()) >= en_az_fark for o in out):
            out.append(m)
    return np.array(out)


@dataclass
class Birey:
    no: int
    tur: int
    renk: int
    maske: np.ndarray          # (25,) bool: aile şekli + kişisel iz
    doku: np.ndarray           # (6,)
    ses: np.ndarray            # (8,)
    gizli: bool                # rengi türün gizli varyantı mı
    emekli: bool
    test: bool                 # yalnız ölçüm bireyi (akışta yok)
    yeni_kural: bool = False   # değişimden sonra gelen birey (yalnız degisim açıkken)
    tek_duyu: bool = False     # H-DB (b): akışta yalnız gözle karşılanır (yalnız tek_duyu_orani > 0 iken)
    koku: np.ndarray | None = None   # (10,) yalnız DunyaAyar.koku açıkken
    tat: np.ndarray | None = None    # (5,) yalnız DunyaAyar.tat açıkken


class Dunya:
    """Belirlenimci dünya. Bütün öznitelikler GİZLİ kayıttır (yalnız ölçüm ve duyu organları okur)."""

    def __init__(self, seed, ayar=None):
        self.seed = dev_seed(seed)
        self.ayar = a = ayar or DunyaAyar()
        r = np.random.default_rng([_TUZ, seed])
        self.palet = _palet(a.n_renk, r)
        self.aile_sekil = _sekiller(a.n_aile, r)
        self.tur_aile = np.repeat(np.arange(a.n_aile), a.tur_aile)
        self.tur_doku = r.uniform(0.0, 1.0, (a.n_tur, DOKU_BOYUT))
        self.tur_ses = r.uniform(0.0, 1.0, (a.n_tur, SES_BANT))
        # renk dağılımları: aile renkleri [4f, 4f+4); tür 2f+0 → ilk 3, tür 2f+1 → son 3 (ortak 2 renk)
        self.tur_renk_p = np.zeros((a.n_tur, a.n_renk))
        self.gizli_renk = np.full(a.n_tur, -1)
        for t in range(a.n_tur):
            f, kardes_sira = divmod(t, a.tur_aile)
            aile = np.arange(f * a.aile_renk, (f + 1) * a.aile_renk)
            destek = aile[:-1] if kardes_sira == 0 else aile[1:]
            p = r.dirichlet(np.full(len(destek), a.renk_alfa))
            if f < a.gizli_aile:
                g = aile[-1] if kardes_sira == 0 else aile[0]        # kardeşte olan, kendisinde gösterilmeyen renk
                self.gizli_renk[t] = g
                self.tur_renk_p[t, destek] = (1.0 - a.gizli_olasilik) * p
                self.tur_renk_p[t, g] = a.gizli_olasilik
            else:
                self.tur_renk_p[t, destek] = p
        if a.kardes_vurgu is not None:                 # M3b: kardeşin, bu türün gizli rengine verdiği görünür pay
            for t in range(a.n_tur):
                g = int(self.gizli_renk[t])
                if g < 0:
                    continue
                k = t + 1 if t % a.tur_aile == 0 else t - 1
                kendi_gizli = int(self.gizli_renk[k])
                gorunur = [c for c in np.flatnonzero(self.tur_renk_p[k] > 0) if c != kendi_gizli]
                kutle = float(self.tur_renk_p[k, gorunur].sum())
                digerleri = [c for c in gorunur if c != g]
                eski = self.tur_renk_p[k, digerleri].copy()
                self.tur_renk_p[k, g] = a.kardes_vurgu * kutle
                self.tur_renk_p[k, digerleri] = eski / eski.sum() * (1.0 - a.kardes_vurgu) * kutle
        sonuc_p = np.zeros((a.n_tur, len(SONUC_DEGERLERI)))
        for t in range(a.n_tur):
            iki = r.choice(len(SONUC_DEGERLERI), 2, replace=False)
            sonuc_p[t, iki] = r.dirichlet([2.0, 2.0])
        self.tur_sonuc_p = sonuc_p
        self.tur_olasilik = r.dirichlet(np.full(a.n_tur, 6.0))
        self.bireyler = []
        for t in range(a.n_tur):
            for k in range(a.birey + a.test_birey):
                test = k >= a.birey
                renk = int(r.choice(a.n_renk, p=self.tur_renk_p[t]))
                if not test and k == 0 and self.gizli_renk[t] >= 0:
                    renk = int(self.gizli_renk[t])                   # her gizli türde en az bir gizli renkli birey
                gizli = renk == self.gizli_renk[t]
                emekli = (not test and not gizli and 0 < k <= int(round(a.emekli_orani * a.birey)))
                m = self.aile_sekil[self.tur_aile[t]].copy()
                cevir = r.choice(GOZ * GOZ, a.iz_piksel, replace=False)
                m[cevir] = ~m[cevir]
                self.bireyler.append(Birey(len(self.bireyler), t, renk, m,
                                           np.clip(self.tur_doku[t] + r.normal(0.0, a.iz_sapma, DOKU_BOYUT), 0, 1),
                                           np.clip(self.tur_ses[t] + r.normal(0.0, a.iz_sapma, SES_BANT), 0, 1),
                                           bool(gizli), bool(emekli), bool(test)))
        self.degisen_renk_p = None
        if a.degisim is not None:                      # yer tutucular akıştan önce; öznitelikler akıştan sonra çekilir
            for _ in range(a.birey):                   # (varsayılan dünyanın RNG akışı değişmez)
                self.bireyler.append(Birey(len(self.bireyler), a.degisen_tur, -1, None, None, None, False, False,
                                           False, True))
        self.akis = self._akis(r)
        if a.degisim is not None:
            t = a.degisen_tur
            f2 = (self.tur_aile[t] + 1) % a.n_aile
            yeni = np.arange(f2 * a.aile_renk, f2 * a.aile_renk + a.aile_renk - 1)
            self.degisen_renk_p = np.zeros(a.n_renk)
            self.degisen_renk_p[yeni] = r.dirichlet(np.full(len(yeni), a.renk_alfa))
            for b in self.bireyler:
                if b.yeni_kural:
                    b.renk = int(r.choice(a.n_renk, p=self.degisen_renk_p))
                    m = self.aile_sekil[self.tur_aile[t]].copy()
                    cevir = r.choice(GOZ * GOZ, a.iz_piksel, replace=False)
                    m[cevir] = ~m[cevir]
                    b.maske = m
                    b.doku = np.clip(self.tur_doku[t] + r.normal(0.0, a.iz_sapma, DOKU_BOYUT), 0, 1)
                    b.ses = np.clip(self.tur_ses[t] + r.normal(0.0, a.iz_sapma, SES_BANT), 0, 1)
        if a.tek_duyu_orani > 0.0:                     # ayrı RNG: yukarıdaki bütün çekimler varsayılanla aynı
            r2 = np.random.default_rng([_TUZ, seed, 0x7D])
            katman = {}
            for b in self.bireyler:
                if not b.test:
                    katman.setdefault((b.tur, b.emekli, b.yeni_kural), []).append(b.no)
            for anahtar in sorted(katman):
                uyeler = katman[anahtar]
                k = int(round(a.tek_duyu_orani * len(uyeler)))
                for no in r2.choice(uyeler, k, replace=False):
                    self.bireyler[int(no)].tek_duyu = True
        self.tur_koku = self.tur_tat = None
        self.sonuc_tat = None                          # sonuç değeri başına tat kayması (yalnız tat_sonuc > 0)
        if a.tat_sonuc > 0.0:
            self.sonuc_tat = np.random.default_rng([_TUZ, seed, 0xC0C, 5]).uniform(
                -0.5, 0.5, (len(SONUC_DEGERLERI), TAT_BOYUT))
        if a.koku or a.tat:                            # ayrı RNG; koku ve tat değerleri öteki bayraktan bağımsız
            r3 = np.random.default_rng([_TUZ, seed, 0xC0C])
            tur_koku = r3.uniform(0.0, 1.0, (a.n_tur, KOKU_BOYUT))
            tur_tat = r3.uniform(0.0, 1.0, (a.n_tur, TAT_BOYUT))
            if a.koku_aile > 0.0:                      # aile ortak kokusu (ayrı RNG; 0'da hiçbir şey değişmez)
                aile_koku = np.random.default_rng([_TUZ, seed, 0xC0C, 4]).uniform(0.0, 1.0, (a.n_aile, KOKU_BOYUT))
                tur_koku = (1.0 - a.koku_aile) * tur_koku + a.koku_aile * aile_koku[self.tur_aile]
            for b in self.bireyler:
                k = np.clip(tur_koku[b.tur] + r3.normal(0.0, a.iz_sapma, KOKU_BOYUT), 0, 1)
                t = np.clip(tur_tat[b.tur] + r3.normal(0.0, a.iz_sapma, TAT_BOYUT), 0, 1)
                b.koku, b.tat = (k if a.koku else None), (t if a.tat else None)
            self.tur_koku = tur_koku if a.koku else None
            self.tur_tat = tur_tat if a.tat else None

    def _akis(self, r):
        a = self.ayar
        n_em, n_ac = int(a.emeklilik * a.karsilasma), int(a.acilis * a.karsilasma)
        n_dg = None if a.degisim is None else int(a.degisim * a.karsilasma)
        akis = np.empty(a.karsilasma, int)
        for i in range(a.karsilasma):
            t = int(r.choice(a.n_tur, p=self.tur_olasilik))
            sonra = n_dg is not None and i >= n_dg and t == a.degisen_tur
            aday = [b.no for b in self.bireyler if b.tur == t and not b.test
                    and not (b.emekli and i >= n_em) and not (b.gizli and i < n_ac)
                    and b.yeni_kural == sonra]
            akis[i] = int(r.choice(aday))
        return akis

    def renk_p(self, tur, adim):
        """Türün o andaki renk dağılımı (değişimden sonra değişen türde yeni kural)."""
        if self.degisen_renk_p is not None and tur == self.ayar.degisen_tur and adim >= self.degisim_adimi():
            return self.degisen_renk_p
        return self.tur_renk_p[tur]

    def degisim_adimi(self):
        return None if self.ayar.degisim is None else int(self.ayar.degisim * self.ayar.karsilasma)

    # ---- gizli kayıt sorguları (yalnız ölçüm) ----
    def birey(self, no):
        return self.bireyler[no]

    def test_bireyleri(self, tur=None):
        return [b for b in self.bireyler if b.test and (tur is None or b.tur == tur)]

    def gosterilen_renkler(self, tur, adim):
        """Akışta [0, adim) içinde bu türde görülmüş renkler (kümesi)."""
        return {self.bireyler[n].renk for n in self.akis[:adim] if self.bireyler[n].tur == tur}

    def acilis_adimi(self):
        return int(self.ayar.acilis * self.ayar.karsilasma)

    def emeklilik_adimi(self):
        return int(self.ayar.emeklilik * self.ayar.karsilasma)

    def sozluk(self):
        return {"seed": self.seed, "ayar": dataclasses.asdict(self.ayar)}
