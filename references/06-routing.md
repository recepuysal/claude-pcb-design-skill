# 06 — Yol Çizimi (Routing) ve Bakır Dökme

## 1. Temel Prensip: Akım Döngüsü (Current Loop)

Her sinyalin bir **dönüş akımı** vardır. Yüksek frekansta (kenar süresi ns mertebesindeyse, dijital hatların hepsi böyledir) dönüş akımı sinyal izinin **hemen altındaki referans düzlemden** geri döner. Bu nedenle:
- Sinyalin altındaki GND düzlemini kesersen dönüş akımı dolaşmak zorunda kalır. Döngü alanı büyür ve EMI ile crosstalk artar.
- **2 katmanda kural:** Alt katman GND'dir. Alttan bir iz geçirmek zorunda kalırsan **kısa** tut (≤10–15 mm) ve üstteki hızlı sinyallere **dik** geçir. Uzun alt katman izleri GND'yi adacıklara böler. Bu durum yasaktır.

## 2. Routing Sırası

1. **Güç ve yüksek akım yolları** (SMPS sıcak döngüsü, motor yolları) — geniş iz veya polygon
2. **Kritik sinyaller:** kristal, USB diferansiyel çift, analog/ADC, sense hatları
3. **Saat ve hızlı dijital** (SPI SCK, PWM)
4. **Kalan sinyaller**
5. **GND dökümü + dikiş via'ları (stitching)**
6. DRC + görsel review

## 3. Geometri Kuralları

- Köşeler **yay (arc) ile yuvarlatılır**; bu kullanıcının stilidir (`00-kullanici-stili.md` §2). Yay kullanılamayan yerde 45° kullanılır. 90° köşe kullanma (elektriksel etkisi düşük frekansta küçüktür ama amatör görünür). Asla **dar açı (acute angle)** oluşturma; dar açılar aşındırmada asit tuzağı (acid trap) olur.
- İz pad'e **pad'in uzun ekseni boyunca, merkezden** girer. Pad'e yandan ya da çapraz girme.
- İz genişliği pad genişliğinden büyükse pad'e girerken pad genişliğine daraltılır (neck-down). Bu, tombstoning'i önler.
- İki pasifin pad'leri arasından iz geçirme (0603 altı hariç değil, hiçbir durumda tavsiye edilmez).
- Gereksiz via kullanma. Her via bir kusur ve endüktans kaynağıdır. Sinyal başına en fazla 2 via hedefle.
- SMD pad'in içine via koyma (via-in-pad), JLC'de dolgu seçilmedikçe lehim emilir. İstisna: QFN termal pad'indeki ısıl via'lar (0.3 mm, maskeyle örtülü ya da "tented").
- Paralel uzun hatlarda 3W kuralı uygulanır (merkezler arası ≥3× iz genişliği) ve crosstalk azaltılır.
- Kart kenarına paralel ve çok yakın hızlı sinyal çizme (≥1 mm + GND).
- Yarım kalmış iz parçası (stub), boşta kalan via ya da çift çizilmiş iz bırakma.

## 4. Güç Routing'i

- Genişlik: `04-jlcpcb-kurallar.md` §3 net class tablosuna göre belirlenir. Şüpheliysen geniş tut.
- Güç **yıldız ya da ağaç** şeklinde dağıtılır: kaynak → bulk → IC'ler. Zincirleme ince izle (daisy chain) dağıtma.
- Dekuplaj sıralaması: güç izi **önce kondansatöre, sonra IC pinine** gelir. Kondansatörün GND ucu via ile hemen GND düzlemine iner (pad'in yanına, ≤0.5 mm).
- Yüksek akımda polygon (copper pour/zone) kullan. Katman değiştirmede çoklu via kullan.
- Ölçüm/sense hatları (akım sense, batarya ölçümü, FB) **Kelvin** bağlanır: güç akımının geçtiği izden değil, doğrudan sense noktasının pad'inden ayrı ince bir iz çekilir.

## 5. Topraklama (Grounding)

- **Tek GND neti kullan.** AGND/DGND ayrımını yalnızca datasheet zorunlu kılıyorsa yap. Ayırırsan tek noktada birleştir. Çoğu karışık sinyal tasarımında doğru yöntem bölünmemiş tek GND düzlemi + doğru yerleşimdir (gürültülü ve hassas bölgelerin fiziksel ayrılması).
- Güç GND (motor, SMPS) dönüş yolu, hassas devrelerin altından geçmemelidir. Bunu yerleşimle sağla.
- Konnektör GND pinleri düzleme birden fazla via ile bağlanır.

## 6. Bakır Dökme (Copper Pour)

- **Alt katman: tam GND dökümü.** Üst katman: boş alanlar GND dökümü + dikiş via'ları (isteğe bağlı ama önerilir).
- Dikiş via'ları: kart kenarı boyunca ve döküm boyunca **~5–10 mm** aralıkla, ayrıca her katman geçişinde sinyal via'sının yanına bir GND via'sı.
- Döküm boşluğu (zone clearance): 0.3 mm; minimum genişlik: 0.25 mm. Ada (island) olarak kalan bakırları sil ("remove islands").
- Termal rölyef: THT pad'lerde **açık** (lehimlenebilirlik için). Yüksek akım SMD pad'lerde **solid** bağlantı.
- Anten altı, kristal altı (sadece GND olabilir; tercihen kristal bölgesi solid GND ve başka sinyal yok) ve yüksek gerilim bölgeleri için keepout tanımla.
- Dökümü en son yap, sonra **her değişiklikten sonra yeniden doldur** (refill: KiCad `B`, EasyEDA `Shift+B`).

## 7. Özel Sinyaller (özet — ayrıntı `10-arayuzler.md`)

| Sinyal | Kural |
|---|---|
| Kristal | Kısa, simetrik, via yok, altında solid GND, etrafında GND guard; başka hat yaklaşmaz |
| USB D+/D− | Diferansiyel çift, eşit uzunluk (±0.15 mm), via yok, kesintisiz GND üstünde, ESD konnektörde |
| SPI SCK | Kısa; >10 cm ise kaynakta 22–33 Ω seri direnç |
| I2C | Kritik değil, ancak toplam kapasite <400 pF olmalı |
| ADC girişi | Gürültülü hatlardan uzak, RC filtresi ADC pinine yakın |
| SMPS SW | Mümkün olan en küçük alan; FB hattı SW ve indüktörden uzak |
| Motor fazları | Geniş, kısa, kart içi eşit uzunluk gerekmez |

## 8. Routing Kapısı

- [ ] DRC **0 hata**; unrouted (bağlanmamış) net **0**
- [ ] Alt GND düzleminde uzun yarık yok; GND adacığı yok
- [ ] Dekuplaj kondansatörlerinin GND via'ları pad'e bitişik
- [ ] Güç izleri net class genişliğinde; katman geçişlerinde yeterli via var
- [ ] Kristal, USB ve SMPS kuralları sağlandı
- [ ] Dar açı, stub ve gereksiz via yok
- [ ] Döküm yeniden dolduruldu, dikiş via'ları eklendi
- [ ] Görsel review yapıldı: üst, alt ve birleşik görünüm
