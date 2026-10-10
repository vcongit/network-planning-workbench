from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.comments import Comment
import datetime as dt

F = "Arial"
base = Font(name=F, size=10)
bold = Font(name=F, size=10, bold=True)
blue = Font(name=F, size=10, color="0000FF")
green = Font(name=F, size=10, color="008000")
hdr_font = Font(name=F, size=10, bold=True, color="FFFFFF")
hdr_fill = PatternFill("solid", fgColor="1F3864")
title_font = Font(name=F, size=14, bold=True, color="1F3864")
inp_fill = PatternFill("solid", fgColor="FFF2CC")
tot_fill = PatternFill("solid", fgColor="D9E1F2")
thin = Side(style="thin", color="BFBFBF")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
center = Alignment(horizontal="center", vertical="center", wrap_text=True)

INR = '₹#,##0;(₹#,##0);-'
INR2 = '₹#,##0.00;(₹#,##0.00);-'
PCT = '0.0%;(0.0%);-'
NUM = '#,##0;(#,##0);-'
TIME = 'hh:mm'

wb = Workbook()

def style_range(ws, rng, font=None, fill=None, fmt=None, align=None, border=True):
    for row in ws[rng]:
        for c in row:
            if font: c.font = font
            if fill: c.fill = fill
            if fmt: c.number_format = fmt
            if align: c.alignment = align
            if border: c.border = box

def header(ws, row, labels, start_col=1):
    for i, l in enumerate(labels):
        c = ws.cell(row=row, column=start_col+i, value=l)
        c.font = hdr_font; c.fill = hdr_fill; c.alignment = center; c.border = box
    ws.row_dimensions[row].height = 42

# ---------------- README ----------------
rd = wb.active; rd.title = "README"
rd["A1"] = "Mini Network Planning Workbench - Bengaluru (BLR) hub"; rd["A1"].font = title_font
lines = [
 ("What this is", "A learning model of a fictional hub-and-spoke airline: 1 hub (BLR) + 6 spokes. It shows how a planner connects schedule, demand, fares and cost to decide: add, hold, watch or cut."),
 ("IMPORTANT", "All data is synthetic/illustrative. Distances are rounded approximate great-circle values; fares, demand, costs, speeds and turn times are my own assumptions, NOT Sabre or any airline's data. Verify before quoting any number externally."),
 ("Colour legend", "Blue text on yellow = input you can change. Black = formula. Green = link to another sheet. Do not overwrite black cells."),
 ("Tab: Inputs", "Scenario levers (demand, fare, cost change), connection rules (MCT, max connect) and the fleet table (seats, speed, cost per block hour, turnaround)."),
 ("Tab: Markets", "One row per spoke: distance, baseline daily demand per direction, average fare, aircraft type, and a frequency adjustment (+/-) for what-if."),
 ("Tab: Schedule", "One row per aircraft rotation (BLR -> spoke -> BLR). Edit the BLR departure time and spoke; arrival, turnaround and return times are computed. Connection counts show whether the hub banks work."),
 ("Tab: Route_PnL", "Per-route daily economics: capacity, passengers, spill, load factor, revenue, cost, profit, ASK/RPK, RASK, CASK, yield, breakeven load factor, a recommendation and the profit change from adding one more daily flight. Spill alone never triggers ADD: the extra flight must also be profitable."),
 ("How a number flows", "Schedule (rotations per spoke) -> frequency -> capacity (seats x flights) -> passengers = MIN(capacity, demand) -> revenue; block time (distance/speed + allowance) -> cost per flight -> profit."),
 ("Practice 1", "Set Markets!G for MAA to +3 and F to ATR72. What happens to profit and spill? Why does a smaller aircraft help on a short route?"),
 ("Practice 2", "Set Inputs!B6 (cost change) to +10%. Which routes flip from HOLD to WATCH or REVIEW? Explain breakeven load factor."),
 ("Practice 3", "In Schedule, R19 (BOM) arrives about 10:21, nine minutes after the 10:30 bank leaves. Change its BLR departure to 05:30 and watch the connection counts and flag. Explain MCT and why 'a few minutes late' kills a connection."),
 ("Practice 4", "Raise demand 15% in Inputs!B4. Which routes spill, and does adding a flight pay (column X)? What else could you do: bigger aircraft, higher fare?"),
 ("Limits (be honest in interviews)", "No recapture of spilled passengers, no network (O&D) revenue from connecting passengers, no fare classes, no slots, single-day view, two aircraft types only. Real planning tools model all of this."),
]
r = 3
for k, v in lines:
    rd.cell(row=r, column=1, value=k).font = bold
    c = rd.cell(row=r, column=2, value=v); c.font = base; c.alignment = wrap
    rd.cell(row=r, column=1).alignment = wrap
    r += 1
