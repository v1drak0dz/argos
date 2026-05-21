import re

import pandas as pd

# Caminho do arquivo de entrada
input_file = "frontend-user-stories.md"
# Caminho do Excel de saída
output_file = "frontend-user-stories.xlsx"

# Lê o conteúdo do arquivo
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Regex para capturar cada bloco de tarefa
pattern = re.compile(
    r"##\s+(?P<id>[A-Za-z0-9-]+)\s*"
    r"User Story:\s*(?P<user_story>.*?)\s*"
    r"Acceptance Criteria:\s*(?P<criteria>(?:-.*?\n)+)"
    r"Priority:\s*(?P<priority>\w+)\s*"
    r"Category:\s*(?P<category>\w+)",
    re.DOTALL,
)

rows = []
for match in pattern.finditer(content):
    user_story = match.group("user_story").strip()
    criteria = "\n".join(
        [
            line.strip("- ").strip()
            for line in match.group("criteria").strip().splitlines()
        ]
    )
    priority = match.group("priority").strip()
    category = match.group("category").strip()
    origin = "Frontend" if "Frontend" in match.group("id") else "Backend"

    rows.append(
        {
            "UserStory": user_story,
            "AcceptanceCriteria": criteria,
            "Priority": priority,
            "Category": category,
            "Origin": origin,
        }
    )

# Cria DataFrame e exporta para Excel
df = pd.DataFrame(
    rows, columns=["UserStory", "AcceptanceCriteria", "Priority", "Category", "Origin"]
)
df.to_excel(output_file, index=False)

print(f"Excel gerado em: {output_file}")
