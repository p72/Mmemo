import tkinter as tk
from tkinter import ttk, messagebox
import csv
import datetime
import os

FILENAME = "診療記録.csv"

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("選択なし", "削除する行を選択してください。")
        return

    values = tree.item(selected[0], "values")
    tree.delete(selected[0])

    # CSVから該当行を削除
    new_rows = []
    with open(FILENAME, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if tuple(row) != values:
                new_rows.append(row)

    with open(FILENAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    messagebox.showinfo("削除完了", "選択された行を削除しました。")
    load_data()

def edit_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("選択なし", "編集する行を選択してください。")
        return

    values = tree.item(selected[0], "values")

    # 入力欄にデータをセット
    entry_date.delete(0, tk.END)
    entry_date.insert(0, values[0])
    entry_name.delete(0, tk.END)
    entry_name.insert(0, values[1])
    entry_patient_no.delete(0, tk.END)
    entry_patient_no.insert(0, values[2])
    entry_age.delete(0, tk.END)
    entry_age.insert(0, values[3])
    gender_var.set(values[4])
    text_symptoms.delete("1.0", tk.END)
    text_symptoms.insert(tk.END, values[5])
    entry_diagnosis.delete(0, tk.END)
    entry_diagnosis.insert(0, values[6])

    # TreeviewとCSVから元データを削除
    delete_selected()

def duplicate_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("選択なし", "複製する行を選択してください。")
        return

    values = tree.item(selected[0], "values")
    #
    entry_date.delete(0, tk.END)
    entry_date.insert(0, values[0])
    entry_name.delete(0, tk.END)
    entry_name.insert(0, values[1])
    entry_patient_no.delete(0, tk.END)
    entry_patient_no.insert(0, values[2])
    entry_age.delete(0, tk.END)
    entry_age.insert(0, values[3])
    gender_var.set(values[4])
    text_symptoms.delete("1.0", tk.END)
    text_symptoms.insert(tk.END, values[5])
    entry_diagnosis.delete(0, tk.END)
    entry_diagnosis.insert(0, values[6])

def submit():
    date = entry_date.get()
    name = entry_name.get()
    patient_no = entry_patient_no.get()
    age = entry_age.get()
    gender = gender_var.get()
    symptoms = text_symptoms.get("1.0", tk.END).strip()
    diagnosis = entry_diagnosis.get()
    updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not (date and name and patient_no and age and gender and symptoms and diagnosis):
        messagebox.showwarning("未入力", "すべての項目を入力してください。")
        return

    # CSV全体を読み込み直して重複をチェック
    existing_rows = []
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            existing_rows = list(reader)

    new_row = [date, name, patient_no, age, gender, symptoms, diagnosis, updated_at]
    if new_row[:-1] in [row[:-1] for row in existing_rows]:
        messagebox.showwarning("重複警告", "このデータは既に存在しますが、保存を続行します。")

    # CSV保存
    with open(FILENAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(new_row)

    # Treeview更新
    load_data()

    # 入力リセット
    entry_date.delete(0, tk.END)
    entry_date.insert(0, datetime.date.today().isoformat())
    entry_name.delete(0, tk.END)
    entry_patient_no.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    gender_var.set(None)
    text_symptoms.delete("1.0", tk.END)
    entry_diagnosis.delete(0, tk.END)

    messagebox.showinfo("保存完了", "診療内容を保存しました。")

def search_data():
    keyword = entry_search.get().strip()
    if not keyword:
        load_data()
        return

    for row in tree.get_children():
        tree.delete(row)

    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if any(keyword in item for item in row):
                    tree.insert("", tk.END, values=row)

def load_data():
    # Treeviewの中身をリセット
    for row in tree.get_children():
        tree.delete(row)

    # CSVがあれば読み込む
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                tree.insert("", tk.END, values=row)

def sort_treeview(col, reverse):
    data = [(tree.set(k, col), k) for k in tree.get_children("")]
    try:
        data.sort(key=lambda t: float(t[0]) if t[0].replace('.', '', 1).isdigit() else t[0], reverse=reverse)
    except Exception:
        data.sort(reverse=reverse)

    for index, (val, k) in enumerate(data):
        tree.move(k, "", index)
    tree.heading(col, command=lambda: sort_treeview(col, not reverse))

def show_selected(event=None):
    selected = tree.selection()
    if not selected:
        text_view.config(state="normal")
        text_view.delete("1.0", tk.END)
        text_view.insert(tk.END, "診療内容が選択されていません。")
        text_view.config(state="disabled")
        return

    values = tree.item(selected[0], "values")
    info = (
        f"📅 診療日: {values[0]}\n"
        f"👤 名前: {values[1]}\n"
        f"🆔 患者No: {values[2]}\n"
        f"🎂 年齢: {values[3]}\n"
        f"⚧ 性別: {values[4]}\n"
        f"🤒 主訴・症状:\n{values[5]}\n"
        f"🩺 診断名: {values[6]}\n"
        f"🕒 更新日時: {values[7]}"
    )
    text_view.config(state="normal")
    text_view.delete("1.0", tk.END)
    text_view.insert(tk.END, info)
    text_view.config(state="disabled")

def toggle_treeview():
    if frame_tree.winfo_ismapped():
        frame_tree.pack_forget()
        btn_toggle_tree.config(text="📁 診療記録を表示")
    else:
        frame_tree.pack(padx=10, pady=10, fill="both", expand=True)
        btn_toggle_tree.config(text="📂 診療記録を非表示")

# メインウィンドウ
root = tk.Tk()
root.title("診療入力フォーム v1.0")
root.geometry("1000x700")

# ===== 入力欄エリア =====
frame_input = tk.LabelFrame(root, text="📝 診療入力")
frame_input.pack(pady=10)

left_frame = tk.LabelFrame(frame_input, text="👤 基本情報")
left_frame.pack(side=tk.LEFT, padx=10, pady=5, anchor="n")

right_frame = tk.LabelFrame(frame_input, text="📝 診療内容")
right_frame.pack(side=tk.LEFT, padx=10, pady=5, anchor="n")

# 診療日
tk.Label(left_frame, text="📅 診療日").grid(row=0, column=0, sticky="w")
entry_date = tk.Entry(left_frame, width=20)
entry_date.insert(0, datetime.date.today().isoformat())
entry_date.grid(row=0, column=1, sticky="w", padx=5, pady=3)

# 患者名
tk.Label(left_frame, text="👤 患者名").grid(row=1, column=0, sticky="w")
entry_name = tk.Entry(left_frame, width=20)
entry_name.grid(row=1, column=1, sticky="w", padx=5, pady=3)

# 患者No
tk.Label(left_frame, text="🆔 患者No").grid(row=2, column=0, sticky="w")
entry_patient_no = tk.Entry(left_frame, width=10)
entry_patient_no.grid(row=2, column=1, sticky="w", padx=5, pady=3)

# 年齢
tk.Label(left_frame, text="🎂 年齢").grid(row=3, column=0, sticky="w")
entry_age = tk.Entry(left_frame, width=10)
entry_age.grid(row=3, column=1, sticky="w", padx=5, pady=3)

# 性別
tk.Label(left_frame, text="⚧ 性別").grid(row=4, column=0, sticky="w")
gender_var = tk.StringVar()
frame_gender = tk.Frame(left_frame)
tk.Radiobutton(frame_gender, text="男性", variable=gender_var, value="男性").pack(side=tk.LEFT)
tk.Radiobutton(frame_gender, text="女性", variable=gender_var, value="女性").pack(side=tk.LEFT)
tk.Radiobutton(frame_gender, text="その他", variable=gender_var, value="その他").pack(side=tk.LEFT)
frame_gender.grid(row=4, column=1, sticky="w", padx=5, pady=3)

# 症状
tk.Label(right_frame, text="🤒 主訴 / 症状").grid(row=0, column=0, sticky="nw")
text_symptoms = tk.Text(right_frame, height=8, width=40)
text_symptoms.grid(row=0, column=1, padx=5, pady=3)

# 診断名
tk.Label(right_frame, text="🩺 診断名").grid(row=2, column=0, sticky="w")
entry_diagnosis = tk.Entry(right_frame, width=30)
entry_diagnosis.grid(row=2, column=1, sticky="w", padx=5, pady=3)

# ===== 操作メニュー =====
frame_buttons = tk.LabelFrame(root, text="⚙️ 操作メニュー")
frame_buttons.pack(pady=10)

tk.Label(frame_buttons, text="検索ワード").pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(frame_buttons, width=30)
entry_search.pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="検索", command=search_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="保存", command=submit).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="削除", command=delete_selected).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="編集", command=edit_selected).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="複製", command=duplicate_selected).pack(side=tk.LEFT, padx=5)

# ===== Treeviewエリア =====
frame_tree = tk.Frame(root)
frame_tree.pack(padx=10, pady=10, fill="both", expand=True)

columns = ("診療日", "名前", "患者No", "年齢", "性別", "症状", "診断名", "更新日時")
tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=5)

for col in columns:
    tree.heading(col, text=col, command=lambda c=col: sort_treeview(c, False))
    tree.column(col, width=100 if col not in ("症状", "更新日時") else 200)

tree.pack(fill="both", expand=True)

# 参照表示エリア
frame_view = tk.LabelFrame(root, text="診療内容（参照）")
frame_view.pack(fill="both", expand=False, padx=10, pady=5)

text_view = tk.Text(frame_view, height=8, wrap="word")
text_view.pack(fill="both", expand=True, padx=10, pady=5)
text_view.config(state="disabled")

# データ読み込み
load_data()
tree.bind("<<TreeviewSelect>>", show_selected)

btn_toggle_tree = tk.Button(root, text="📂 診療記録を非表示", command=toggle_treeview)
btn_toggle_tree.pack()

root.mainloop()