rd.column_dimensions["A"].width = 26; rd.column_dimensions["B"].width = 110
for i in range(3, r): rd.row_dimensions[i].height = 42

# ---------------- Inputs ----------------
ip = wb.create_sheet("Inputs")
ip["A1"] = "Inputs and scenario levers"; ip["A1"].font = title_font
ip["A3"] = "Scenario levers and rules"; ip["A3"].font = bold
levers = [
 ("Demand change vs base", 0, PCT, "Scenario lever. 0.1 = +10% demand on every route."),
 ("Fare change vs base", 0, PCT, "Scenario lever. Applies to all average fares."),
 ("Cost change (fuel, charges)", 0, PCT, "Scenario lever. Applies to all flight costs."),
 ("Minimum connect time, MCT (minutes)", 45, NUM, "Assumption: shortest legal/realistic transfer time at the hub. Real MCTs vary by airport, terminal and domestic/international."),
 ("Maximum useful connect time (minutes)", 180, NUM, "Assumption: connections longer than this are not treated as useful."),
 ("Spill threshold to recommend ADD (share of demand)", 0.05, PCT, "Assumption: if more than this share of demand is turned away, recommend adding capacity."),
 ("Thin-margin threshold (load factor points above breakeven)", 0.03, PCT, "Assumption: below this cushion the route is flagged WATCH."),
]
for i, (lab, val, fmt, note) in enumerate(levers):
    r = 4 + i
    ip.cell(row=r, column=1, value=lab).font = base
    c = ip.cell(row=r, column=2, value=val); c.font = blue; c.fill = inp_fill; c.number_format = fmt; c.border = box
    n = ip.cell(row=r, column=3, value=note); n.font = base
ip["A12"] = "Fleet table (illustrative assumptions - not real airline data)"; ip["A12"].font = bold
header(ip, 13, ["Aircraft", "Seats", "Cruise speed (km/h)", "Taxi/climb allowance (hrs)", "Cost per block hour (INR)", "Fixed cost per departure (INR)", "Turnaround (min)"])
fleet = [("A320", 180, 800, 0.5, 480000, 150000, 45), ("ATR72", 78, 500, 0.4, 150000, 50000, 35)]
for i, row in enumerate(fleet):
    r = 14 + i
    for j, v in enumerate(row):
        c = ip.cell(row=r, column=1+j, value=v)
        c.font = blue if j > 0 else bold; c.border = box
        if j > 0: c.fill = inp_fill
        if j in (4, 5): c.number_format = INR
        if j in (1, 2, 6): c.number_format = NUM
ip["A17"] = "Block time = distance / cruise speed + taxi/climb allowance. Cost per flight = block hours x cost per block hour + fixed cost per departure."
ip["A17"].font = base
ip.column_dimensions["A"].width = 52
for col in "BCDEFG": ip.column_dimensions[col].width = 18
ip.column_dimensions["C"].width = 22

