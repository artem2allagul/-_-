def filter_outliers(vibe_list, min_val=0.0, max_val=50.0):
    return [v for v in vibe_list if min_val <= v <= max_val]
 
 
def get_stat_dict(vibe_list):
    if not vibe_list:
        return {'count': 0, 'mean': 0.0, 'min': 0.0, 'max': 0.0}
    mean_val = sum(vibe_list) / len(vibe_list)
    return {
        'count': len(vibe_list),
        'mean': round(mean_val, 2),
        'min': min(vibe_list),
        'max': max(vibe_list)
    }
 
 
def extract_top_vibes(vibe_list, k=3):
    sorted_list = sorted(vibe_list, reverse=True)
    return sorted_list[:k]
 
 
if __name__ == '__main__':
    test_raw = [10.0, -5.0, 30.0, 70.0, 20.0]
    test_clean = filter_outliers(test_raw)
    print(f"[Автотест модуля] Фильтрованный сигнал: {test_clean}")
    print(f"[Автотест модуля] Статистика: {get_stat_dict(test_clean)}")
    print(f"[Автотест модуля] ТОП-2 пика: {extract_top_vibes(test_clean, 2)}")

