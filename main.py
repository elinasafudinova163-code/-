import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data_file = "trainings.json"
        self.trainings = self.load_data()

        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = tk.Entry(self.root)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить тренировку", command=self.add_training).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Фильтры
        tk.Label(self.root, text="Фильтр по типу:").grid(row=4, column=0, padx=5, pady=5)
        self.filter_type = ttk.Combobox(self.root, values=["Все"] + list(set(t["type"] for t in self.trainings)))
        self.filter_type.set("Все")
        self.filter_type.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по дате (YYYY-MM-DD):").grid(row=5, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтры", command=self.apply_filters).grid(
            row=6, column=0, columnspan=2, pady=10
        )

        # Таблица
        columns = ("Дата", "Тип", "Длительность")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def validate_input(self, date_str, duration_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD.")
            return False

        try:
            duration = float(duration_str)
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом.")
            return False

        return True

    def add_training(self):
        date = self.date_entry.get()
        training_type = self.type_entry.get()
        duration = self.duration_entry.get()

        if not self.validate_input(date, duration):
            return

        training = {
            "date": date,
            "type": training_type,
            "duration": float(duration)
        }
        self.trainings.append(training)
        self.save_data()
        self.update_table()
        self.clear_entries()

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def update_table(self, filtered_trainings=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        trainings_to_show = filtered_trainings if filtered_trainings is not None else self.trainings
        for training in trainings_to_show:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                f"{training['duration']} мин"
            ))

    def apply_filters(self):
        filter_type = self.filter_type.get()
        filter_date = self.filter_date.get()

        filtered = self.trainings

        if filter_type != "Все":
            filtered = [t for t in filtered if t["type"] == filter_type]

        if filter_date:
            try:
                datetime.strptime(filter_date, "%Y-%m-%d")
                filtered = [t for t in filtered if t["date"] == filter_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты для фильтра.")
                return

        self.update_table(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