# ---------------- Markets ----------------
mk = wb.create_sheet("Markets")
mk["A1"] = "Markets (spokes served from BLR)"; mk["A1"].font = title_font
mk["A2"] = "Blue/yellow cells are inputs. Demand and fare are per direction per day, synthetic. Distances: rounded approximate great-circle, assumption."; mk["A2"].font = base
header(mk, 4, ["Spoke", "City", "Distance (km)", "Base demand (pax/day/direction)", "Average fare (INR)", "Aircraft", "Frequency adjustment (+/- daily flights)", "Note"])
mkts = [
 ("TRV", "Thiruvananthapuram", 505, 640, 4500, "A320", 0, "Strong business and leisure market"),
 ("COK", "Kochi", 340, 300, 3200, "ATR72", 0, "Short sector, turboprop fits demand"),
 ("HYD", "Hyderabad", 500, 640, 4800, "A320", 0, "Corporate heavy"),
 ("MAA", "Chennai", 290, 480, 3200, "A320", 0, "Very short sector, jet may be too big/costly"),
 ("GOI", "Goa", 485, 440, 4500, "A320", 0, "Leisure, seasonal"),
 ("BOM", "Mumbai", 845, 980, 6200, "A320", 0, "Trunk route, high demand"),
]
for i, row in enumerate(mkts):
    r = 5 + i
    for j, v in enumerate(row):
        c = mk.cell(row=r, column=1+j, value=v); c.border = box
        c.font = bold if j == 0 else (blue if j in (2,3,4,5,6) else base)
        if j in (2,3,4,5,6): c.fill = inp_fill
        if j == 2 or j == 3: c.number_format = NUM
        if j == 4: c.number_format = INR
dv = DataValidation(type="list", formula1="=Inputs!$A$14:$A$15", allow_blank=False); mk.add_data_validation(dv); dv.add("F5:F10")
widths = [10, 22, 14, 20, 16, 12, 24, 44]
for i, w in enumerate(widths): mk.column_dimensions[chr(65+i)].width = w
mk.freeze_panes = "A5"

# ---------------- Schedule ----------------
sc = wb.create_sheet("Schedule")
sc["A1"] = "Daily rotation schedule (BLR hub)"; sc["A1"].font = title_font
sc["A2"] = "Share of arrivals (before the last departure) with at least one valid onward connection:"; sc["A2"].font = bold
sc["H2"] = '=IF(COUNTIF(H5:H27,"<"&MAX(D5:D27))=0,0,COUNTIFS(I5:I27,">0",H5:H27,"<"&MAX(D5:D27))/COUNTIF(H5:H27,"<"&MAX(D5:D27)))'; sc["H2"].number_format = PCT; sc["H2"].font = bold
header(sc, 4, ["Rotation", "Spoke", "Aircraft", "BLR departure", "Block time (hrs, each way)", "Arrive spoke", "Depart spoke", "Arrive BLR", "Valid onward connections from this arrival", "Valid feeder arrivals into this departure", "Check"])
rot = []
def add(spoke, times): 
    for t in times: rot.append((spoke, t))
add("TRV", ["06:30","10:30","14:30","18:30"])
add("COK", ["06:30","10:30","14:30","18:30"])
add("HYD", ["06:30","10:30","14:30","18:30"])
add("MAA", ["06:30","14:30","18:30"])
add("GOI", ["06:30","10:30","14:30"])
add("BOM", ["06:30","10:30","12:30","14:30","18:30"])
for i, (spoke, t) in enumerate(rot):
    r = 5 + i
    h, m = map(int, t.split(":"))
    sc.cell(row=r, column=1, value=f"R{i+1:02d}").font = bold
    c = sc.cell(row=r, column=2, value=spoke); c.font = blue; c.fill = inp_fill
    sc.cell(row=r, column=3, value=f"=INDEX(Markets!$F$5:$F$10,MATCH(B{r},Markets!$A$5:$A$10,0))").font = green
    c = sc.cell(row=r, column=4, value=dt.time(h, m)); c.font = blue; c.fill = inp_fill; c.number_format = TIME
    sc.cell(row=r, column=5, value=f"=INDEX(Route_PnL!$D$5:$D$10,MATCH(B{r},Route_PnL!$A$5:$A$10,0))").font = green
    sc.cell(row=r, column=5).number_format = '0.00'
    sc.cell(row=r, column=6, value=f"=D{r}+E{r}/24").number_format = TIME
    sc.cell(row=r, column=7, value=f"=F{r}+INDEX(Inputs!$G$14:$G$15,MATCH(C{r},Inputs!$A$14:$A$15,0))/1440").number_format = TIME
    sc.cell(row=r, column=8, value=f"=G{r}+E{r}/24").number_format = TIME
    sc.cell(row=r, column=9, value=f"=SUMPRODUCT(($D$5:$D$27-H{r}>=Inputs!$B$7/1440)*($D$5:$D$27-H{r}<=Inputs!$B$8/1440)*($B$5:$B$27<>B{r}))").number_format = NUM
    sc.cell(row=r, column=10, value=f"=SUMPRODUCT((D{r}-$H$5:$H$27>=Inputs!$B$7/1440)*(D{r}-$H$5:$H$27<=Inputs!$B$8/1440)*($B$5:$B$27<>B{r}))").number_format = NUM
    sc.cell(row=r, column=11, value=f'=IF(AND(I{r}=0,H{r}<MAX($D$5:$D$27)),"! arrival misses every onward bank",IF(AND(J{r}=0,D{r}>MIN($H$5:$H$27)),"! departure has no feeder","OK"))')
    for col in range(1, 12):
        c = sc.cell(row=r, column=col); c.border = box
        if col not in (2, 4, 3, 5): c.font = bold if col == 1 else base
        if col in (6,7,8,9,10,11): c.font = base
