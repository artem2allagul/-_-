"""Приложение «Двухзвенный манипулятор» (Tkinter)."""
import tkinter as tk
from tkinter import ttk, messagebox

from arm_model import PlanarArm


class ArmApp(tk.Tk):
    """Главное окно: ползунки/поля ввода углов, холст, вывод координат."""

    SIZE = 480      # размер холста, пикс.
    SCALE = 80      # пикселей на метр

    def __init__(self, arm):
        super().__init__()
        self.title("Двухзвенный манипулятор")
        self.resizable(False, False)
        self.arm = arm
        self._busy = False                      # защита от рекурсии
        self._warned = [False, False]           # предупреждение уже показано
        self.angle_vars = [tk.DoubleVar(value=0.0) for _ in range(2)]
        self.entry_vars = [tk.StringVar(value="0.0") for _ in range(2)]
        self.info = tk.StringVar()
        self.status = tk.StringVar(value="Углы в допустимых пределах")
        self._build_widgets()
        self._redraw()

    # ----- создание виджетов -----
    def _build_widgets(self):
        self.canvas = tk.Canvas(self, width=self.SIZE, height=self.SIZE,
                                bg="white")
        self.canvas.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

        panel = ttk.LabelFrame(self, text="Углы суставов")
        panel.grid(row=0, column=1, sticky="n", padx=5, pady=5)
        for i in range(2):
            low, high = self.arm.limits(i)
            ttk.Label(panel, text=f"Сустав {i + 1}, ° "
                      f"(допустимо {low:.0f}...{high:.0f}):").pack(anchor="w")
            ttk.Scale(panel, from_=-180, to=180, length=220,
                      variable=self.angle_vars[i],
                      command=lambda _v, k=i: self._on_slider(k)
                      ).pack(fill="x", pady=2)
            ttk.Entry(panel, textvariable=self.entry_vars[i],
                      width=10).pack(anchor="w", pady=(0, 8))
        ttk.Button(panel, text="Применить значения из полей",
                   command=self._apply_entries).pack(fill="x", pady=2)
        ttk.Button(panel, text="Сброс (0°, 0°)",
                   command=self._reset).pack(fill="x", pady=2)

        out = ttk.LabelFrame(self, text="Положение схвата")
        out.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(out, textvariable=self.info, justify="left").pack(anchor="w")
        self.status_label = ttk.Label(out, textvariable=self.status,
                                      wraplength=240, foreground="green")
        self.status_label.pack(anchor="w", pady=(8, 0))

    # ----- обработчики событий -----
    def _ok(self, text="Углы в допустимых пределах"):
        self.status.set(text)
        self.status_label.config(foreground="green")

    def _fail(self, text):
        self.status.set(text)
        self.status_label.config(foreground="red")

    def _on_slider(self, index):
        """Перемещение ползунка: при выходе за предел значение блокируется."""
        if self._busy:
            return
        value = round(self.angle_vars[index].get(), 1)
        try:
            self.arm.set_angle(index, value)
        except ValueError as err:
            self._busy = True
            self.angle_vars[index].set(self.arm.get_angle(index))
            self._busy = False
            self._fail(str(err) + ". Значение заблокировано.")
            if not self._warned[index]:
                self._warned[index] = True
                messagebox.showwarning("Предел сустава", str(err))
        else:
            self._warned[index] = False
            self.entry_vars[index].set(f"{value:.1f}")
            self._ok()
        self._redraw()

    def _apply_entries(self):
        """Ввод углов с клавиатуры (с обработкой ошибок)."""
        try:
            values = [float(v.get().replace(",", ".")) for v in self.entry_vars]
            for i, val in enumerate(values):
                self.arm.check_angle(i, val)
        except ValueError as err:
            text = str(err)
            if text.startswith("could not convert"):
                text = "Введите числовые значения углов"
            self._fail(text)
            messagebox.showerror("Ошибка ввода", text)
            return
        for i, val in enumerate(values):
            self.arm.set_angle(i, val)
            self.angle_vars[i].set(val)
        self._ok()
        self._redraw()

    def _reset(self):
        for i in range(2):
            self.arm.set_angle(i, 0.0)
            self.angle_vars[i].set(0.0)
            self.entry_vars[i].set("0.0")
            self._warned[i] = False
        self._ok()
        self._redraw()

    # ----- отрисовка -----
    def _to_px(self, x, y):
        c = self.SIZE / 2
        return c + x * self.SCALE, c - y * self.SCALE

    def _redraw(self):
        cv = self.canvas
        cv.delete("all")
        c = self.SIZE / 2
        cv.create_line(0, c, self.SIZE, c, fill="#ccc")
        cv.create_line(c, 0, c, self.SIZE, fill="#ccc")
        reach = sum(link.length for link in self.arm.links) * self.SCALE
        cv.create_oval(c - reach, c - reach, c + reach, c + reach,
                       outline="#bbb", dash=(4, 4))
        pts = [self._to_px(*p) for p in self.arm.joints()]
        cv.create_line(*pts[0], *pts[1], width=8, fill="steelblue",
                       capstyle="round")
        cv.create_line(*pts[1], *pts[2], width=6, fill="darkorange",
                       capstyle="round")
        for px, py in pts[:2]:
            cv.create_oval(px - 7, py - 7, px + 7, py + 7,
                           fill="white", outline="black", width=2)
        gx, gy = pts[2]
        cv.create_rectangle(gx - 6, gy - 6, gx + 6, gy + 6,
                            fill="red", outline="black")
        x, y = self.arm.end_point()
        cv.create_text(gx + 10, gy - 14, anchor="w",
                       text=f"({x:.2f}; {y:.2f})")
        self.info.set(f"x = {x:.3f} м\ny = {y:.3f} м\n"
                      f"θ1 = {self.arm.get_angle(0):.1f}°\n"
                      f"θ2 = {self.arm.get_angle(1):.1f}°")


def main():
    arm = PlanarArm(1.5, 1.0)
    app = ArmApp(arm)
    app.mainloop()


if __name__ == "__main__":
    main()
