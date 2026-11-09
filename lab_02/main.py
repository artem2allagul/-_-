def analyze_reactor(temperatures, norm_temp=100, max_temp=180):
    total_temp = 0
    emergency_count = 0
    count = len(temperatures)

    if count == 0:
        return 0.0, 0

    print("Результаты анализа замеров")
    for t in temperatures:
        total_temp += t
        if t < norm_temp:
            print(f"Температура {t} С - Нагрев")
        elif norm_temp <= t <= max_temp:
            print(f"Температура {t} С - Норма")
        else:
            print(f"Температура {t} С - Авария")
            emergency_count += 1

    avg_temp = total_temp / count
    return avg_temp, emergency_count


measurements = [85.5, 100.0, 120.3, 185.0, 95.0, 200.5]
avg, emergencies = analyze_reactor(measurements)
print("-" * 34)
print(f"Средняя температура: {avg:.2f} С")
print(f"Количество аварийных замеров: {emergencies}")
