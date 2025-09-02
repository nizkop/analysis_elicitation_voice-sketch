import pandas as pd

from src.color_codes import global_colors
from src.plt_settings import my_plt, save_my_figures, default_height, figure_width, size_2

# CSV-Datei laden
df = pd.read_csv('src/GES/Gesture Elicitation Studies.csv')


# Überprüfen, ob die Spaltennamen korrekt sind
#print(df.columns)

# Entfernen von Leerzeichen aus der 'Publication Year'-Spalte (und nur die gültigen Jahre bearbeiten)
df['Publication Year'] = pd.to_numeric(df['Publication Year'], errors='coerce')

# Entfernen von NaN-Werten (ungültige Jahre)
df = df.dropna(subset=['Publication Year'])

# Umwandeln von "Publication Year" zu Ganzzahlen (entfernen der ".0")
df['Publication Year'] = df['Publication Year'].astype(int)

# Zählen der Paper pro Jahr
paper_counts_per_year = df['Publication Year'].value_counts().sort_index()

print(paper_counts_per_year)
# Balkendiagramm erstellen
my_plt.figure(figsize=(figure_width, default_height-2))#7,3
paper_counts_per_year.plot(kind='bar', color=global_colors[None], width=0.8)

# Achsentitel in fett und größer
my_plt.xlabel('Year of Publication', fontweight='bold')
my_plt.ylabel('Number of\nPapers/Articles', fontweight='bold')

# x-Achsenbeschriftungen schräg anzeigen (45 Grad)
my_plt.xticks(rotation=45)

# Diagramm anzeigen
save_my_figures("gesture-elicitation-studies-bar")
my_plt.show()