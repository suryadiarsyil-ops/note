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
    with open(filename, "r") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return {}
            return data
        except json.JSONDecodeError:
            return {}

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def encode_text(text):
    return base64.b64encode(text.encode()).decode()

def decode_text(text_b64):
    try:
        return base64.b64decode(text_b64.encode()).decode()
    except:
        return "[ERROR: data rusak]"
import datetime

# --- Tambah catatan dengan timestamp ---
def tambah_catatan(username, catatan):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = load_data()
    if username not in data["notes"]:
        data["notes"][username] = []
    data["notes"][username].append({
        "text": catatan,
        "time": timestamp
    })
    save_data(data)
    print("✔ Catatan ditambahkan.")

# --- Lihat catatan dengan timestamp ---
def lihat_catatan(username):
    data = load_data()
    notes = data["notes"].get(username, [])
    if not notes:
        print("⚠ Belum ada catatan.")
    else:
        print("\n--- Catatan ---")
        for i, note in enumerate(notes, 1):
            print(f"{i}. [{note['time']}] {note['text']}")
   
# --- Edit catatan ---
def edit_catatan(username, index, new_text):
    data = load_data()
    notes = data["notes"].get(username, [])
    if 0 <= index < len(notes):
        notes[index]["text"] = new_text
        save_data(data)
        print("✔ Catatan berhasil diedit.")
    else:
        print("❌ Nomor catatan tidak valid.")

# --- Hapus catatan ---
def hapus_catatan(username, index):
    data = load_data()
    notes = data["notes"].get(username, [])
    if 0 <= index < len(notes):
        deleted = notes.pop(index)
        save_data(data)
        print(f"✔ Catatan '{deleted['text']}' berhasil dihapus.")
    else:
        print("❌ Nomor catatan tidak valid.")                     
            
# ------------------ Main ------------------
def main():
    users = load_data(USER_FILE)
    notes = load_data(NOTES_FILE)

    while True:
        print("\n=== Asisten Shadow ===")
        print("1. Register")
        print("2. Login")
        print("3. Keluar")
        pilih = input("Pilih: ")

        if pilih == "1":
            username = input("Buat username: ")
            password = input("Buat password: ")
            if username in users:
                print("❌ Username sudah ada!")
            else:
                users[username] = password
                save_data(USER_FILE, users)
                print("✔ Registrasi berhasil, silakan login.")

        elif pilih == "2":
            username = input("Username: ")
            password = input("Password: ")
            if users.get(username) == password:
                print(f"✔ Selamat datang {username}!")
                while True:
                    print("\n--- MENU ---")
                    print("1. Tambah catatan")
                    print("2. Lihat catatan")
                    print("3. Edit catatan")
                    print("4. Hapus catatan")
                    print("5. Logout")
                    pilih2 = input("Pilih: ")

                    if pilih2 == "1":  # tambah
                        note = input("Tulis catatan: ")
                        lock = input("Kunci catatan? (biarkan kosong jika tidak): ")
                        enc_note = encode_text(note)
                        enc_lock = encode_text(lock) if lock else ""

                        if username not in notes:
                            notes[username] = []
                        notes[username].append({"note": enc_note, "lock": enc_lock})
                        save_data(NOTES_FILE, notes)
                        print("✔ Catatan ditambahkan.")

                    elif pilih2 == "2":  # lihat
                        print("\n--- Catatan ---")
                        user_notes = notes.get(username, [])
                        if not user_notes:
                            print("(Belum ada catatan)")
                        else:
                            for i, item in enumerate(user_notes, 1):
                                lock = item.get("lock", "")
                                if lock:
                                    print(f"{i}. 🔒 Catatan terkunci")
                                else:
                                    print(f"{i}. {decode_text(item['note'])}")

                            pilih_cat = input("\nBuka catatan nomor (atau ENTER untuk kembali): ")
                            if pilih_cat.isdigit():
                                idx = int(pilih_cat) - 1
                                if 0 <= idx < len(user_notes):
                                    item = user_notes[idx]
                                    if item.get("lock"):
                                        pw = input("Masukkan kunci catatan: ")
                                        if encode_text(pw) == item["lock"]:
                                            print("✔ Catatan:", decode_text(item["note"]))
                                        else:
                                            print("❌ Kunci salah.")
                                    else:
                                        print("✔ Catatan:", decode_text(item["note"]))

                    elif pilih2 == "3":  # edit
                        user_notes = notes.get(username, [])
                        if not user_notes:
                            print("(Belum ada catatan)")
                        else:
                            for i, item in enumerate(user_notes, 1):
                                print(f"{i}. {'🔒' if item.get('lock') else ''} {decode_text(item['note']) if not item.get('lock') else 'Catatan terkunci'}")

                            pilih_cat = input("\nEdit catatan nomor: ")
                            if pilih_cat.isdigit():
                                idx = int(pilih_cat) - 1
                                if 0 <= idx < len(user_notes):
                                    item = user_notes[idx]
                                    if item.get("lock"):
                                        pw = input("Masukkan kunci catatan: ")
                                        if encode_text(pw) != item["lock"]:
                                            print("❌ Kunci salah.")
                                            continue
                                    new_note = input("Tulis isi baru: ")
                                    new_lock = input("Kunci baru (biarkan kosong jika tetap): ")
                                    item["note"] = encode_text(new_note)
                                    item["lock"] = encode_text(new_lock) if new_lock else item.get("lock", "")
                                    save_data(NOTES_FILE, notes)
                                    print("✔ Catatan berhasil diupdate.")

                    elif pilih2 == "4":  # hapus
                        user_notes = notes.get(username, [])
                        if not user_notes:
                            print("(Belum ada catatan)")
                        else:
                            for i, item in enumerate(user_notes, 1):
                                print(f"{i}. {'🔒' if item.get('lock') else ''} {decode_text(item['note']) if not item.get('lock') else 'Catatan terkunci'}")

                            pilih_cat = input("\nHapus catatan nomor: ")
                            if pilih_cat.isdigit():
                                idx = int(pilih_cat) - 1
                                if 0 <= idx < len(user_notes):
                                    item = user_notes[idx]
                                    if item.get("lock"):
                                        pw = input("Masukkan kunci catatan: ")
                                        if encode_text(pw) != item["lock"]:
                                            print("❌ Kunci salah.")
                                            continue
                                    del user_notes[idx]
                                    save_data(NOTES_FILE, notes)
                                    print("✔ Catatan dihapus.")

                    elif pilih2 == "5":
                        print("✔ Logout berhasil.")
                        break
                    else:
                        print("❌ Pilihan tidak valid.")

            else:
                print("❌ Username atau password salah!")

        elif pilih == "3":
            print("✔ Keluar.")
            break

        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    main()
