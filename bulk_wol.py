import customtkinter as ctk
import tkinter as tk
import socket
import re
import threading
import json
import os

# Arayüz teması
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

PROFILE_FILE = "wol_profiles.json"

class BulkWoLApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Toplu WoL Tetikleyici v1.1")
        self.geometry("600x750")
        
        self.profiles = self._load_profiles_from_file()

        # --- BAŞLIK ---
        self.label = ctk.CTkLabel(self, text="MAC Adreslerini Girin", font=("Segoe UI", 18, "bold"))
        self.label.pack(pady=(20, 5), padx=20, anchor="w")
        
        self.sub_label = ctk.CTkLabel(self, text="(Format: AA:BB:CC:DD:EE:FF veya AA-BB-CC-DD-EE-FF. Açıklama yazabilirsiniz.)", text_color="gray", font=("Segoe UI", 12))
        self.sub_label.pack(pady=(0, 10), padx=20, anchor="w")

        # --- PROFİL YÖNETİM PANELİ ---
        self.profile_frame = ctk.CTkFrame(self)
        self.profile_frame.pack(pady=5, padx=20, fill="x")

        # Profil Seçici (Combobox)
        self.profile_var = ctk.StringVar(value="Profil Seçin...")
        self.profile_menu = ctk.CTkOptionMenu(self.profile_frame, variable=self.profile_var, values=self._get_profile_names(), command=self.load_profile)
        self.profile_menu.pack(side="left", padx=10, pady=10)

        # Yeni Profil Adı Girdisi
        self.profile_entry = ctk.CTkEntry(self.profile_frame, placeholder_text="Yeni profil adı...", width=150)
        self.profile_entry.pack(side="left", padx=(0, 10), pady=10)

        # Kaydet Butonu
        self.save_btn = ctk.CTkButton(self.profile_frame, text="Kaydet", width=80, fg_color="#2E7D32", hover_color="#1B5E20", command=self.save_profile)
        self.save_btn.pack(side="left", padx=(0, 10), pady=10)

        # Sil Butonu
        self.delete_btn = ctk.CTkButton(self.profile_frame, text="Sil", width=80, fg_color="#C62828", hover_color="#8E0000", command=self.delete_profile)
        self.delete_btn.pack(side="left", padx=(0, 10), pady=10)

        # --- MAC GİRİŞ ALANI ---
        self.textbox = ctk.CTkTextbox(self, width=560, height=350, font=("Consolas", 14))
        self.textbox.pack(pady=10, padx=20)

        # --- TETİKLEME BUTONU ---
        self.send_button = ctk.CTkButton(self, text="Tümünü Uyandır (Broadcast)", font=("Segoe UI", 14, "bold"), height=40, command=self.trigger_wol)
        self.send_button.pack(pady=15)

        # --- DURUM ÇUBUĞU ---
        self.status_label = ctk.CTkLabel(self, text="Bekleniyor...", text_color="gray", font=("Segoe UI", 14))
        self.status_label.pack(pady=5)

    # --- JSON PROFİL METOTLARI ---
    def _load_profiles_from_file(self):
        if os.path.exists(PROFILE_FILE):
            try:
                with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_profiles_to_file(self):
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.profiles, f, indent=4, ensure_ascii=False)

    def _get_profile_names(self):
        names = list(self.profiles.keys())
        return names if names else ["Profil Bulunamadı"]

    def save_profile(self):
        profile_name = self.profile_entry.get().strip()
        if not profile_name:
            self.status_label.configure(text="Lütfen kaydetmek için bir profil adı yazın!", text_color="#FFCA28")
            return
            
        raw_text = self.textbox.get("1.0", "end-1c")
        self.profiles[profile_name] = raw_text
        self._save_profiles_to_file()
        
        # Menüyü güncelle
        self.profile_menu.configure(values=self._get_profile_names())
        self.profile_var.set(profile_name)
        self.profile_entry.delete(0, "end")
        self.status_label.configure(text=f"'{profile_name}' profili başarıyla kaydedildi.", text_color="#66BB6A")

    def load_profile(self, selected_profile):
        if selected_profile in self.profiles:
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", self.profiles[selected_profile])
            self.status_label.configure(text=f"'{selected_profile}' profili yüklendi.", text_color="#42A5F5")

    def delete_profile(self):
        selected_profile = self.profile_var.get()
        if selected_profile in self.profiles:
            del self.profiles[selected_profile]
            self._save_profiles_to_file()
            
            # Menüyü güncelle
            new_names = self._get_profile_names()
            self.profile_menu.configure(values=new_names)
            self.profile_var.set(new_names[0] if new_names != ["Profil Bulunamadı"] else "Profil Seçin...")
            self.textbox.delete("1.0", "end")
            self.status_label.configure(text=f"'{selected_profile}' profili silindi.", text_color="#FF5252")

    # --- WOL METOTLARI (Aynı kaldı) ---
    def wake_on_lan(self, macaddress):
        try:
            mac_clean = macaddress.replace("-", "").replace(":", "")
            if len(mac_clean) != 12: return False
            data = bytes.fromhex('FF' * 6 + mac_clean * 16)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(data, ('255.255.255.255', 9))
            sock.close()
            return True
        except Exception as e:
            return False

    def trigger_wol(self):
        raw_text = self.textbox.get("1.0", "end-1c")
        mac_list = re.findall(r'(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', raw_text)
        mac_list = list(set(mac_list))
        
        if not mac_list:
            self.status_label.configure(text="Girilen metinde geçerli MAC adresi bulunamadı!", text_color="#FF5252")
            return

        self.send_button.configure(state="disabled")
        self.status_label.configure(text=f"{len(mac_list)} cihaz tetikleniyor...", text_color="#FFCA28")
        threading.Thread(target=self._send_packets, args=(mac_list,), daemon=True).start()

    def _send_packets(self, mac_list):
        success_count = 0
        for mac in mac_list:
            if self.wake_on_lan(mac):
                success_count += 1
        self.after(0, self._update_ui_post_send, success_count, len(mac_list))

    def _update_ui_post_send(self, success_count, total_count):
        self.status_label.configure(text=f"Tetikleme Tamamlandı: {success_count}/{total_count} paketi gönderildi.", text_color="#66BB6A")
        self.send_button.configure(state="normal")

if __name__ == "__main__":
    app = BulkWoLApp()
    app.mainloop()