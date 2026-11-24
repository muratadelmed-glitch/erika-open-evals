# İP1: zor dünyada kilitli bellek sınavı (ön kayıt)

- **Yetki:** `docs/eidra/kararlar/KULLANICI_KARARI_2026-11-24_BASVURU_GUCLENDIRME.md` madde 1.
- **Araç:** `pilot/vucut/ip1.py` (bu dosyanın kilit commit'inde dondurulur).
- **Kilit:** dosyanın sonundaki `ip0` bloğunda `statu` satırı `KILIT_ADAYI` → `KILITLI` yapılan commit. Kilit commit'i
  yalnız bu satırı değiştirir (`ip0.kilit_denetle`). Kilitten sonra araç şu durumlarda koşmaz:
  - `pilot/` kodu değişmişse (sonuclar/ ve testler/ dışında; substrat/ ve rust/ kaynakları dahil);
  - iki genom dosyası değişmişse (ayrı denetim; ayrıca içerik SHA-256'sı araçta sabit);
  - ERIKA 2 Rust çekirdeğinin (`libsubstrat_cekirdek.so`) SHA-256'sı `89762ce1…f8d8` değilse.
- **Bir kez:** kilitli koşu bitince `docs/eidra/plan/2026-11-24_IP1_KOSU_KAYDI.md` commit edilir (manifest SHA-256'sı ile).
  Bu dosya git geçmişinde bir kez bile varsa araç yeni kilitli koşuyu reddeder. Dünya süreçleri yalnız `kos` üst
  sürecinin verdiği tek kullanımlık belirteçle açılır.

## 0. Basit anlatım

ERIKA 1, alıştırma dünyalarında zor testte nesnelerin %77'sini biliyordu. Bu sayı, gördüğümüz dünyalardan geliyor.
Şimdi hiç açılmamış 20 yeni dünyada aynı testi tek sefer yapacağız. "Geçti" demek için gerekenleri koşudan önce yazıp
kilitliyoruz. Sonuç ne çıkarsa çıksın yayımlanır.

## 1. Soru ve hipotezler

Başvurunun iddiası (DEV, 6 dünya): zor dünyada, bütün ikililer ölçütüyle ERIKA 1 nesnelerin %77,1'ini biliyor. Her
karşılaşmayı saklayan en yakın komşu referansı (%56,8) ve tek başına bellek sistemleri (yavaş %32,9, hızlı %27,4)
geride kalıyor.

| # | Hipotez | Ölçü | Geçme kuralı |
|---|---|---|---|
| H1 | ERIKA 1 görülmemiş dünyalarda da yüksek düzeyde biliyor | ERIKA 1'in dünya ortalaması (bilinen / görülen) | ≥ 0,70 |
| H2a | ERIKA 1, her karşılaşmayı saklayan 1-en yakın komşudan iyi | ERIKA 1'in kesin fazla bildiği dünya sayısı | ≥ 16 / 20 |
| H2b | ERIKA 1, her karşılaşmayı saklayan 5-en yakın komşudan iyi | aynı | ≥ 16 / 20 |
| H3a | ERIKA 1, yalnız hızlı bellekten iyi | aynı | ≥ 16 / 20 |
| H3b | ERIKA 1, yalnız yavaş bellekten iyi | aynı | ≥ 16 / 20 |

- **Genel karar:** beşi de geçerse `PASS`; biri bile geçmezse `FAIL` (hangisinin geçmediği yazılır).
- Bir dünya çökerse, eksikse, çıktısının SHA-256'sı manifestle uyuşmazsa ya da yeniden hesaplanan sayım dünya sürecinin
  sayımıyla uyuşmazsa: `INCONCLUSIVE`. Eksik dünya yerine yenisi açılmaz; yeniden koşu yoktur.
- **Eşiklerin gerekçesi** (DEV, §5):
  - H1 için 0,70: 20 DEV dünyasında ERIKA 1'in dünya ortalaması 0,780, %95 aralığı [0,764; 0,796]. Bu nedenle 0,70,
    ortalamanın yaklaşık 8 puan altında. En kötü DEV dünyası ise 0,697 (310818): eşik dünya başına değil, ortalamaya
    uygulanır. Amaç %77'nin tam tekrarı değil; düzeyin görülmemiş dünyada çökmediğini göstermek. Ölçülen değer ve %95
    aralığı ayrıca yazılır.
  - 16/20, tek yönlü işaret testinde p ≈ 0,006 demek. Beraberlik ERIKA 1 aleyhine sayılır. DEV'de dört karşılaştırmanın
    dördünde ERIKA 1, 20 dünyanın 20'sinde önde (en küçük fark 17 nesne).
  - ERIKA 2 kollarından birinin hatası (ör. Rust çekirdeği) yalnız o kolu boş bırakır; H1–H3'ü etkilemez.

## 2. Dünyalar

- **Değerlendirme bölümü 312021–312040 (20 dünya).** İP0 312001–312020'yi kullandı; 312000 karantinada. Bu dünyalar daha
  önce hiçbir araçla açılmadı: vücut dünyası değerlendirme seed'ini yalnız kilitli ön kayıtla kurar (`dunya.dev_seed`).
- **Düzen:** nöral ERIKA'nın evrim merdiveninde düzey 4 ("zor dünya"): `substrat/evrim1.DUZEYLER[4]` =
  `DunyaAyar(birey=30, iz_piksel=1, iz_sapma=0.04, koku=True, koku_aile=0.5)`, öteki alanlar varsayılan. Vücut normal
  (`ayarla(None)`).
  - Akışta 180 birey var (3 aile × 2 tür × 30). Bunlara ek olarak tür başına 4 test bireyi var; bunlar akışta hiç
    görünmez ve bu sınava girmez.
  - 12 renk, 3.000 karşılaşma. Koku var; tür kokusunun yarısı ailede ortak. Tat yok.
  - Her birey kendi türünden sapar:
    - aile şeklinden 1 çevrik piksel;
    - doku, ses ve kokuda N(0; 0,04) sapma.
  - Tür başına bireylerin %30'u yalnız akışın ilk %30'unda görünür (emekliler). Gizli renkli bireyler akışın %70'inde girer.
  - Sınav yalnız akışta en az bir kez görülen nesneleri sorar: DEV'de dünya başına 177–180.
- Mühürlü holdout (251000–251063) kullanılmaz.

## 3. Ölçüt

- Görülen her nesne 7 kez sorulur:
  - dört duyu birlikte;
  - her iki duyulu ipucuyla ayrı ayrı (6 çift).
- İpucu renksizdir. Göz ipucu renksiz 5×5 görüntüdür; dokunma, ses ve koku yeni gürültüyle üretilir
  (`olcum.ipucu(d, b, 1001)`).
- Yedi cevabın hepsi doğru palet rengiyse nesne "biliniyor". Skor = bilinen / görülen.
- **İstatistik birimi dünyadır.** Ölçülerin hesaplanışı:
  - dünya ortalaması;
  - %95 bootstrap aralığı (dünya üzerinden, 10.000 tekrar, tohum 0);
  - en kötü dünya;
  - eşli karşılaştırmada aynı dünyada kesin fazla bilinen nesne sayısı.

## 4. Kollar (hepsi aynı dünya, aynı akış, aynı ipuçları)

| Kol | Ne | Rol |
|---|---|---|
| `erika1` | ERIKA 1: `erika_son_bol_tam_kar_ebk` (İP0'daki kol) | **birincil** |
| `hizli` | yalnız hızlı bellek (`epizodik`) | referans (H3a) |
| `yavas` | yalnız yavaş bellek (`yavas`) | referans (H3b) |
| `nn1` | her karşılaşmayı saklayan 1-en yakın komşu (`evrim3.tavan` ile aynı) | referans (H2a) |
| `knn5` | aynı bellek, 5 en yakın komşunun çoğunluk oyu | referans (H2b) |
| `e2_<genom>_t<0,1,2>` | ERIKA 2, dört genom × üç ağ tohumu | betimsel (eşiksiz) |

- **ERIKA 2 genomları:**
  - `k515`: 515. kuşağın evrilmiş kuralı (arşiv, içerik SHA-256 `dc7f2383…066e`);
  - `k852`: en son evrilmiş kural (`36f15fcb…c704`);
  - `el`: elle verilen kural, ayarsız;
  - `el_uyum005`: aynı kural, duyu uyumu 0,005 (DEV'de ayarlandı).
- **ERIKA 2 ağ ayarları:** ag2, atama izi, birikimli uyum, kapı, Rust çekirdeği (v1.7 ayarları). Ağ tohumu (0, 1, 2)
  bağlantıları ve başlangıcı değiştirir.
- **k-NN'de k = 5'in seçimi:** DEV 310806–310819 (14 dünya), k ∈ {1, 3, 5, 9, 15, 25} arasında en yüksek ortalama
  (betik ve günlük: `pilot/sonuclar/2026-11-24_IP1_KNN_SECIMI.{py,log}`):

  | k | 1 | 3 | **5** | 9 | 15 | 25 |
  |---|---|---|---|---|---|---|
  | ortalama | 0,5874 | 0,6135 | **0,6143** | 0,5896 | 0,5664 | 0,5381 |

  - k = 3 ile 5 pratikte eşit.
  - k seçilirken ERIKA 1 bu dünyalarda koşulmamıştı; seçim ERIKA 1'e göre yapılmadı. Seçim, referansı güçlendiren yönde.
  - **Beraberlik kuralı:** oy eşitse ve en yakın komşunun rengi eşitlerden biriyse o renk; değilse eşitlerin en küçük
    renk indeksi.
- **Bütçe ölçüleri (betimsel; karar vermez), her kol ve dünya için:**
  - öğrenme + sınav CPU süresi (tek iş parçacığı);
  - yaşam sonunda tutulan sayı adedi (`ip1.sayi_say`; NumPy dizileri ve Python sayıları, önbellekler dahil).

## 5. DEV dayanağı (kilitten önce, görülmüş dünyalar)

Aynı araçla, `--dev`, 310800–310819 (20 dünya). Parite: 310800–310805'te ERIKA 1, hızlı, yavaş, 1-NN sayımları
`pilot/sonuclar/2026-11-23_ERIKA1_ZOR_DUNYA.json.gz` ile; 310800–310801'de ERIKA 2 sayımları
`2026-11-23_VIDEO_SAYI_DOGRULAMA` ile birebir aynı.

Aynı araçla (`--dev`, ağaç kirli olduğu için rapor bunu `INCONCLUSIVE / DEV_ONLY` etiketler; sayılar aşağıda), 20 dünya,
süre 592 sn (4 süreç):

| kol | bilinen / görülen | dünya ort. | %95 aralık | en kötü dünya | CPU sn / yaşam | tutulan sayı |
|---|---|---|---|---|---|---|
| `erika1` | 2792 / 3578 | 0.780 | [0.764, 0.796] | 0.697 | 13.5 | 847,216 |
| `hizli` | 1000 / 3578 | 0.279 | [0.252, 0.308] | 0.156 | 6.8 | 263,909 |
| `yavas` | 1300 / 3578 | 0.363 | [0.329, 0.396] | 0.184 | 1.9 | 379 |
| `nn1` | 2081 / 3578 | 0.582 | [0.559, 0.604] | 0.478 | 0.3 | 150,098 |
| `knn5` | 2172 / 3578 | 0.607 | [0.588, 0.626] | 0.517 | 0.5 | 150,098 |
| `e2_k515_t0` | 1194 / 3578 | 0.334 | [0.310, 0.362] | 0.246 | 7.0 | 2,118,053 |
| `e2_k852_t0` | 700 / 3578 | 0.196 | [0.176, 0.216] | 0.124 | 7.6 | 2,118,053 |
| `e2_el_t0` | 1594 / 3578 | 0.446 | [0.421, 0.471] | 0.363 | 5.7 | 1,896,765 |
| `e2_el_uyum005_t0` | 1927 / 3578 | 0.539 | [0.519, 0.559] | 0.436 | 5.3 | 1,896,765 |

- ERIKA 2'nin üç ağ tohumu arasındaki fark küçük: k515 0,329–0,334, k852 0,196–0,200, el 0,446, el_uyum005 0,538–0,539.
- **Bütçe okuması:** ERIKA 1, 1-NN'nin yaklaşık 5,6 katı sayı tutuyor ve yaklaşık 45 katı CPU harcıyor. ERIKA 2 en çok
  sayıyı tutuyor (ağırlıklar). Bu sınav doğruluk sınar, verim sınamaz.
- Sıralama 310800–310819 olarak 20 dünya; 310806–310819'da k seçimi ERIKA 1 koşusundan önce yapıldı.

## 6. Süreç

1. Bu dosya ve araç commit edilir (`statu: KILIT_ADAYI`).
2. Bağımsız denetim (ajan; araç ve ön kayıt, sızıntı ve kaçamak açısından): yapıldı, 1 kritik + 5 önemli + 5 küçük
   bulgu; hepsi kilitten önce düzeltildi (`pilot/sonuclar/2026-11-24_IP1_ON_DENETIM.md`).
3. Kilit commit'i: yalnız `statu` satırı `KILITLI` olur.
4. Kilit commit'inde ayrı, temiz bir klonda (öteki ajanların commit'i koşuyu bozmasın), tek koşu:
   `cd pilot && python3 -B -m vucut.ip1 kos --cikti <depo dışı dizin> --dunyalar 312021 … 312040 --on_kayit ../docs/eidra/plan/2026-11-24_IP1_ZOR_DUNYA_ON_KAYIT.md --is 4`
5. Karar: `python3 -B -m vucut.ip1 rapor <dizin> --on_kayit <bu dosya> --json <dizin>/rapor.json`.
6. Koşu kaydı (`2026-11-24_IP1_KOSU_KAYDI.md`: manifest SHA-256'sı, karar) hemen commit edilir.
7. Ham çıktılar (dünya JSON'ları, MANIFEST, açık veri .npz) arşivlenir ve açık depoda (`erika-open-evals/records/`)
   yayımlanır. Dışarıdan yeniden puanlama: açık depodaki puanlayıcı tahmin ve cevaplardan sayımı yeniden hesaplar.

## 7. Bilinen sınırlar (koşudan önce yazıldı)

- Tek kod sürümü, dünya başına tek koşu; ERIKA 1'de tohum yok (ölçüm tohumları kodda).
- Dünyalar küçük ve sentetik. Bu sınav, başka dünya türlerine genellemeyi göstermez.
- 1-NN ve 5-NN akıştaki bütün ham karşılaşmaları saklar. Yani elde olan bütün bilgiyi tutar. Ama öğrenen bir yöntem
  değildir. Daha güçlü referanslar (ör. çevrimdışı eğitilmiş sınıflandırıcı) bu sınavda yok.
- ERIKA 1 bu referanslardan daha çok sayı tutar ve daha çok CPU harcar (§5). Bu sınav verim üstünlüğü iddiası
  sınamaz; yalnız doğruluk sınar.
- ERIKA 2 için eşik yok. Ön kayıtlı amaç yalnız bugünkü düzeyi görülmemiş dünyada ölçmek.

```ip0
dunyalar: 312021 312022 312023 312024 312025 312026 312027 312028 312029 312030 312031 312032 312033 312034 312035 312036 312037 312038 312039 312040
kollar: erika1,hizli,yavas,nn1,knn5,e2_k515_t0,e2_k515_t1,e2_k515_t2,e2_k852_t0,e2_k852_t1,e2_k852_t2,e2_el_t0,e2_el_t1,e2_el_t2,e2_el_uyum005_t0,e2_el_uyum005_t1,e2_el_uyum005_t2
bayraklar: --duzey=4 --olcut=tum_ikililer --knn=5 --e2_tohumlar=0,1,2
statu: KILITLI
```
