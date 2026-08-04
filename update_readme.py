import requests
import json
from datetime import datetime

def fetch_code_run_stats():
    # Получаем статистику решенных задач
    stats_url = "https://coderun.yandex.ru/api/profile/statistics/Mishuter/problems/solved/dynamic"
    
    # Получаем данные о соревновании
    competition_url = "https://coderun.yandex.ru/api/profile/Mishuter/season-results/2026-summer"
    
    try:
        stats_response = requests.get(stats_url)
        stats_data = stats_response.json()
        
        competition_response = requests.get(competition_url)
        competition_data = competition_response.json()
        
        # Извлекаем данные о задачах
        total_solved = stats_data['result']['totalSolved']
        easy_solved = 0
        medium_solved = 0
        hard_solved = 0
        
        for stat in stats_data['result']['statistic']:
            if stat['literalDifficulty'] == 'EASY':
                easy_solved = stat['solved']
            elif stat['literalDifficulty'] == 'MEDIUM':
                medium_solved = stat['solved']
            elif stat['literalDifficulty'] == 'HARD':
                hard_solved = stat['solved']
        
        # Извлекаем данные о соревновании
        competition_info = competition_data['result']['tracks'][0]
        comp_name = competition_data['result']['name']
        comp_solved = competition_info['problemSolved']
        comp_total = competition_info['problemTotal']
        comp_score = competition_info['score']
        comp_place = competition_info['place']
        comp_total_participants = competition_info['totalParticipants']
        
        # Форматируем ASCII блок
        stats_block = f"""╭────────────────────────────────────────────╮
│ CODE RUN                                   │
│                                            │
│  {total_solved:<16}{easy_solved:<10}{medium_solved:<10}{hard_solved}    │
│ Solved          Easy     Medium     Hard   │
│                                            │
├────────────────────────────────────────────┤
│ COMPETITIONS                               │
│                                            │
│ {comp_name:<42}  │
│                                            │
│  {comp_solved} / {comp_total:<12}{comp_score:<11}#{comp_place} / {comp_total_participants:,}   │
│  Solved        Points          Place       │
╰────────────────────────────────────────────╯
Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        return stats_block
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def update_readme():
    stats_block = fetch_code_run_stats()
    
    if stats_block:
        with open('README.md', 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Ищем маркеры для вставки
        start_marker = "<!-- CODE_RUN_STATS_START -->"
        end_marker = "<!-- CODE_RUN_STATS_END -->"
        
        if start_marker in readme_content and end_marker in readme_content:
            start_index = readme_content.find(start_marker) + len(start_marker)
            end_index = readme_content.find(end_marker)
            
            new_content = (
                readme_content[:start_index] + 
                "\n" + stats_block + "\n" + 
                readme_content[end_index:]
            )
            
            with open('README.md', 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print("README updated successfully!")
        else:
            print("Markers not found in README. Please add:")
            print(f"{start_marker}")
            print(f"{end_marker}")

if __name__ == "__main__":
    update_readme()