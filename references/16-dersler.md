# 16 — Dersler (Lessons Learned) — Kendi Kendine Öğrenme Kaydı

Her projenin başında bu dosyayı oku. Her projenin sonunda ya da kullanıcı bir hata/tercih bildirdiğinde **en üste** yeni kayıt ekle.

Format:
```
## YYYY-MM-DD — <proje> — <kısa başlık>
- Ne oldu: ...
- Kural: ...  (genel kural ise ilgili referans dosyasını da güncelle: <dosya>)
```

---

## 2026-11-11 — NANO-C (Nano uyumlu USB-C) — Alan bütçesi Faz 0'da yapılmalı
- Ne oldu: Kullanıcıya "tek yüz dizgi" seçeneği önerildi, kullanıcı onayladı. Yerleşimde 18×43 mm'ye sığmadığı ortaya çıktı ve soru yeniden soruldu. Orijinal Nano zaten çift yüzlü.
- Kural: Form faktörü sabit kartlarda **Faz 0/1'de alan bütçesi** çıkar: Σ(pad+gövde alanı) × 1.5 ≤ kullanılabilir alan. Seçenek sunmadan önce hesapla. Footprint'lerin courtyard'ına değil **pad + gövde** sınırına bak (EasyEDA courtyard'ları yalnız gövdeyi kapsar). (`01-gereksinim-mimari.md`)

## 2026-11-11 — NANO-C — EasyEDA footprint tuzakları
- Ne oldu: TYPE-C-31-M-12 footprint'inde iki konum deliği kaplamalı (PTH, halka 0) tanımlıydı. Konnektörün kendi pad aralığı 0.1 mm idi ve genel 0.2 mm kuralına takıldı.
- Kural: İçe aktarılan footprint'leri DRC'den geçir: numarasız PTH → NPTH yap. Fine-pitch konnektör için yalnız o footprint'e `.kicad_dru` kuralı yaz: `A.memberOfFootprint('J1') && B.memberOfFootprint('J1')` (`A.Parent.Reference` çalışmıyor). (`15-kicad-otomasyon.md`)

## 2026-11-11 — NANO-C — Breadboard modüllerinde header yüzü
- Ne oldu: Pin header'lar önce üst yüze kondu. Nano tipi modüllerde header pinleri aşağı bakar, plastik gövde **alt yüzde** kalır.
- Kural: Breadboard/modül kartlarında 1×N header'ları alt yüze yerleştir. pcbnew'de tek sıralı header'ı `FLIP_DIRECTION_LEFT_RIGHT` ile çevir (TOP_BOTTOM pin sırasını ters çevirir). Çevirdikten sonra pin 1 konumunu pad dökümüyle doğrula.

## 2026-11-11 — NANO-C — KiCad kurallarının yeri
- Ne oldu: `board.GetDesignSettings()` ile yapılan kural değişiklikleri (kenar boşluğu) DRC'ye yansımadı, çünkü kurallar `.kicad_pro` dosyasında tutuluyor. Parity uyarıları footprint'e kopyalanmayan Datasheet/Manufacturer alanlarından çıktı.
- Kural: Kuralları ve net class'ları `.kicad_pro` → `board.design_settings.rules` ve `net_settings` içine JSON olarak yaz. Netlist'teki tüm alanları (Datasheet ve Description dahil) `fp.SetField()` ile footprint'e kopyala.

## 2026-11-11 — genel — "Doğru ama amatör" çizim
- Ne oldu: Önceki PCB/şematik çalışmalarında bağlantılar doğruydu ama kullanıcı çizimi profesyonel bulmadı.
- Kural: Bu skill oluşturuldu. Faz kapıları, kontrol listeleri, kullanıcı stili (kutu kutu şematik, smooth yollar) ve en az 2 tur görsel öz-inceleme zorunlu hale getirildi.

## 2026-11-11 — kullanıcı tercihi — Stil
- Ne oldu: Kullanıcı şematiğin kutu kutu düzgün bloklar halinde olmasını, PCB'de smooth (yuvarlatılmış) yolları sevdiğini söyledi.
- Kural: `00-kullanici-stili.md` her projede uygulanır.

## 2026-11 — kablo test cihazı — Doğrulanmamış mekanik varsayımlar
- Ne oldu: Header aralığı (25.4 mm), konnektör pin 1 yönü ve kablo pin dizilimi tahminle tasarıma girdi; bunlar sonradan sorun olarak döndü.
- Kural: Ölçü ve pin yönü varsayımlarını her teslimde "doğrulanmamış varsayımlar" başlığı altında listele ve kullanıcının ölçmesini iste. (`12-kontrol-listeleri.md` §E)

## 2026-11 — kablo test cihazı — Dış dünyaya doğrudan bağlanan IC pinleri
- Ne oldu: MCP23S17 pinleri konnektörlere seri direnç ve ESD koruması olmadan doğrudan bağlandı (maliyet/yer kararı).
- Kural: Kablo/konnektöre giden GPIO'larda seri direnç + ESD varsayılandır. Çıkarılacaksa riski kullanıcıya açıkça yaz ve karar olarak kaydet. (`10-arayuzler.md`)

## 2026-11 — KiCad betik üretimi — UUID ve elle düzenleme
- Ne oldu: Şematik yeniden üretilince UUID'ler değişti ve PCB eşleşmesi bozuldu. Kullanıcının elle düzenlediği dosyanın üzerine yazma riski oluştu.
- Kural: UUID'leri deterministik üret. Kullanıcı elle düzenlemeye başladıktan sonra betikle yeniden üretme. (`15-kicad-otomasyon.md`)

## 2026-11 — parça seçimi — Yerel stok
- Ne oldu: Bazı parçalar (4×100R dizi, SRV05-4) Türkiye'de bulunamadı; kullanıcı kartı elle lehimledi.
- Kural: Kart elle lehimlenecekse önce kullanıcının yerel stoğunu/envanterini sor. JLC dizgi varsayımını o zaman yap.
