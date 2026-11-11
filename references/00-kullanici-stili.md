# 00 — Kullanıcı Stili (ZORUNLU — her projede uygulanır)

Bu dosya kullanıcının kişisel çizim zevkini tanımlar. Genel kurallarla çelişirse **bu dosya geçerlidir** (elektriksel doğruluk hariç).

## 1. Şematik: "Kutu Kutu" Blok Düzeni

Kullanıcı, şematiğin fonksiyon bloklarına ayrılmış **düzgün kutular** halinde olmasını seviyor (önceki projelerde yaptığımız gibi).

Kurallar:
- Her fonksiyon bloğu **dikdörtgen bir çerçeve** içindedir: `GÜÇ GİRİŞİ / KORUMA`, `5V BOOST`, `3V3 LDO`, `MCU`, `MOTOR SÜRÜCÜ`, `KONNEKTÖRLER`, `DURUM LED'LERİ`...
- Çerçevenin sol üst köşesinde **blok başlığı** bulunur: büyük ve kalın yazı (KiCad'de 2.54 mm text, kalın). İsteğe bağlı olarak altına tek satır açıklama yazılır ("TP4056 – 1 A şarj, Rprog = 1.2k").
- Çerçeveler **ızgara gibi hizalıdır**: aynı satırdaki kutuların üst kenarları aynı hizada, aynı sütundakilerin sol kenarları aynı hizadadır. Kutular arasında eşit boşluk (≥5 mm) bırakılır.
- Kutuların sırası blok diyagramı izler: sol üstten başlar (güç girişi), sağa ve aşağıya doğru ilerler (çıkışlar/konnektörler sağda ya da altta).
- Kutu içindeki bağlantılar **tel** ile yapılır. Kutular arası bağlantılar **net label / güç sembolü** ile yapılır. Böylece her kutu kendi başına okunur.
- Kutu içinde boşluk dengeli olur: parçalar kutunun kenarına yapışmaz (≥2.5 mm iç boşluk) ve kutu gereğinden büyük olmaz.
- Çerçeve çizgisi: ince, düz ya da kesikli (dashed). Projede tek bir stil seçilir ve tutarlı kullanılır. Varsayılan: **kesikli, 0.15–0.25 mm**.
- Hesap/layout notları kutunun içine, ilgili parçanın yanına küçük yazıyla eklenir.
- Kapak/başlık bloğunda revizyon ve tarih bulunur.

Uygulama:
- **EasyEDA:** "Rectangle" ile kutu çizilir, "Text" ile başlık eklenir. Kutular "Align" araçlarıyla hizalanır.
- **KiCad:** Grafik dikdörtgen (`Place > Rectangle`) + text kullanılır. Otomatik üretimde (`sch_lib` tipi betiklerde) her blok için `(rectangle (start x y) (end x y) (stroke (width 0.2) (type dash)))` ve başlık `text` öğesi eklenir. Kutu ölçüsü, bloğun içerdiği parçaların sınır kutusu + 5 mm pay olarak hesaplanır ve 1.27 mm ızgaraya yuvarlanır.

## 2. PCB: Yumuşak / Yuvarlatılmış Yollar (Smooth / Arc Tracks)

Kullanıcı köşeleri **yay (arc) ile yuvarlatılmış** "smooth" yolları seviyor.

Kurallar:
- Tüm sinyal ve güç yollarında köşeler **yay** ile döner (45° kırık yerine). Düz kısımlar düz kalır; yalnızca köşeler yuvarlatılır.
- Yay yarıçapı tutarlı olur: sinyal izlerinde **≥ 3 × iz genişliği** (ör. 0.25 mm iz → ~0.8–1.5 mm yarıçap). Paralel giden bus/izlerde **eş merkezli (concentric)** yaylar kullanılır, böylece aralık sabit kalır.
- Paralel iz grupları birlikte ve eşit aralıkla döner (konser görünümü).
- Pad girişi yine **düz** olur: iz pad'e merkezden ve pad ekseni boyunca girer. Yay, pad'den en az bir iz genişliği uzakta başlar.
- Diferansiyel çiftlerde (USB) yaylar eş merkezli ve simetrik olur. Uzunluk eşitliği yeniden kontrol edilir.
- **Teardrop** (pad/via–iz geçişinde damla) ile birlikte kullanılabilir ve smooth görünümü tamamlar. Varsayılan: açık.
- DRC yay geometrisinde de temiz olmalıdır. Yuvarlatma sonrası **boşluk (clearance) ihlalleri ve döküm boşlukları yeniden kontrol edilir**.

Uygulama:
- **KiCad 10:** İnteraktif router'da köşe modu `Ctrl+/` ile değiştirilir: 45° → 90° → **Arc 45°** → Arc 90°. "Arc 45" seç. Mevcut izleri yuvarlatmak için izleri seçip *Route > Fillet Tracks* kullan (yarıçap gir). Teardrop: *Edit > Edit Teardrops* ya da Board Setup. Otomatik üretimde izler `(arc (start) (mid) (end) (width) (layer) (net))` olarak yazılır; köşe = iki düz segment arasındaki teğet yay. Fillet geometrisinin hesabı: yarıçap R, köşe açısı θ için kesim mesafesi d = R·tan(θ/2).
- **EasyEDA Pro:** Routing sırasında köşe/açı modunu yay (arc) moduna al (routing modu değiştirme kısayolu veya üst araç çubuğundaki routing ayarları). Yerleşik bir "yolları yuvarlat/round corner" aracı varsa onu kullan. Teardrop için *Tools > Teardrops*. Menü adları sürüme göre değişebilir; kullanıcıya yol tarif ederken sürümü sor ya da ekran görüntüsü iste.

## 3. Genel Görünüm Tercihleri

- Düzen, hizalama ve tutarlılık önceliklidir. Kullanıcı "temiz, okunur, profesyonel" görünüm istiyor.
- Kart kimliğinde şirket adı yazılmaz.
- Kullanıcı yeni bir tercih belirttiğinde bu dosyaya eklenir (tarihli).

## Tercih Geçmişi

- 2026-11-11: Şematikte kutu kutu blok düzeni; PCB'de smooth (arc) yollar istendi.
