import tkinter as tk
from tkinter import ttk, messagebox

# Data ruangan yang sudah tersedia
test_rooms = {
    "FT-8": 100,
    "FT-9": 100,
    "GKT-LT4": 100,
    "GKT-LT5": 100,
    "AUDIT" : 210,
    "FT-1" : 65,
    "FT-6": 110,
    "FT-3": 100,
    "FT-4":65,
    "FT-7": 115,
}

schedule = []  # Tempat menyimpan jadwal yang sudah dibuat
available_times = ["08:00", "10:00", "12:00", "14:00"]
available_days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
available_classes = ["Kelas A", "Kelas B", "Kelas C"]

# Fungsi mencari ruangan menggunakan Greedy Algorithm
def find_room_greedy(rooms, mahasiswa):
    sorted_rooms = sorted(rooms.items(), key=lambda x: x[1])
    for room, capacity in sorted_rooms:
        if capacity >= mahasiswa:
            return room
    return None

# Fungsi untuk menambahkan jadwal ujian
def add_schedule():
    matkul = entry_matkul.get()
    kelas = kelas_var.get()
    mahasiswa = entry_mahasiswa.get().strip()
    
    if not matkul or not kelas or not mahasiswa.isdigit():
        messagebox.showerror("Error", "Harap isi mata kuliah, pilih kelas, dan jumlah mahasiswa dengan benar.")
        return
    
    mahasiswa = int(mahasiswa)
    if mahasiswa > max(test_rooms.values(), default=0):
        messagebox.showerror("Error", "Jumlah mahasiswa melebihi kapasitas ruangan terbesar.")
        return

    suitable_rooms = [room for room, capacity in test_rooms.items() if capacity >= mahasiswa]
    if not suitable_rooms:
        messagebox.showerror("Error", "Tidak ada ruangan yang sesuai.")
        return

    for day in available_days:
        for time in available_times:
            if any(s["hari"] == day and s["jam"] == time and s["kelas"] == kelas for s in schedule):
                continue  
            
            available_rooms = [room for room in suitable_rooms if not any(
                s["hari"] == day and s["jam"] == time and s["ruang"] == room for s in schedule)]
            
            if available_rooms:
                selected_room = find_room_greedy({room: test_rooms[room] for room in available_rooms}, mahasiswa)
                
                if selected_room:
                    schedule.append({
                        "matkul": matkul,
                        "kelas": kelas,
                        "mahasiswa": mahasiswa,
                        "hari": day,
                        "jam": time,
                        "ruang": selected_room
                    })
                    update_schedule()
                    messagebox.showinfo("Sukses", f"Jadwal untuk {matkul} - {kelas} berhasil ditambahkan.")
                    return

    messagebox.showerror("Gagal", "Tidak dapat menemukan jadwal yang tersedia.")

# Fungsi untuk menghapus jadwal yang dipilih
def delete_schedule():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih jadwal yang ingin dihapus.")
        return

    for item in selected_item:
        values = tree.item(item, "values")
        schedule[:] = [s for s in schedule if not (s["matkul"] == values[0] and s["kelas"] == values[1] and s["hari"] == values[3] and s["jam"] == values[4] and s["ruang"] == values[5])]
        tree.delete(item)

    messagebox.showinfo("Sukses", "Jadwal berhasil dihapus.")

# Fungsi untuk menampilkan jadwal
def update_schedule():
    for row in tree.get_children():
        tree.delete(row)
    for s in schedule:
        tree.insert("", "end", values=(s["matkul"], s["kelas"], s["mahasiswa"], s["hari"], s["jam"], s["ruang"]))

# UI
root = tk.Tk()
root.title("Penjadwalan Ujian - Greedy Algorithm")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Mata Kuliah").grid(row=0, column=0)
entry_matkul = tk.Entry(frame_input)
entry_matkul.grid(row=0, column=1)

tk.Label(frame_input, text="Pilih Kelas").grid(row=2, column=0)
kelas_var = tk.StringVar()
kelas_dropdown = ttk.Combobox(frame_input, textvariable=kelas_var, values=available_classes, state="readonly")
kelas_dropdown.grid(row=2, column=1)
kelas_dropdown.current(0)

tk.Label(frame_input, text="Jumlah Mahasiswa").grid(row=1, column=0)
entry_mahasiswa = tk.Entry(frame_input)
entry_mahasiswa.grid(row=1, column=1)

tk.Button(frame_input, text="Tambah Jadwal", command=add_schedule).grid(row=3, column=0, pady=10)
tk.Button(frame_input, text="Hapus Jadwal", command=delete_schedule).grid(row=3, column=1, pady=10)

tree = ttk.Treeview(root, columns=("Matkul", "Kelas", "Mahasiswa", "Hari", "Jam", "Ruangan"), show="headings")
for col in ("Matkul", "Kelas", "Mahasiswa", "Hari", "Jam", "Ruangan"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(pady=10)

root.mainloop()
