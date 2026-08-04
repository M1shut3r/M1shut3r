import requests
import math

PROFILE = "Mishuter"
STATS_URL = f"https://coderun.yandex.ru/api/profile/statistics/{PROFILE}/problems/solved/dynamic"
COMP_URL = f"https://coderun.yandex.ru/api/profile/{PROFILE}/season-results/2026-summer"

COLORS = {"EASY": "#3fb950", "MEDIUM": "#d29922", "HARD": "#f85149"}

def fetch_data():
    stats = requests.get(STATS_URL).json()["result"]
    comp = requests.get(COMP_URL).json()["result"]
    return stats, comp

def build_svg(stats, comp):
    total_solved = stats["totalSolved"]
    diff = {s["literalDifficulty"]: s for s in stats["statistic"]}
    total_all = sum(s["total"] for s in stats["statistic"])

    track = comp["tracks"][0]
    comp_name = comp["name"]
    solved, total = track["problemSolved"], track["problemTotal"]
    score = track["score"]
    place = track["place"]
    participants = track["totalParticipants"]

    # Круговой индикатор
    r = 58
    C = 2 * math.pi * r
    frac = min(total_solved / total_all, 1) if total_all else 0
    dash = frac * C

    # Строки сложностей с прогресс-барами
    rows = ""
    y = 78
    for key, label in [("EASY", "Easy"), ("MEDIUM", "Medium"), ("HARD", "Hard")]:
        d = diff.get(key, {"solved": 0, "total": 0})
        s, t = d["solved"], d["total"]
        bar_w = 480
        fill_w = max(round(s / t * bar_w), 6) if t and s else 0
        rows += f'''
  <text x="210" y="{y}" fill="#e6edf3" font-size="19" font-weight="600">{label}</text>
  <text x="690" y="{y}" fill="#e6edf3" font-size="17" font-weight="600" text-anchor="end">{s} / {t}</text>
  <rect x="210" y="{y + 14}" width="{bar_w}" height="6" rx="3" fill="#2d333b"/>
  <rect x="210" y="{y + 14}" width="{fill_w}" height="6" rx="3" fill="{COLORS[key]}"/>'''
        y += 66

    svg = f'''<svg width="720" height="420" viewBox="0 0 720 420" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif">
  <rect width="720" height="420" rx="16" fill="#0d1117"/>
  <circle cx="110" cy="120" r="{r}" fill="none" stroke="#2d333b" stroke-width="10"/>
  <circle cx="110" cy="120" r="{r}" fill="none" stroke="#f0883e" stroke-width="10" stroke-linecap="round" stroke-dasharray="{dash:.1f} {C:.1f}" transform="rotate(-90 110 120)"/>
  <text x="110" y="120" fill="#ffffff" font-size="42" font-weight="700" text-anchor="middle" dominant-baseline="central">{total_solved}</text>
  {rows}
  <line x1="30" y1="268" x2="690" y2="268" stroke="#2d333b" stroke-width="1"/>
  <text x="30" y="305" fill="#8b949e" font-size="14" font-weight="700" letter-spacing="3">COMPETITIONS</text>
  <text x="30" y="338" fill="#e6edf3" font-size="20" font-weight="700">{comp_name}</text>
  <text x="30" y="380" fill="#ffffff" font-size="22" font-weight="700">{solved} / {total}</text>
  <text x="30" y="402" fill="#8b949e" font-size="14">Solved</text>
  <text x="280" y="380" fill="#ffffff" font-size="22" font-weight="700">{score}</text>
  <text x="280" y="402" fill="#8b949e" font-size="14">Points</text>
  <text x="480" y="380" fill="#ffffff" font-size="22" font-weight="700">#{place} / {participants:,}</text>
  <text x="480" y="402" fill="#8b949e" font-size="14">Place</text>
</svg>'''
    return svg

def update_readme():
    stats, comp = fetch_data()

    # Сохраняем SVG-карточку
    with open("stats.svg", "w", encoding="utf-8") as f:
        f.write(build_svg(stats, comp))

    # Вставляем картинку в README между маркерами
    readme_block = '<div align="center">\n  <img src="./stats.svg" alt="CodeRun statistics" width="720"/>\n</div>'

    with open('README.md', 'r', encoding='utf-8') as file:
        readme_content = file.read()

    start_marker = "<!-- CODE_RUN_STATS_START -->"
    end_marker = "<!-- CODE_RUN_STATS_END -->"

    if start_marker in readme_content and end_marker in readme_content:
        start_index = readme_content.find(start_marker) + len(start_marker)
        end_index = readme_content.find(end_marker)
        new_content = (readme_content[:start_index] + "\n" + readme_block + "\n" + readme_content[end_index:])
        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(new_content)
        print("README and stats.svg updated successfully!")
    else:
        print("Markers not found in README!")

if __name__ == "__main__":
    update_readme()