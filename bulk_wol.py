import customtkinter as ctk
import socket
import re
import threading

# Arayüz teması
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BulkWoLApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Toplu WoL Tetikleyici")
        self.geometry("550x650")

        # Başlık ve Açıklama
        self.label = ctk.CTkLabel(self, text="MAC Adreslerini Girin", font=("Segoe UI", 18, "bold"))
        self.label.pack(pady=(20, 5), padx=20, anchor="w")
        
        self.sub_label = ctk.CTkLabel(self, text="(Format: AA:BB:CC:DD:EE:FF veya AA-BB-CC-DD-EE-FF. Her satıra bir tane)", text_color="gray", font=("Segoe UI", 12))
        self.sub_label.pack(pady=(0, 10), padx=20, anchor="w")

        # MAC giriş alanı
        self.textbox = ctk.CTkTextbox(self, width=500, height=400, font=("Consolas", 14))
        self.textbox.pack(pady=10, padx=20)

        # Tetikleme Butonu
        self.send_button = ctk.CTkButton(self, text="Tümünü Uyandır (Broadcast)", font=("Segoe UI", 14, "bold"), height=40, command=self.trigger_wol)
        self.send_button.pack(pady=15)

        # Durum Çubuğu
        self.status_label = ctk.CTkLabel(self, text="Bekleniyor...", text_color="gray", font=("Segoe UI", 14))
        self.status_label.pack(pady=5)

    def wake_on_lan(self, macaddress):
        """Tek bir MAC adresi için Magic Packet oluşturur ve UDP üzerinden yayınlar."""
        try:
            # Sadece hex karakterlerini bırak
            mac_clean = macaddress.replace("-", "").replace(":", "")
            if len(mac_clean) != 12:
                return False
            
            # Magic Packet: 6 byte FF + 16 kez MAC adresi
            data = bytes.fromhex('FF' * 6 + mac_clean * 16)
            
            # Paketi yerel ağa (255.255.255.255) port 9 üzerinden gönder
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(data, ('255.255.255.255', 9))
            sock.close()
            return True
        except Exception as e:
            print(f"Hata ({macaddress}): {e}")
            return False

    def trigger_wol(self):
        raw_text = self.textbox.get("1.0", "end-1c")
        
        # Sadece geçerli MAC adresi formatlarını seç (Regex)
        mac_list = re.findall(r'(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', raw_text)
        
        # Çift kayıtları (duplicate) kaldır
        mac_list = list(set(mac_list))
        
        if not mac_list:
            self.status_label.configure(text="Girilen metinde geçerli MAC adresi bulunamadı!", text_color="#FF5252")
            return

        self.send_button.configure(state="disabled")
        self.status_label.configure(text=f"{len(mac_list)} farklı cihaz için paketler hazırlanıyor...", text_color="#FFCA28")
        
        # Arayüzü kitlememek için arka planda çalıştır
        threading.Thread(target=self._send_packets, args=(mac_list,), daemon=True).start()

    def _send_packets(self, mac_list):
        success_count = 0
        for mac in mac_list:
            if self.wake_on_lan(mac):
                success_count += 1
        
        # İşlem bitince UI'ı ana thread'de güncelle
        self.after(0, self._update_ui_post_send, success_count, len(mac_list))

    def _update_ui_post_send(self, success_count, total_count):
        self.status_label.configure(text=f"İşlem Tamamlandı: {success_count}/{total_count} cihaza Magic Packet gönderildi.", text_color="#66BB6A")
        self.send_button.configure(state="normal")

if __name__ == "__main__":
    app = BulkWoLApp()
    app.mainloop()