import tkinter as tk
from tkinter import messagebox, simpledialog
import random


class Sudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Судоку")
        self.root.geometry("450x400")  # Начальный размер окна
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        self.create_menu()
        self.create_grid()
        self.generate_sudoku()
        self.remove_numbers()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Игра", menu=file_menu)
        file_menu.add_command(label="Настройки", command=self.settings)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

    def settings(self):
        try:
            width = simpledialog.askinteger("Настройки", "Введите ширину окна:")
            height = simpledialog.askinteger("Настройки", "Введите высоту окна:")
            if width and height:
                self.root.geometry(f"{width}x{height}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=3, font=('Times New Roman', 18), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.bind("<KeyRelease>", self.validate_input)
                self.entries[i][j] = entry

    def generate_sudoku(self):
        if not self.fill_grid():
            messagebox.showerror("Ошибка", "Не удалось сгенерировать Судоку.")
            return

    def fill_grid(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True  # Все ячейки заполнены

        row, col = empty_cell
        numbers = list(range(1, 10))
        random.shuffle(numbers)  # Перемешиваем числа

        for number in numbers:
            if self.is_safe(row, col, number):
                self.grid[row][col] = number
                if self.fill_grid():
                    return True
                self.grid[row][col] = 0  # Если не удалось заполнить, сбрасываем

        return False  # Если ни одно число не подошло

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)  # Возвращаем первую пустую ячейку
        return None  # Если пустых ячеек нет

    def is_safe(self, row, col, num):
        for x in range(9):
            if self.grid[row][x] == num or self.grid[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False
        return True

    def remove_numbers(self):
        count = random.randint(20, 30) # Заполнение ячеек
        while count != 0:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.grid[i][j] != 0:
                self.entries[i][j].delete(0,tk.END)
                self.grid[i][j] = 0
                count -= 1

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.entries[i][j].insert(0, self.grid[i][j])
                    self.entries[i][j].config(state='readonly')  # ячейка только для чтения

    def check_win(self):
        for i in range(9):
            for j in range(9):
                if self.entries[i][j]['state'] != 'readonly':  # Проверка на только редактируемое
                    current_value = self.entries[i][j].get()
                    if current_value == "" or not current_value.isdigit() or not 1 <= int(
                            current_value) <= 9 or not self.is_safe(i, j, int(current_value)):
                        return  # Игра не закончена
        messagebox.showinfo("Победа!", "Вы выиграли! Все ячейки заполнены правильно.")
        self.root.quit()  # Закрываем окно игры

    def validate_input(self, event):
        widget = event.widget
        try:
            value = int(widget.get())
            row, col = widget.grid_info()['row'], widget.grid_info()['column']

            # сбрасываем цвета для всех ячеек
            for i in range(9):
                for j in range(9):
                    current_value = self.entries[i][j].get()
                    if current_value != "":
                        if self.is_safe(i, j, int(current_value)):
                            self.entries[i][j].config(bg='lightgreen')  # Зеленый для правильного
                        else:
                            self.entries[i][j].config(bg='lightcoral')  # Красный для неправильного

            # Проверяем на дубликаты в строках и столбцах
            for i in range(9):
                if i != row and self.entries[i][col].get() == str(value):
                    self.entries[i][col].config(bg='lightcoral')  # Красный цвет для дубликата в столбце
                if i != col and self.entries[row][i].get() == str(value):
                    self.entries[row][i].config(bg='lightcoral')  # Красный цвет для дубликата в строке

            # Проверяем на дубликаты в квадрате 3x3
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            square_has_duplicate = False

            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if (i != row or j != col) and self.entries[i][j].get() == str(value):
                        square_has_duplicate = True

            # Проверяем, является ли введенное значение безопасным
            if widget.get() not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                widget.delete(0, tk.END)
                messagebox.showerror("Ошибка", "Введите число от 1 до 9")
            elif self.is_safe(row, col, value):
                widget.config(bg='lightgreen')  # Зеленый цвет для правильного ответа
            else:
                widget.config(bg='lightcoral')  # Красный цвет для неправильного ответа

        except ValueError:
            widget.config(bg='white')  # Если не число, сбрасываем цвет

        # энд гейм ура ура
        self.check_win()
if __name__ == "__main__":
    root = tk.Tk()
    sudoku_game = Sudoku(root)
    root.mainloop()
