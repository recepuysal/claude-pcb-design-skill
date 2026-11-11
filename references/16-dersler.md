# 16 — Dersler (Lessons Learned) — Kendi Kendine Öğrenme Kaydı

Her projenin başında bu dosyayı oku. Her projenin sonunda ya da kullanıcı bir hata/tercih bildirdiğinde **en üste** yeni kayıt ekle.

Format:
```
## YYYY-MM-DD — <proje> — <kısa başlık>
- Ne oldu: ...
- Kural: ...  (genel kural ise ilgili referans dosyasını da güncelle: <dosya>)
```

---

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
