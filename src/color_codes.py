

global_colors = {#TODO zu Verzeichnis in Ausarbeitung = ?
    # Grafen im Theorieteil:
    # darkblue //  Mittelgrau neutral
    None: '#00008B',

    # Nationalfarben:
    "is": '#003897',  # Island Blau
    "de": '#FFCC00', # Deutschland Gold

    # QUALITATIVE Palette, 3-4 Farben:
    # zurzeit ausgewählt: Egypt
    "GUI": '#DD5129FF', #43B284FF',
    "sketch": '#0F7BA2FF',
    "voice": '#FAB255FF',


    # CODING-Bereiche:
    # Address blue warm, #4A66ACFF, #629DD1FF, #297FD5FF, #7F8FA9FF, #5AA2AEFF, #9D90A0FF
    "FULLMODLESS": "#4A66ACFF",
    "OPERATIONMODLESS": "#ADD8E6",
    "LOCATIONMODLESS": "#297FD5FF",
    "FULLMOD": "#4A66ACFF",# "#51929D",
    "LOCATIONMOD": "#297FD5FF",
    "OPERATIONMOD": "#ADD8E6",
    "EMPTYMOD": "#004080",


    # BLAUE, SEQUENTIELLE Palette mit 4 Farben:
    # zur Zeit ausgewählt: Aluterus Scriptus
    # #0F1926FF, #025940FF, #02734AFF, #038C33FF, #03A62CFF
    "groupP": '#',
    "groupA": '#66CC44',
    "groupB": '#038C33FF',
    "groupC": '#025F47',

    # DEMOGRAPHICS, Grüne Palette, Sequentiell, 3 Farben:
    "none": '#247C77',
    "a little": '#3BB973',
    "a lot": '#88D796',
    #  #B0F2BCFF, #89E8ACFF, #67DBA5FF, #4CC8A3FF, #38B2A3FF, #2C98A0FF, #257D98FF
    # #88D796, #5FCC86, #3BB973, 	#299E87, #247C77, 	#205F6D, 	#1A4D60

    # 5 Farben + ROT, Diverging Palette:
    # zur Zeit ausgewählt: M C Coolidge
    "very easy": '#204035FF',
    "easy": '#4A7169FF',
    "neutral": '#BEB59CFF',
    "difficult": '#735231FF',
    "very difficult": '#49271BFF',
    "skipped/missunderstood": "#8B0000",#= darkred

    # Agreement rates:
    # "agreement": "#800080",#=purple
    #agreement: (Pal grau, #E1E2E5FF, #B8BCC1FF, #9AA0A7FF, #73787EFF, #4D5054FF)
    "low": "#E7E3D7",
    "medium": "#C1BAA0",
    "high": "#A39572",
    "veryhigh": "#968469",#"#7C7251", 93885A, 8F7F63


    # Category sizes:
    # Purp #F3E0F7FF, #E4C7F1FF, #D1AFE8FF, #B998DDFF, #9F82CEFF, #826DBAFF, #63589FFF
    "category_size_2": "#E4C7F1FF",
    "category_size_3": "#D1AFE8FF",
    "category_size_4": "#9F82CEFF",
    "category_size_5": "#63589FFF",

    # Categories:
    "location:entry": "#43B284FF",
    "location:address": "#572F30FF",
    "location:pointing": "#FBA72AFF",
    "location:address - location:entry": "#4D705A",
    "location:entry - location:pointing": "#9FAC57",
    "location:address - location:pointing": "#A96B2C",
    "location:address - location:entry - location:pointing": "#7B6D43",
    "operation:words": "#3FB8AF",
    "operation:symbol": "#FF9E9D",
    "operation:symbol - operation:words": "#DAD8A7",#nicht mischfarbe
}

# https://r-graph-gallery.com/color-palette-finder



from src.plt_settings import blend_colors
import matplotlib.colors as mcolors

def get_mischfarbe():
    color_sketch_rgb = mcolors.to_rgb(global_colors['sketch'])
    color_voice_rgb = mcolors.to_rgb(global_colors['voice'])
    return blend_colors(color_voice_rgb, color_sketch_rgb, alpha=0.5)
def rgb_to_hex(r, g, b):
    return '#{:02X}{:02X}{:02X}'.format(int(r*255), int(g*255), int(b*255))
global_colors["voice+sketch"] = rgb_to_hex(*get_mischfarbe())



if __name__ == '__main__':
    color_sketch_rgb = mcolors.to_rgb(global_colors['operation:symbol'])
    color_voice_rgb = mcolors.to_rgb(global_colors['operation:words'])
    mischfarbe = blend_colors(color_voice_rgb, color_sketch_rgb, alpha=0.5)
    print( rgb_to_hex(*mischfarbe))