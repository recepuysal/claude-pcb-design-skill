# 11 — Serigrafi (Silkscreen) ve Kart Üzeri Dokümantasyon

## 1. Boyutlar (JLC)

- Referans (refdes) metni: **yükseklik 1.0 mm, kalınlık 0.15 mm** (JLC minimum). Çok yoğun kartlarda refdes'i Fab katmanında tut ve serigrafide gösterme. Bu durumda montaj çizimi (assembly drawing) PDF olarak verilir.
- Başlık ve konnektör etiketleri: 1.5–2.0 mm yükseklik, 0.2–0.25 mm kalınlık.
- Pad'e mesafe ≥0.15 mm. Serigrafi **asla pad, via veya maske açıklığının üzerine binmez** (JLC bu kısmı keser ve yazı kesik çıkar).

## 2. Yerleşim Kuralları

- Refdes, ait olduğu parçanın **yanında ve tutarlı bir konumda** durur (ör. hep üstte ya da hep solda). Başka bir parçanın yanına düşerek karışıklık yaratmamalıdır.
- Okuma yönü yalnızca **iki yöndedir:** 0° (soldan sağa okunur) ve 90° (aşağıdan yukarıya okunur). Ters (180°/270°) yazı kullanma.
- Parça altına (gövde altında kalacak şekilde) yazı yazma; gövde serigrafiyi kapatır.
- Hizalı bir parça grubunun refdes'leri de hizalı olur.

## 3. Zorunlu İşaretler

- **Pin 1** işareti (IC, konnektör): nokta ya da üçgen; gövde dışında, montajdan sonra da görünür olmalı.
- **Kutupluluk:** diyot katot çizgisi, LED katot işareti, elektrolitik "+" işareti, pil "+/−" işareti.
- **Konnektör pin etiketleri:** her pinin yanına sinyal adı yazılır (ör. `GND 3V3 SDA SCL`). Kullanıcı kartı tak-çıkar yaparken şematiğe bakmak zorunda kalmamalı.
- Güç girişinde gerilim ve polarite: `12V ⎓ +  −`.
- Buton/LED fonksiyonu: `RST`, `BOOT`, `PWR`, `CHG`.
- Jumper ve DIP anahtar ayarları kısa bir tabloyla yazılır.
- Test noktalarının etiketleri: `TP3 +3V3`.

## 4. Kart Kimliği

- Kart adı + revizyon + tarih: ör. `MOTOR-DRV v1.0 2026-11`. Şirket adı yazılmaz (kullanıcı tercihi).
- JLC sipariş numarasının yeri: `JLCJLCJLCJLC` metni (ya da ücretli kaldırma seçeneği).
- İsteğe bağlı: QR kod / seri numarası kutusu (beyaz dolu alan), logo.
- Kart yönünü gösteren işaret (ör. "TOP" ve ok) mekanik montajda faydalıdır.

## 5. Fab/Assembly Katmanları

- Fab katmanında gövde çizgisi + refdes bulunur (montaj çizimi için).
- Courtyard tüm parçalarda tanımlı ve çakışmasız olmalı.
- 3D model her parçada olmalı. 3D render, kullanıcıya ve review'a gösterilir.

## 6. Serigrafi Kontrol Listesi

- [ ] Pad/via üzerinde serigrafi yok (DRC "silk over copper" temiz)
- [ ] Tüm refdes'ler okunur, 1.0/0.15 mm, iki yönde ve parçasına yakın
- [ ] Pin 1 ve kutup işaretleri tam
- [ ] Konnektör pin etiketleri ve güç girişi polaritesi yazılı
- [ ] Kart adı / revizyon / tarih yazılı; şirket adı yok
- [ ] JLC sipariş numarası yeri belirlendi
