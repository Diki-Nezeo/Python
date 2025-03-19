import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd 
import ttkbootstrap as tb

# Data ruangan yang sudah tersedia
test_rooms = {
    "FT-8": 100,
    "FT-9": 100,
    "GKT-LT4": 100,
    "GKT-LT5": 100,
    "AUDIT": 210,
    "FT-1": 65,
    "FT-6": 110,
    "FT-3": 100,
    "FT-4": 65,
    "FT-7": 115,
}

schedule = []
available_times = ["08:00", "12:00"]
available_days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
available_classes = ["Kelas A", "Kelas B", "Kelas C"]
available_semesters = ["Semester 1", "Semester 3", "Semester 5", "Semester 7"]

# Fungsi utama untuk Divide and Conquer
def divide_and_conquer_schedule(subjects):
    if len(subjects) == 1:
        matkul, kelas, semester, mahasiswa = subjects[0]
        return [assign_exam(matkul, kelas, semester, mahasiswa)]
    
    mid = len(subjects) // 2
    left_half = subjects[:mid]
    right_half = subjects[mid:]

    left_schedule = divide_and_conquer_schedule(left_half)
    right_schedule = divide_and_conquer_schedule(right_half)

    return left_schedule + right_schedule

# Fungsi untuk menjadwalkan satu mata kuliah
def assign_exam(matkul, kelas, semester, mahasiswa):
    suitable_rooms = sorted([room for room, capacity in test_rooms.items() if capacity >= mahasiswa], key=lambda r: test_rooms[r])
    
    if not suitable_rooms:
        return None

    for day in available_days:
        for time in available_times:
            if any(s["hari"] == day and s["jam"] == time and s["kelas"] == kelas and s["semester"] == semester for s in schedule):
                continue
            available_rooms = [room for room in suitable_rooms if not any(s["hari"] == day and s["jam"] == time and s["ruang"] == room for s in schedule)]
            if available_rooms:
                selected_room = available_rooms[0]
                new_schedule = {
                    "matkul": matkul,
                    "kelas": kelas,
                    "semester": semester,
                    "mahasiswa": mahasiswa,
                    "hari": day,
                    "jam": time,
                    "ruang": selected_room
                }
                schedule.append(new_schedule)
                return new_schedule
    return None

# Fungsi untuk menambahkan jadwal manual
def add_schedule_manual():
    matkul = entry_matkul.get()
    kelas = kelas_var.get()
    semester = semester_var.get()
    mahasiswa = entry_mahasiswa.get().strip()
    
    if not matkul or not kelas or not mahasiswa.isdigit() or not semester:
        messagebox.showerror("Error", "Harap isi semua data dengan benar.")
        return
    
    mahasiswa = int(mahasiswa)
    subjects = [(matkul, kelas, semester, mahasiswa)]
    divide_and_conquer_schedule(subjects)
    update_schedule()
    messagebox.showinfo("Sukses", f"Jadwal untuk {matkul} - {kelas} - {semester} berhasil ditambahkan.")

# Fungsi untuk memproses file Excel
def load_from_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
    if not file_path:
        return
    
    try:
        df = pd.read_excel(file_path)
        subjects = [(row['Mata Kuliah'], row['Kelas'], row['Semester'], int(row['Jumlah Mahasiswa'])) for _, row in df.iterrows()]
        divide_and_conquer_schedule(subjects)
        update_schedule()
        messagebox.showinfo("Sukses", "Jadwal berhasil diunggah dari file.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memuat file: {str(e)}")

# Fungsi untuk memperbarui tampilan jadwal
def update_schedule():
    for row in tree.get_children():
        tree.delete(row)
    for s in schedule:
        tree.insert("", "end", values=(s["matkul"], s["kelas"], s["semester"], s["mahasiswa"], s["hari"], s["jam"], s["ruang"]))

