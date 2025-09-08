import subprocess
import time
import pyautogui
import uno
# from sympy.physics.units.definitions.dimension_definitions import information


# xhost +SI:localuser:$(whoami)

def connecting():
    try:
        localContext = uno.getComponentContext()
        print("ComponentContext erfolgreich erhalten")
    except Exception as e:
        print("Fehler beim Abrufen des ComponentContext:", e)
        exit(1)

    libreoffice_process = subprocess.Popen(["libreoffice", "--accept=socket,host=localhost,port=2002;urp;", "EXCEL.ods"])
    time.sleep(3)  # Wait until opened

    try:
        resolver = localContext.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", localContext)
        ctx = resolver.resolve(
                "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        smgr = ctx.ServiceManager
        print("Verbindung zum UNO-Server erfolgreich")
    except Exception as e:
        print(f"Fehler beim Verbinden mit dem UNO-Server: {e}")
        exit(1)

    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    model = desktop.getCurrentComponent()
    sheets = model.getSheets()
    # print(sheets)
    # print(type(sheets))
    return desktop, model, sheets

def get_sheet(sheet_name:str):
    sheets = model.getSheets()
    task_sheet = sheets.getByName(sheet_name)
    model.getCurrentController().setActiveSheet(task_sheet)
    return task_sheet

def screenshot(sheet:str):
    # Screenshot area (x, y, width, height)
    area = (00, 170+45, 1440, 460-45)# auf zirp
    screenshot = pyautogui.screenshot(region=area)
    if sheet == "startpage":
        screenshot.save("Spreadsheet.png")
    # elif sheet in [f"task_{c}" for c in "ABCDEF"]:
    #     letter_to_number = {
    #         "A": "21",
    #         "B": "22",
    #         "C": "23",
    #         "D": "24",
    #         "E": "25",
    #         "F": "26"
    #     }
    #     screenshot.save(f"task_{letter_to_number[sheet[-1]]}.png")
    else:
        screenshot.save(f"{sheet}.png")
    time.sleep(1)

def select_cell(task_name:str, task_sheet, controller):
    relevant_cell = {
        "task_1": (5, 8),   # F9
        "task_2": (4, 7),   # E8
        "task_3": (9, 9),   # J10
        "task_4": (10, 7),  # K8
        "task_5": (None,None),
        "task_6": (None,None),
        "task_7":  (None,None),#(9, 2),   # J3
        "task_8": (4, 12),  # E13
        "task_9": (2, 8),   # C9
        "task_10": (None,None),
        "task_11": (None,None),
        "task_12": (None,None),
        "task_13": (None,None),
        "task_14": (11, 5), # L6
        "task_15": (3, 16), # D17
        "task_16": (None,None),
        "task_17": (5, 12), # F13
        "task_18": (3, 8),  # D9
        "task_19": (None,None),
        "task_20": (11, 6), # L7
        "task_A": (None,None),
        "task_B": (None,None),
        "task_C": (None,None),
        "task_D": (None,None),
        "task_E": (None,None),
        "task_F": (None,None),
        "task_G": (10,7),#K8
        "startpage": (None,None),
    }
    # (Spalte F = Index 5, Zeile 8 = Index 7)
    position_x, position_y = (None,None) #relevant_cell[task_name]
    if position_x is None or position_y is None:
        position_x,position_y = (13,19) # N20
        cell = task_sheet.getCellByPosition(position_x, position_y)
        controller.select(cell)  # markiert
    else:
        # Zelle auswählen (muss in letztem Öffnen des Sheets angeklickt gewesen sein!)
        cell = task_sheet.getCellByPosition(position_x, position_y)  # (Spalte, Zeile)
        # controller.select(cell) #markiert
    time.sleep(0.1)


desktop, model, sheets = connecting()

sheet_names = ["startpage"]+[f"task_{sheet_no}" for sheet_no in range(1, 20+1)]+ [f"task_{a}" for a in ["C", "E", "G"]]
for sheet_name in sheet_names:
    try:
        task_sheet = get_sheet(sheet_name)
        time.sleep(1)
        select_cell(sheet_name, task_sheet=task_sheet, controller = model.getCurrentController())
        time.sleep(1)
        screenshot(sheet_name)
    except Exception as e:
        print(sheet_name, e)
