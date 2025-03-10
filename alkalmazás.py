# Schmidt László adatbáziskezelő
#
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import csv
from tkinter import filedialog
from tkinter import messagebox

def create_database():
    conn = sqlite3.connect('raktar.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS termekek (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nev TEXT,
            mennyiseg INTEGER,
            ar REAL
        )
    ''')
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect('raktar.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM termekek')
    rows = cursor.fetchall()
    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert('', tk.END, values=row)
    conn.close()

def add_product():
    nev = nev_entry.get()
    mennyiseg = mennyiseg_entry.get()
    ar = ar_entry.get()
    conn = sqlite3.connect('raktar.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO termekek (nev, mennyiseg, ar) VALUES (?, ?, ?)', (nev, mennyiseg, ar))
    conn.commit()
    conn.close()
    load_data()

def update_product():
    selected_items = tree.selection()
    if not selected_items:
        return
    answer = messagebox.askyesno('Módosítás', 'Biztosan módosítani szeretnéd a kijelölt sorokat?')
    if answer == True:
        for selected_item in selected_items:
            id = tree.item(selected_item)['values'][0]
            nev = nev_entry.get()
            mennyiseg = mennyiseg_entry.get()
            ar = ar_entry.get()
            conn = sqlite3.connect('raktar.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE termekek SET nev=?, mennyiseg=?, ar=? WHERE id=?', (nev, mennyiseg, ar, id))
            conn.commit()
            conn.close()
        load_data()

def delete_product():
    selected_items = tree.selection()
    if not selected_items:
        return
    answer = messagebox.askyesno('Törlés', 'Biztosan törölni szeretnéd a kijelölt sorokat?')
    if answer == True:
        for selected_item in selected_items:
            id = tree.item(selected_item)['values'][0]
            conn = sqlite3.connect('raktar.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM termekek WHERE id=?', (id,))
            conn.commit()
            conn.close()
        load_data()

def import_data():
    try:
        file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')], title='Importálás', bg='lightblue')
        if file_path:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                conn = sqlite3.connect('raktar.db')
                cursor = conn.cursor()
                for row in reader:
                    cursor.execute('INSERT INTO termekek (nev, mennyiseg, ar) VALUES (?, ?, ?)', row)
                conn.commit()
                conn.close()
            load_data()
    except FileNotFoundError:
        tk.messagebox.showerror('Hiba', 'A fájl nem található!')
    except Exception as e:
        tk.messagebox.showerror('Hiba', f'Hiba történt az importálás során: {e}')

def save_data():
    file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    if file_path:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Név', 'Mennyiség', 'Ár'])
            for item in tree.get_children():
                values = tree.item(item)['values']
                writer.writerow(values)

create_database()

root = tk.Tk()
root.title('RaktárMester ')

window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Címke hozzáadása
cimke = tk.Label(root, text='Schmidt László adatbáziskezelő 5/13GV (Üdvözöllek!)', font=('Helvetica', 16, 'bold'))
cimke.grid(row=0, columnspan=5, pady=10)

nev_label = tk.Label(root, text='Név: ️')
nev_label.grid(row=1, column=0)
nev_entry = tk.Entry(root)
nev_entry.grid(row=1, column=1)

mennyiseg_label = tk.Label(root, text='Mennyiség: ')
mennyiseg_label.grid(row=2, column=0)
mennyiseg_entry = tk.Entry(root)
mennyiseg_entry.grid(row=2, column=1)

ar_label = tk.Label(root, text='Ár: ')
ar_label.grid(row=3, column=0)
ar_entry = tk.Entry(root)
ar_entry.grid(row=3, column=1)

add_button = tk.Button(root, text='Hozzáadás ➕', command=add_product)
add_button.grid(row=4, column=0)
update_button = tk.Button(root, text='Módosítás ✏️', command=update_product)
update_button.grid(row=4, column=1)
delete_button = tk.Button(root, text='Törlés ️', command=delete_product)
delete_button.grid(row=4, column=2)
import_button = tk.Button(root, text='Importálás ', command=import_data)
import_button.grid(row=4, column=3)
save_button = tk.Button(root, text='Mentés ', command=save_data)
save_button.grid(row=4, column=4)

tree = ttk.Treeview(root, columns=('ID', 'Név', 'Mennyiség', 'Ár'), show='headings', selectmode=tk.EXTENDED)
tree.heading('ID', text='ID 🆔')
tree.heading('Név', text='Név ️')
tree.heading('Mennyiség', text='Mennyiség ')
tree.heading('Ár', text='Ár ')
tree.grid(row=5, columnspan=5)

load_data()

root.mainloop()
