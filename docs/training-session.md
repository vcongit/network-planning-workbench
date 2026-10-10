# 15-minute training session: how to read a schedule and a route P&L

**Audience:** up to 10 people, mixed experience. **Materials:** the workbook on screen, the deck outline as backup, a one-page handout.

**Goals.** By the end, each person can (1) explain load factor versus breakeven load factor, (2) say why a full route does not always need another flight, (3) spot a connection that fails because of minimum connect time.

| Minutes | Segment | What to do |
|---|---|---|
| 0-2 | Why it matters | Hub-and-spoke in one sentence. Ask: "If a flight is 100% full, should we add one?" Take two guesses and park them. |
| 2-5 | Six terms | Capacity, demand, spill, load factor, breakeven load factor, block time. One sentence and one workbook cell each. |
| 5-10 | Live demo | On `Route_PnL`, walk Mumbai: 100% load factor, 80 spilled, yet a sixth A320 loses money (column X). Then switch Chennai to ATR72 with +3 rotations and watch profit flip. |
| 10-13 | Connections | On `Schedule`, show R19 landing at 10:21 and missing the 10:30 bank. Change departure to 05:30 and watch the flag clear. Explain the 45-minute MCT. |
| 13-15 | Check and close | Three questions, then one takeaway: judge a flight by what the next flight adds, not by how full the current ones are. |

## Check questions

1. A route is 89% full. Is it making money? *Only if 89% is above its breakeven load factor.*
2. Why can a smaller aircraft help on a short route? *Fixed cost per departure and ground time do not shrink with distance.*
3. A connection fails by nine minutes. What went wrong? *The arrival missed the minimum connect time to the next bank.*

## Presenter tips

- One sentence per term, then show the cell. People remember the demo.
- Say the limits out loud: synthetic data, no network revenue, no fare classes.
- If someone challenges a number, change the input live.
- For customers, swap the workbook for their product screens; keep the structure: term, cell, example.

## Handout

Load factor = passengers / seats. Breakeven load factor = cost / revenue at 100% full. Spill = demand turned away. Block time = pushback to gate. MCT = shortest workable transfer. Rule of thumb: add a flight only if it earns more than it costs.
