import os
import json
import base64
import datetime

USER_FILE = "users.json"
NOTES_FILE = "notes.json"

# ------------------ Helper ------------------
def load_data(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return {}
            return data
        except json.JSONDecodeError:
            return {}

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def encode_text(text):
    return base64.b64encode(text.encode()).decode()

def decode_text(text_b64):
    try:
        return base64.b64decode(text_b64.encode()).decode()
    except:
        return "[ERROR: data rusak]"

# ------------------ Catatan Functions ------------------
def tambah_catatan(username, catatan, kunci=""):
    """Menambahkan catatan dengan timestamp"""
    notes = load_data(NOTES_FILE)
    
    if username not in notes:
        notes[username] = []
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notes[username].append({
        "note": encode_text(catatan),
        "lock": encode_text(kunci) if kunci else "",
        "time": timestamp
    })
    
    save_data(NOTES_FILE, notes)
    print("✔ Catatan ditambahkan.")

def lihat_catatan(username, tampilkan_semua=False):
    """Menampilkan daftar catatan"""
    notes = load_data(NOTES_FILE)
    user_notes = notes.get(username, [])
    
    if not user_notes:
        print("⚠ Belum ada catatan.")
        return user_notes
    
    if not tampilkan_semua:
        print("\n--- Daftar Catatan ---")
        for i, item in enumerate(user_notes, 1):
            lock_status = "🔒" if item.get("lock") else "🔓"
            preview = decode_text(item["note"])[:30] + "..." if len(decode_text(item["note"])) > 30 else decode_text(item["note"])
            if item.get("lock"):
                print(f"{i}. {lock_status} [Catatan Terkunci] - {item.get('time', 'Tanpa waktu')}")
            else:
                print(f"{i}. {lock_status} {preview} - {item.get('time', 'Tanpa waktu')}")
    
    return user_notes

def buka_catatan(username, index):
    """Membuka isi catatan tertentu"""
    notes = load_data(NOTES_FILE)
    user_notes = notes.get(username, [])
    
    if 0 <= index < len(user_notes):
        item = user_notes[index]
        
        if item.get("lock"):
            pw = input("Masukkan kunci catatan: ")
            if encode_text(pw) == item["lock"]:
                print(f"\n📝 Catatan [{item.get('time', 'Tanpa waktu')}]:")
                print(decode_text(item["note"]))
            else:
                print("❌ Kunci salah.")
        else:
            print(f"\n📝 Catatan [{item.get('time', 'Tanpa waktu')}]:")
            print(decode_text(item["note"]))
    else:
        print("❌ Nomor catatan tidak valid.")

def edit_catatan(username, index, new_text, new_lock=""):
    """Mengedit catatan"""
    notes = load_data(NOTES_FILE)
    user_notes = notes.get(username, [])
    
    if 0 <= index < len(user_notes):
        item = user_notes[index]
        
        if item.get("lock"):
            pw = input("Masukkan kunci saat ini: ")
            if encode_text(pw) != item["lock"]:
                print("❌ Kunci salah.")
                return False
        
        # Update timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item["note"] = encode_text(new_text)
        item["time"] = timestamp
        
        if new_lock is not None:
            item["lock"] = encode_text(new_lock) if new_lock else ""
        
        save_data(NOTES_FILE, notes)
        print("✔ Catatan berhasil diedit.")
        return True
    else:
        print("❌ Nomor catatan tidak valid.")
        return False

def hapus_catatan(username, index):
    """Menghapus catatan"""
    notes = load_data(NOTES_FILE)
    user_notes = notes.get(username, [])
    
    if 0 <= index < len(user_notes):
        item = user_notes[index]
        
        if item.get("lock"):
            pw = input("Masukkan kunci catatan: ")
            if encode_text(pw) != item["lock"]:
                print("❌ Kunci salah.")
                return False
        
        # Konfirmasi penghapusan
        konfirmasi = input(f"Yakin hapus catatan ini? (y/n): ")
        if konfirmasi.lower() != 'y':
            print("❌ Penghapusan dibatalkan.")
            return False
        
        del user_notes[index]
        save_data(NOTES_FILE, notes)
        print("✔ Catatan dihapus.")
        return True
    else:
        print("❌ Nomor catatan tidak valid.")
        return False

# ------------------ Main ------------------
def main():
    while True:
        print("\n" + "="*30)
        print("        ASISTEN SHADOW")
        print("="*30)
        print("  1. Register")
        print("  2. Login")
        print("  3. Keluar")
        print("-"*30)
        
        pilih = input("Pilih menu (1-3): ").strip()

        if pilih == "1":
            print("\n--- REGISTRASI ---")
            username = input("Buat username: ").strip()
            password = input("Buat password: ").strip()
            
            users = load_data(USER_FILE)
            
            if not username or not password:
                print("❌ Username dan password tidak boleh kosong!")
            elif username in users:
                print("❌ Username sudah ada!")
            else:
                users[username] = encode_text(password)  # Simpan password terenkripsi
                save_data(USER_FILE, users)
                print("✔ Registrasi berhasil, silakan login.")

        elif pilih == "2":
            print("\n--- LOGIN ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            users = load_data(USER_FILE)
            
            if username in users and users[username] == encode_text(password):
                print(f"\n✔ Selamat datang {username}!")
                
                while True:
                    print("\n" + "-"*30)
                    print(f"     MENU UTAMA - {username}")
                    print("-"*30)
                    print("  1. Tambah catatan")
                    print("  2. Lihat semua catatan")
                    print("  3. Buka catatan")
                    print("  4. Edit catatan")
                    print("  5. Hapus catatan")
                    print("  6. Logout")
                    print("-"*30)
                    
                    pilih2 = input("Pilih menu (1-6): ").strip()

                    if pilih2 == "1":
                        print("\n--- TAMBAH CATATAN ---")
                        note = input("Tulis catatan: ").strip()
                        if not note:
                            print("❌ Catatan tidak boleh kosong!")
                            continue
                        
                        lock = input("Kunci catatan? (biarkan kosong jika tidak): ").strip()
                        tambah_catatan(username, note, lock)

                    elif pilih2 == "2":
                        print("\n--- SEMUA CATATAN ---")
                        lihat_catatan(username)

                    elif pilih2 == "3":
                        user_notes = lihat_catatan(username, tampilkan_semua=False)
                        if user_notes:
                            pilih_cat = input("\nBuka catatan nomor (atau 0 untuk kembali): ").strip()
                            if pilih_cat.isdigit():
                                idx = int(pilih_cat) - 1
                                if idx == -1:
                                    continue
                                buka_catatan(username, idx)

                    elif pilih2 == "4":
                        user_notes = lihat_catatan(username, tampilkan_semua=False)
                        if user_notes:
                            pilih_cat = input("\nEdit catatan nomor (atau 0 untuk kembali): ").strip()
                            if pilih_cat.isdigit():
                                idx = int(pilih_cat) - 1
                                if idx == -1:
                                    continue
                                
                                new_note = input("Tulis isi baru: ").strip()
                                if not new_note:
                                    print("❌ Catatan tidak boleh kosong!")
                                    continue
                                
                                new_lock = input("Kunci baru (biarkan kosong jika tidak diubah, ketik 'hapus' untuk menghapus kunci): ").strip()
                                
                                if new_lock.lower() == 'hapus':
                                    edit_catatan(username, idx, new_note, "")
                                else:
                                    edit_catatan(username, idx, new_note, new_lock)

                    elif pilih2 == "5":
                        user_notes = lihat_catatan(username, tampilkan_semua=False)
                        if user_notes:
                            pilih_cat = input("\nHapus catatan nomor (atau 0 untuk kembali): ").strip()
                            if pilih_cat.isdigit():
                                idx = int(pilih_cat) - 1
                                if idx == -1:
                                    continue
                                hapus_catatan(username, idx)

                    elif pilih2 == "6":
                        print("✔ Logout berhasil.")
                        break

                    else:
                        print("❌ Pilihan tidak valid. Silakan pilih 1-6.")

            else:
                print("❌ Username atau password salah!")

        elif pilih == "3":
            print("\n✔ Terima kasih telah menggunakan Asisten Shadow!")
            break

        else:
            print("❌ Pilihan tidak valid. Silakan pilih 1-3.")

if __name__ == "__main__":
    main()
