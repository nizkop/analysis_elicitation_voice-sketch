import matplotlib.pyplot as my_plt
import matplotlib.font_manager as fm


font_path = '/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf'  # Beispiel: '/usr/share/fonts/truetype/Symbola.ttf'
prop = fm.FontProperties(fname=font_path)
fm.fontManager.addfont(font_path)


size_1 = 16
size_2 = size_1-2
footnotesize = 11
my_plt.rcParams.update({
    'font.family': ['DejaVu Sans', 'Noto Sans Symbols'],
    'font.size': size_1,          # Grund-Schriftgröße (alle Texte)
    'font.weight': 'bold',    # Fettdruck für alle Texte
    'axes.labelweight': 'bold',  # Fettdruck für Achsenbeschriftungen
    'axes.titleweight': 'bold',  # Fettdruck für Titel
    'xtick.labelsize': size_2,       # Schriftgröße der x-Tick-Labels
    'ytick.labelsize': size_2,       # Schriftgröße der y-Tick-Labels
    'legend.fontsize': size_2,       # Schriftgröße der Legende
    'legend.title_fontsize': size_2, # Schriftgröße des Legendentitels
    'text.usetex': True,
    'text.latex.preamble' : r'''
        \usepackage{textcomp}
    ''',
})
my_plt.xticks(rotation=45)

figure_width = 10
default_height = 6




def save_my_figures(name:str, fig=None, bbox_extra_artists:list=[], height=4):
    if "pdf" in name:
        raise Exception("PDF not supposed to be in name, is added automatically")
    if fig is None:
        fig = my_plt.gcf()
    # fig.tight_layout()
    fig.savefig(f"{name}.pdf",
                bbox_inches='tight',#<- Plot will occupy maximum of available space
                transparent=True,
                dpi=300,
                bbox_extra_artists=bbox_extra_artists#Extra-Elemente berücksichten, wie z.B. Legende
                )



def blend_colors(c1, c2, alpha=0.5):
    if alpha > 0.5:
        raise Exception('alpha > 0.5')
    r = alpha * c1[0] + alpha * c2[0]
    g = alpha * c1[1] + alpha * c2[1]
    b = alpha * c1[2] + alpha * c2[2]
    return (r, g, b)