sc.conditional_formatting.add("K5:K27", FormulaRule(formula=['LEFT(K5,1)="!"'], fill=PatternFill("solid", bgColor="F8CBAD")))
for i, w in enumerate([10, 9, 10, 14, 16, 13, 13, 13, 22, 22, 36]): sc.column_dimensions[chr(65+i)].width = w
sc.freeze_panes = "A5"
sc["A29"] = "Note: block time depends on aircraft and distance (Route_PnL). The number of rotations per spoke here drives scheduled frequency in Route_PnL. Times are one synthetic day."
sc["A29"].font = base

# ---------------- Route_PnL ----------------
pl = wb.create_sheet("Route_PnL")
pl["A1"] = "Route economics (daily, both directions unless stated)"; pl["A1"].font = title_font
pl["A2"] = "Formulas only - change Inputs, Markets or Schedule. Capacity/demand/passengers are per direction; revenue, cost, profit, ASK, RPK are both directions."; pl["A2"].font = base
cols = ["Spoke", "Aircraft", "Seats", "Block time (hrs)", "Scheduled rotations", "Daily flights per direction", "Capacity (pax/dir/day)", "Demand (pax/dir/day)", "Passengers carried (per dir)", "Spill (pax/dir)", "Load factor", "Fare (INR)", "Revenue (INR/day)", "Cost (INR/day)", "Profit (INR/day)", "ASK/day", "RPK/day", "RASK (INR)", "CASK (INR)", "Yield (INR/RPK)", "Breakeven load factor", "Cushion (LF pts)", "Recommendation", "Profit change from adding 1 daily flight each way (INR/day)"]
header(pl, 4, cols)
IDX = lambda col, key: f"INDEX(Inputs!${col}$14:${col}$15,MATCH({key},Inputs!$A$14:$A$15,0))"
for i in range(6):
    r = 5 + i
    f = {
     1: f"=Markets!A{r}",
     2: f"=Markets!F{r}",
     3: "=" + IDX("B", f"B{r}"),
     4: f"=Markets!C{r}/" + IDX("C", f"B{r}") + "+" + IDX("D", f"B{r}"),
     5: f"=COUNTIF(Schedule!$B$5:$B$27,A{r})",
     6: f"=MAX(0,E{r}+Markets!G{r})",
     7: f"=F{r}*C{r}",
     8: f"=Markets!D{r}*(1+Inputs!$B$4)",
     9: f"=MIN(G{r},H{r})",
     10: f"=MAX(0,H{r}-G{r})",
     11: f"=IF(G{r}=0,0,I{r}/G{r})",
     12: f"=Markets!E{r}*(1+Inputs!$B$5)",
     13: f"=I{r}*L{r}*2",
     14: f"=F{r}*2*(D{r}*" + IDX("E", f"B{r}") + "+" + IDX("F", f"B{r}") + ")*(1+Inputs!$B$6)",
     15: f"=M{r}-N{r}",
     16: f"=G{r}*Markets!C{r}*2",
     17: f"=I{r}*Markets!C{r}*2",
     18: f"=IF(P{r}=0,0,M{r}/P{r})",
     19: f"=IF(P{r}=0,0,N{r}/P{r})",
     20: f"=IF(Q{r}=0,0,M{r}/Q{r})",
     21: f"=IF(G{r}*L{r}=0,0,N{r}/(L{r}*G{r}*2))",
     22: f"=K{r}-U{r}",
     23: f'=IF(AND(J{r}>Inputs!$B$9*H{r},X{r}>0),"ADD capacity / upgauge",IF(J{r}>Inputs!$B$9*H{r},"HOLD: spill too small to fill another flight - test pricing",IF(O{r}<0,"REVIEW: losing money - downgauge or cut",IF(V{r}<Inputs!$B$10,"WATCH: thin margin","HOLD"))))',
     24: f"=(MIN((F{r}+1)*C{r},H{r})*L{r}*2-(F{r}+1)*2*(D{r}*" + IDX("E", f"B{r}") + "+" + IDX("F", f"B{r}") + ")*(1+Inputs!$B$6))-O" + f"{r}",
    }
    for col, formula in f.items():
        c = pl.cell(row=r, column=col, value=formula); c.border = box
        c.font = green if col in (1, 2, 3) else (bold if col == 23 else base)
        if col == 24: c.number_format = INR
    fm = {3: NUM, 4: '0.00', 5: NUM, 6: NUM, 7: NUM, 8: NUM, 9: NUM, 10: NUM, 11: PCT, 12: INR, 13: INR, 14: INR, 15: INR, 16: NUM, 17: NUM, 18: INR2, 19: INR2, 20: INR2, 21: PCT, 22: PCT}
    for col, fmt in fm.items(): pl.cell(row=r, column=col).number_format = fmt
