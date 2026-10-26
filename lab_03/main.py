import sys
from variant1_mod import filter_outliers, get_stat_dict, extract_top_vibes
 
 
def main():
    max_limit = float(sys.argv[1]) if len(sys.argv) > 1 else 45.0
 
    vibe_raw = [12.4, 15.1, -99.0, 18.2, 520.0, 22.0, 41.5, 14.8, 48.0, 19.3]
 
    clean_vibe = filter_outliers(vibe_raw, min_val=0.0, max_val=max_limit)
    stats = get_stat_dict(clean_vibe)
    top_vibes = extract_top_vibes(clean_vibe, k=3)
 
    print("=== ВИБРОДИАГНОСТИКА ПОДШИПНИКОВ ===")
    print(f"Предел фильтрации (sys.argv): {max_limit} мм/с")
    print(f"Исходный объем замеров: {len(vibe_raw)}")
    print(f"Очищенная выборка: {clean_vibe}")
    print(f"Статистика: {stats}")
    print(f"ТОП-3 критических пика (срез [:3]): {top_vibes}")
 
 
if __name__ == '__main__':
    main()
