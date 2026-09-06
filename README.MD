# Bulk Wake-on-LAN (WoL) Trigger

[🇹🇷 Türkçe açıklama için aşağı kaydırın (Scroll down for Turkish)](#türkçe-açıklama)

A Python-based desktop application with a modern GUI (CustomTkinter) designed to send Wake-on-LAN (WoL) Magic Packets to multiple devices simultaneously. 

Instead of manually formatting MAC addresses, you can paste raw logs or mixed text directly into the application. The tool automatically extracts valid MAC addresses using Regex, filters out duplicates, and sends the broadcast packets in a separate thread to keep the UI responsive.

### Features
* **Smart Extraction:** Paste any raw text; the app automatically finds and extracts valid MAC addresses (e.g., `AA:BB:CC:DD:EE:FF` or `AA-BB-CC-DD-EE-FF`).
* **Profile Manager:** Save frequently used MAC address groups (labs, offices) as JSON profiles and load them with a single click.
* **Duplicate Prevention:** Uses `Set` logic to ensure a magic packet is sent only once per unique MAC address.
* **Non-Freezing UI:** Network operations run on a separate daemon thread, preventing the application from freezing during bulk broadcasts.
* **Modern Interface:** Built with CustomTkinter for a clean, dark-mode desktop experience.

### Prerequisites
1. Python 3.x installed on your system.
2. Install the required UI library:
   ```bash
   python -m pip install customtkinter

Important: Target computers must be connected via Ethernet, and the Wake-on-LAN feature must be enabled in both their BIOS/UEFI settings and OS network adapter settings.  

Run the script via terminal or command prompt:

"python bulk_wol.py"

Paste your MAC addresses into the text box and click the "Tümünü Uyandır (Broadcast)" button.




---------------------------------------------------------------------------------------------------
[Türkçe Açıklama](#türkçe-açıklama) 

# Toplu Wake-on-LAN (WoL) Tetikleyici

-Çoklu cihazlara aynı anda Wake-on-LAN (WoL) sihirli paketleri göndermek için CustomTkinter ile geliştirilmiş, modern arayüzlü Python masaüstü uygulaması.

-MAC adreslerini tek tek düzeltmek yerine, karmaşık log kayıtlarını veya notlarınızı doğrudan uygulamaya yapıştırabilirsiniz. Sistem, içindeki geçerli MAC adreslerini Regex ile otomatik olarak ayıklar, tekrar edenleri siler ve arayüzü dondurmamak için paket gönderimini arka planda (thread) yapar.

# Özellikler

-Akıllı Ayıklama: Herhangi bir metni yapıştırın; uygulama sadece geçerli MAC adreslerini (örn: AA:BB:CC:DD:EE:FF veya AA-BB-CC-DD-EE-FF) bulup kullanır.

-Profil Yöneticisi: Sık kullanılan cihaz gruplarını JSON formatında kaydedip tek tıkla geri yükleyin.

-Çift Kayıt Engelleme (Deduplication): Aynı MAC adresi birden fazla yazılsa bile sadece bir kez paket gönderilir.

-Akıcı Arayüz (Threading): Ağ işlemleri ayrı bir iş parçacığında yürütülür, toplu gönderim sırasında pencere "Yanıt Vermiyor" durumuna düşmez.

-Modern Tasarım: CustomTkinter ile hazırlanmış karanlık tema destekli sade arayüz.

# Gereksinimler

1-Sisteminizde Python 3.x kurulu olmalıdır.
2-Gerekli arayüz kütüphanesini kurun: `python -m pip install customtkinter`
3-Önemli: Hedef bilgisayarlar ağa Ethernet kablosu ile bağlı olmalı ve hem BIOS/UEFI ayarlarından hem de işletim sistemi ağ bağdaştırıcısı özelliklerinden Wake-on-LAN aktif edilmiş olmalıdır.


# Kullanım

Terminal veya komut satırı üzerinden betiği çalıştırın: `python bulk_wol.py`

Metin kutusuna MAC adreslerini yapıştırın ve "Tümünü Uyandır (Broadcast)" butonuna tıklayın.