# Fungsi untuk menghapus jadwal yang dipilih
def delete_schedule():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih jadwal yang ingin dihapus.")
        return

    for item in selected_item:
        values = tree.item(item, "values")
        schedule[:] = [s for s in schedule if not (s["matkul"] == values[0] and s["kelas"] == values[1] and s["semester"] == values[2] and s["hari"] == values[4] and s["jam"] == values[5] and s["ruang"] == values[6])]
        tree.delete(item)
    
    messagebox.showinfo("Sukses", "Jadwal berhasil dihapus.")

def save_to_excel():
    if not schedule:
        messagebox.showwarning("Peringatan", "Tidak ada jadwal untuk disimpan.")
        return

    
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        return
    
    df = pd.DataFrame(schedule)
    try:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Sukses", "Jadwal berhasil disimpan sebagai Excel.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan file: {str(e)}")

#UI
root = tb.Window(themename="darkly")  # Menggunakan ttkbootstrap sejak awal
root.title("Penjadwalan Ujian")
root.geometry("1400x800")  # Atur ukuran lebih besar agar lebih nyaman

# Frame Input
frame_input = tb.Frame(root)
frame_input.pack(pady=10, padx=10, fill="x")

frame_input.grid_columnconfigure(0, weight=1)
frame_input.grid_columnconfigure(1, weight=1)

# Mata Kuliah
tb.Label(frame_input, text="Mata Kuliah", bootstyle="light", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=2)
entry_matkul = tb.Entry(frame_input)
entry_matkul.grid(row=0, column=1, padx=5, pady=2)

# Jumlah Mahasiswa
tb.Label(frame_input, text="Jumlah Mahasiswa", bootstyle="light", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=2)
entry_mahasiswa = tb.Entry(frame_input)
entry_mahasiswa.grid(row=1, column=1, padx=5, pady=2)

# Kelas
tb.Label(frame_input, text="Pilih Kelas", bootstyle="light", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=2)
kelas_var = tk.StringVar()
kelas_dropdown = tb.Combobox(frame_input, textvariable=kelas_var, values=["Kelas A", "Kelas B", "Kelas C"], state="readonly")
kelas_dropdown.grid(row=2, column=1, padx=5, pady=2)
kelas_dropdown.current(0)

# Semester
tb.Label(frame_input, text="Pilih Semester", bootstyle="light", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=5, pady=2)
semester_var = tk.StringVar()
semester_dropdown = tb.Combobox(frame_input, textvariable=semester_var, values=["Semester 1", "Semester 3", "Semester 5", "Semester 7"], state="readonly")
semester_dropdown.grid(row=3, column=1, padx=5, pady=2)
semester_dropdown.current(0)

# Frame Tombol
frame_buttons = tb.Frame(root)
frame_buttons.pack(pady=10)

tb.Button(frame_buttons, text="Tambah Jadwal", command=add_schedule_manual, bootstyle="success").grid(row=0, column=0, padx=5, pady=5)
tb.Button(frame_buttons, text="Unggah File Excel", command=load_from_excel, bootstyle="primary").grid(row=0, column=1, padx=5, pady=5)
tb.Button(frame_buttons, text="Hapus Jadwal", command=delete_schedule, bootstyle="danger").grid(row=1, column=0, padx=5, pady=5)
tb.Button(frame_buttons, text="Unduh Excel",command=save_to_excel, bootstyle="warning").grid(row=1, column=1, padx=5, pady=5)

# Frame Table
frame_table = tb.Frame(root)
frame_table.pack(fill="both", expand=True)

tree_scroll = tb.Scrollbar(frame_table)
tree_scroll.pack(side="right", fill="y")

tree = tb.Treeview(frame_table, columns=("Matkul", "Kelas", "Semester", "Mahasiswa", "Hari", "Jam", "Ruangan"), show="headings", yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree.yview)

for col in ("Matkul", "Kelas", "Semester", "Mahasiswa", "Hari", "Jam", "Ruangan"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill="both", expand=True)

root.mainloop()
