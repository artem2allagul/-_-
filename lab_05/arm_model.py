"""Модель двухзвенного плоского манипулятора (без графического интерфейса)."""
import math


class Link:
    """Звено манипулятора: длина и угол поворота в суставе."""

    def __init__(self, length, angle=0.0):
        self._length = 1.0
        self.length = length          # проверка через свойство
        self.angle = float(angle)     # угол сустава, градусы

    @property
    def length(self):
        """Длина звена, м (только положительное значение)."""
        return self._length

    @length.setter
    def length(self, value):
        if value <= 0:
            raise ValueError("Длина звена должна быть положительной")
        self._length = float(value)

    def __str__(self):
        return f"звено(L={self._length:.2f} м, угол={self.angle:.1f}°)"


class Manipulator:
    """Двухзвенный манипулятор. Угол второго звена отсчитывается
    от направления первого. Допустимый диапазон углов — ±180°."""

    ANGLE_MIN = -180.0
    ANGLE_MAX = 180.0

    def __init__(self, length1=1.5, length2=1.0):
        self.links = [Link(length1), Link(length2)]

    def limits(self, index):
        """Допустимый диапазон угла сустава (переопределяется в потомках)."""
        return self.ANGLE_MIN, self.ANGLE_MAX

    def check_angle(self, index, value):
        """Проверка угла сустава; при выходе за предел — ValueError."""
        low, high = self.limits(index)
        if not low <= value <= high:
            raise ValueError(
                f"Сустав {index + 1}: угол {value:.1f}° вне диапазона "
                f"{low:.0f}...{high:.0f}°")

    def set_angle(self, index, value):
        """Задать угол сустава (после проверки)."""
        self.check_angle(index, value)
        self.links[index].angle = float(value)

    def get_angle(self, index):
        return self.links[index].angle

    def joints(self):
        """Прямая кинематика: координаты начала, сустава и схвата, м."""
        a1 = math.radians(self.links[0].angle)
        a2 = a1 + math.radians(self.links[1].angle)
        x1 = self.links[0].length * math.cos(a1)
        y1 = self.links[0].length * math.sin(a1)
        x2 = x1 + self.links[1].length * math.cos(a2)
        y2 = y1 + self.links[1].length * math.sin(a2)
        return [(0.0, 0.0), (x1, y1), (x2, y2)]

    def end_point(self):
        """Координаты схвата (x, y), м."""
        return self.joints()[-1]

    def __str__(self):
        x, y = self.end_point()
        return (f"{self.__class__.__name__}: θ1={self.links[0].angle:.1f}°, "
                f"θ2={self.links[1].angle:.1f}°, схват=({x:.3f}; {y:.3f}) м")


class PlanarArm(Manipulator):
    """Манипулятор с механическими ограничениями углов суставов."""

    def __init__(self, length1=1.5, length2=1.0,
                 limits=((-90.0, 90.0), (-135.0, 135.0))):
        super().__init__(length1, length2)
        self._limits = limits

    def limits(self, index):
        return self._limits[index]


if __name__ == "__main__":
    # Проверка модели без интерфейса
    arm = PlanarArm(1.5, 1.0)
    print(arm)
    arm.set_angle(0, 90)
    arm.set_angle(1, -90)
    print(arm)
    for idx, val in ((0, 120), (1, -150)):
        try:
            arm.set_angle(idx, val)
        except ValueError as err:
            print("Ошибка:", err)
    print(arm)
