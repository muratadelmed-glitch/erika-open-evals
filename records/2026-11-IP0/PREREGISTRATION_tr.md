# İP0 ön kaydı: kilitli bellek sınavı (KİLİT ADAYI, henüz kilitli değil)

- **Statü:** geçerli statü yalnız §2 sonundaki ip0 kod bloğundaki `statu:` satırıdır (bu satır değişmez; statü orada okunur).
  - **Kilitleme:** bağımsız denetim (Claude 2; 27 Kasım'dan sonra Codex) temiz çıkınca kilit commit'i atılır. Bu commit yalnız bu dosyayı ve içinde yalnız `statu: KILIT_ADAYI` → `statu: KILITLI` satırını değiştirir. SHA'sı iletişim dalına yazılır.
  - **Kilit commit'i tanımı:** `statu: KILITLI` satırını ekleyen en eski commit (`ip0.kilit_denetle`; Claude 2 318 bulgu 1). Kilitten sonra bu dosyaya yapılan her değişiklik (boş satır dahil) koşuyu reddettirir.
  - **Kod zorlaması** (`pilot/vucut/ip0.py::kilit_denetle`; Claude 2 316 bulgu 1–2):
    - `statu: KILITLI` değilse değerlendirme dünyası açılmaz.
    - Kilit commit'inden sonra ölçüm kodu (`pilot/`, yalnız `pilot/substrat`, `pilot/sonuclar`, `pilot/testler` hariç; `requirements.txt`) değişmişse açılmaz.
    - Kapı `Dunya` kurulurken (RNG'den önce) de çalışır.
  - Kilitten sonra bu dosya ve ölçüm kodu değişmez. Değişirse koşu geçersizdir ve yeni ön kayıt gerekir.
- **Kararlar:**
  - `KULLANICI_KARARI_2026-11-23_SORULARA_YANITLAR.md` (madde 1–3, 7);
  - `..._2026-11-21_FON_KONUSU_ERIKA.md` §2 (bellek doğruluğu);
  - `..._2026-11-22_NORAL_ILETISIM_VE_FON_ZAMANI.md` madde 3.
- **Taslak ve gerekçe:** `docs/eidra/plan/2026-11-23_IP0_KILITLI_BELLEK_OLCUMU_ON_KAYIT_TASLAGI.md`.

## 1. Ne ölçülüyor?

ERIKA'nın bugünkü (olasılıksal, nöral olmayan) son hâlinin bellek doğruluğu, **hiç görülmemiş** dünyalarda, bir kez.

- Bu, nöral ERIKA'nın sonucu değildir. Raporda bu açıkça yazılır.
- Ölçülen öğrenen: `erika_son_bol_tam_kar_ebk`.
- Referans kollar: `epizodik` ve `yavas`. Aynı akış, aynı ölçüm, bütçe eşli.

## 2. Düzen

- **Dünyalar:** değerlendirme bölümü, 20 dünya: 312001–312020.
  - 312000 karantinada.
  - Bu dünyalar vücut üreteciyle hiç kurulmadı. Testler bu bölümü üretmez (`DegerlendirmeErisimTestleri`).
- **Dünya ayarı:** orta zor, tat + koku.
  - Aynı JSON'da eşli temel koşul (tat ve koku kapalı) da üretilir; temel koşul ikincildir.
- **Vücut:** keskin (`--keskinlik=2`; kullanıcı kararı madde 2).
- **Koşu:** tam komut aşağıda; depo kökünden, kilit commit'inde, temiz ağaçta.

  ```
  cd pilot && python3 -B -m vucut.ip0 kos --cikti ../kosu/ip0_degerlendirme --is 4 \
    --dunyalar <bloktaki dünyalar> --kollar <bloktaki kollar> --bayraklar="<bloktaki bayraklar>" \
    --on_kayit ../docs/eidra/basvuru/IP0_ON_KAYIT.md
  ```

  - Her dünya ayrı süreç; `PYTHONHASHSEED=0`, iş parçacığı 1.
  - **Çıktı dizini** depo kökündeki yok sayılan `kosu/` altında, böylece ağaç koşu sırasında kirlenmez (316 bulgu 3; `ip0.cikti_denetle` depo içinde yok sayılmayan dizini reddeder).
  - Arşive kopya (`pilot/sonuclar/`, açık depo) koşu bittikten sonra ayrı commit'tir.

```ip0
statu: KILITLI
dunyalar: 312001 312002 312003 312004 312005 312006 312007 312008 312009 312010 312011 312012 312013 312014 312015 312016 312017 312018 312019 312020
kollar: epizodik,yavas,erika_son_bol_tam_kar_ebk
bayraklar: --birey=30 --iz_piksel=1 --iz_sapma=0.04 --ic --koku --tat --koku_aile=0.5 --tat_sonuc=0.5 --keskinlik=2 --unutma
```

## 3. Ölçütler

Son nokta (karşılaşma 3000); tanımlar `pilot/vucut/olcum.py` ve `ip0.py rapor`.

| # | Ölçüt | Alan | Rol |
|---|---|---|---|
| B1 | Kısa süreli renk belleği | `m10_kisa_ornek_dogruluk` | **birincil** |
| B2 | Uzun süreli renk belleği | `m10_uzun_ornek_dogruluk` | **birincil** |
| B3 | Karanlıkta şekil tamamlama, kısa / uzun | `m4_sekil_kisa_tam`, `m4_sekil_uzun_tam` | ikincil |
| B4 | Görülmemiş bireyde şekil | `m4_sekil_genel_tam` | ikincil (genelleme; %90 hedefinin parçası değil) |
| B8 | Unutma, son nokta ve en kötü an | `olcum.unutma` | ikincil |
| — | Tavan (ideal gözlemci) | `tavan.m10_*` | betimsel |

## 4. Karar kuralı (kullanıcı kararı madde 1: "ortalama yeter")

- **PASS:** tat + koku koşulunda, `erika_son_bol_tam_kar_ebk` için 20 dünyanın ortalaması **B1 ≥ 0,90 ve B2 ≥ 0,90**.
  - Biri tutmazsa sonuç `FAIL` olur ve gerçek sayılar yazılır.
- **Karar komutu** (tam; `--alt` ve `--en_kotu` kullanılmaz; 316 bulgu 4):
  `cd pilot && python3 -B -m vucut.ip0 rapor ../kosu/ip0_degerlendirme --kol erika_son_bol_tam_kar_ebk --kosul tat+koku --esik 0.90 --on_kayit ../docs/eidra/basvuru/IP0_ON_KAYIT.md --json ../kosu/ip0_degerlendirme_rapor.json`
  - **Beklenen dünyalar** bu ön kayıttan alınır. MANIFEST yoksa (koşu yarıda kaldıysa) ya da ön kayıtla uyuşmuyorsa karar `INCONCLUSIVE` olur (318 bulgu 3).
  - **Rapor JSON'u** çıktı dizininin dışına yazılır. Rapor yalnız adı sayı olan dünya dosyalarını okur, bu yüzden aynı komut tekrar koşulabilir (318 bulgu 2).
- **Eksik ya da çöken dünya:**
  - 20 dünyanın hepsi çıkış 0 vermeli ve B1/B2 dolu olmalı.
  - Değilse sonuç `INCONCLUSIVE` olur; rapor aracı bu durumda karar üretmez.
  - Yeniden koşu yapılmaz. Hata yeni ön kayıtla (yeni dünyalar) ele alınır.
- **Her durumda raporlananlar:**
  - dünya düzeyi %95 bootstrap aralığı (10 000 yeniden örnekleme, tohum 0);
  - en kötü dünya;
  - B3, B4, B8;
  - temel koşul;
  - referans kollar;
  - tavana uzaklık.
- **Hedef ve sonuç dili** (kullanıcı kararı madde 7): ikincil ölçütler eşik değildir. Hedefleriyle (ör. unutma %0,1–0,2) yan yana yazılır.

## 5. Bilinen sınırlar (koşudan önce yazıldı)

- **Önceki görülmüş dünyalarda (DEV, 310607–310609, k = 2):** son hâl B1/B2 ve M4 0,958–1,000. Taze dünyada farklı olabilir.
- **Vücut keskinliği,** görülmüş dünyalardaki sonuçlara bakıldıktan sonra seçildi (DEV ayarı). k = 1'de karanlık uzun tamamlama %90 altındaydı. Rapor bunu yazar.
- **Değişen dünya** (B5/B6) ve **ölçek** düzeni bu sınava dahil değil.
- **Unutma** yalnız 5 denetim noktasında ölçülüyor.

## 6. Sonra

- **Ham çıktı:** `pilot/sonuclar/` (json.gz + SHA-256) ve açık depo `erika-open-evals/records/2026-11-IP0/`.
- **Bağımsız yeniden puanlama:** Claude 2 ya da Codex.
- **Rapor:** tutan ve tutmayan bütün ölçütler.