t = 11
pl.cell(row=t, column=1, value="NETWORK")
sums = {5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 13: "M", 14: "N", 15: "O", 16: "P", 17: "Q"}
for col, L in sums.items(): pl.cell(row=t, column=col, value=f"=SUM({L}5:{L}10)")
pl.cell(row=t, column=11, value="=IF(P11=0,0,Q11/P11)")
pl.cell(row=t, column=18, value="=IF(P11=0,0,M11/P11)")
pl.cell(row=t, column=19, value="=IF(P11=0,0,N11/P11)")
pl.cell(row=t, column=20, value="=IF(Q11=0,0,M11/Q11)")
pl.cell(row=t, column=21, value="=IF(M11=0,0,N11*K11/M11)")
pl.cell(row=t, column=22, value="=K11-U11")
for col in range(1, 25):
    c = pl.cell(row=t, column=col); c.font = bold; c.fill = tot_fill; c.border = box
fm.update({5: NUM})
for col, fmt in fm.items(): pl.cell(row=t, column=col).number_format = fmt
pl.cell(row=t, column=11).number_format = PCT
pl["A12"] = "Network load factor = total RPK / total ASK (distance-weighted). Network breakeven LF = cost / revenue at 100% load factor."; pl["A12"].font = base
pl.conditional_formatting.add("W5:W10", FormulaRule(formula=['LEFT(W5,3)="ADD"'], fill=PatternFill("solid", bgColor="C6E0B4")))
pl.conditional_formatting.add("W5:W10", FormulaRule(formula=['LEFT(W5,7)="HOLD: s"'], fill=PatternFill("solid", bgColor="DDEBF7")))
pl.conditional_formatting.add("W5:W10", FormulaRule(formula=['LEFT(W5,6)="REVIEW"'], fill=PatternFill("solid", bgColor="F8CBAD")))
pl.conditional_formatting.add("W5:W10", FormulaRule(formula=['LEFT(W5,5)="WATCH"'], fill=PatternFill("solid", bgColor="FFE699")))
for i in range(1, 25): pl.column_dimensions[chr(64+i) if i <= 26 else "A"].width = 15
pl.column_dimensions["W"].width = 44; pl.column_dimensions["X"].width = 24
pl.freeze_panes = "B5"

ch = BarChart(); ch.type = "col"; ch.title = "Load factor vs breakeven load factor by route"
ch.y_axis.title = "Load factor"; ch.y_axis.number_format = "0%"
cats = Reference(pl, min_col=1, min_row=5, max_row=10)
ch.add_data(Reference(pl, min_col=11, min_row=4, max_row=10), titles_from_data=True)
ch.add_data(Reference(pl, min_col=21, min_row=4, max_row=10), titles_from_data=True)
ch.set_categories(cats); ch.height = 8.5; ch.width = 18
pl.add_chart(ch, "A14")

wb.move_sheet("README", offset=-4) if False else None
wb.save("../workbook/Mini_Network_Planning_Workbench.xlsx")
print("saved")
