# Araç yazılım sayfası — 8 Eylül 2026

## Kapsam ve korunanlar

- Yeni hedef: `https://vkotocozum.com/sincan-arac-yazilim`.
- Sayfa: `sincan-arac-yazilim.html`; mevcut ortak stil: `assets/css/site.css`; içerik stili: `assets/css/arac-yazilim.css`.
- Erişim: mevcut üst menüden **Hizmetler → Yazılım Çözümleri → Yazılım Hizmetlerini İncele**. Bölüm başlığı da detay sayfasını açar.
- Ana sayfa ve Hizmetler alt menülerine ilk taslakta eklenen bağlantılar kaldırıldı. Ana sayfa eski haline döndürüldü; mevcut hizmet kartlarının hedefleri korundu.
- Yeni sayfada Hizmetler sayfasının üst menü HTML'i, bağlantıları ve ortak stilleri aynen kullanılıyor. Mobil menü aç/kapa davranışı `assets/js/software-menu.js` ile sağlanıyor. Ayrı bir sayfa menüsü veya yeni üst menü öğesi yok.
- Sitemap'te yeni adres bulunuyor; sayfa konumu Ana Sayfa → Hizmetler → Yazılım Çözümleri olarak tanımlı.
- Mevcut telefon, WhatsApp, QR ve diğer hizmet sayfaları değiştirilmedi.
- Sayfa içindeki yazılım iletişim kişisi Ahmet Bircan Kaya, telefon/WhatsApp: +90 551 865 26 67. Ortak üst menünün mevcut Randevu Al bağlantısı değiştirilmedi; Volkan'ın WhatsApp numarasına gider.
- Yeni sayfadaki saatler Ahmet'in bildirdiği Pzt–Cmt 09.00–19.30. Diğer sayfalardaki dükkan saatleri bu çalışmada değiştirilmedi.
- Mevcut gerçek atölye fotoğrafı ve sosyal paylaşım görseli kullanıldı. Yeni bir logo, fotoğraf veya işletme oluşturulmadı.
- Güç artışı, yakıt tasarrufu, muayene sonucu, işlem süresi ve sabit fiyat garantisi verilmedi.
- Bu dosya bir yayın kaydı değildir. Commit, push, Vercel dağıtımı veya reklam açılışı bu hazırlığın parçası olarak yapılmadı.

## İletişim ve ölçümün mevcut durumu

WhatsApp bağlantısı araç bilgilerini isteyen taslak mesajı açar; kendiliğinden mesaj göndermez. Arama ve harita bağlantıları doğrudan ilgili uygulamaya gider. JavaScript kapalıyken de çalışır.

İletişim düğmelerinde gelecekteki etiket kurulumu için `data-lead-action` ve `data-lead-location` alanları var:

| Aksiyon | Konumlar |
| --- | --- |
| `phone` | `contact` |
| `whatsapp` | `hero`, `contact`, `mobile` |
| `directions` | `contact` |

**Bu alanlar tek başına ölçüm yapmaz.** GA4, Google Ads, Tag Manager veya Meta Pixel eklenmedi. Reklam platformlarına veri gönderilmiyor; analiz çerezi veya tarayıcı depolaması kullanılmıyor. Mevcut sitedeki gibi Google Fonts, yalnızca yazı tipi yüklemek için kullanılıyor.

Etiket kurulurken tıklanan alt öğeler için `closest('a[data-lead-action]')` ile bağlantıyı seç. Telefon ve WhatsApp düğmesi tıklamalarını gerçek müşteri, gönderilmiş mesaj, tamamlanmış arama veya satış olarak sayma. Aynı etkileşimi birden fazla etiketle mükerrer kaydetme. Harita tıklamasını tamamlanmış randevuya eşitleme.

## Reklam açılmadan önce

1. Sayfa metni ve görünümü işletme sahibi tarafından kontrol edilsin. Yeni sayfanın gerçek çalışma kapsamıyla uyumlu olduğu teyit edilsin.
2. Onaydan sonra yalnızca bu çalışmanın dosyaları seçilerek commit/push yapılsın. `marketing/`, `output/`, `tmp/` altındaki eski dosyalar topluca eklenmesin.
3. Mevcut Vercel yayını tamamlanınca temiz URL, CSS, görsel, arama, WhatsApp ve harita hedefleri canlıda kontrol edilsin. Başka bir barındırma hesabına taşınmasın.
4. Kullanılacak Google Ads hesabı ve varsa GA4/GTM kimliği belirlensin. Meta için doğru işletme/reklam hesabı ve varsa veri kaynağı kimliği doğrulansın. Gerçek kimlik olmadan etiket uydurulmasın.
5. Takip teknolojileri etkinleştirilmeden önce gerekli gizlilik ve izin düzeni ayrıca ele alınsın. Hesapların test araçlarıyla tekil olay doğrulaması yapılsın.
6. Kampanya hedef URL'sinde kaynak etiketleri kullanılabilir. Bunlar örnektir; reklam oluşturulmuş değildir:

   - Google: `https://vkotocozum.com/sincan-arac-yazilim?utm_source=google&utm_medium=cpc&utm_campaign=sincan_stage1_test`
   - Instagram: `https://vkotocozum.com/sincan-arac-yazilim?utm_source=instagram&utm_medium=paid_social&utm_campaign=sincan_stage1_test`

7. Eski kart/broşür QR kodlarının hedeflerini değiştirme. Reklam bütçesi için ayrıca onay al; bu sayfa kendi başına harcama başlatmaz.

## Yerel doğrulama

```text
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/software_menu.test.cjs
pnpm build:css
python dev_server.py --host 127.0.0.1 --port 8876 --directory .
```

Yerel sayfa: `http://127.0.0.1:8876/sincan-arac-yazilim`.

Otomatik kontroller; metadata/JSON-LD, telefonlar, WhatsApp taslak mesajı, yerel bağlantılar, sitemap, Yazılım Çözümleri bölümünden erişim, özgün üst menünün aynen kullanılması, eski iletişim hedeflerinin korunması ve mobil menü mantığını kapsar. Bunlar tarayıcıda görsel/mobil test veya gerçek reklam dönüşüm testi yerine geçmez.
