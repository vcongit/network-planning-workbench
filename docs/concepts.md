# Concepts primer

**Network planning** decides where an airline flies, with what aircraft and how often. **Scheduling** decides exactly when. The timetable is then loaded into distribution systems and sold.

## Building blocks

- **Leg vs O&D.** A leg is one flight (BLR-TRV). An origin-destination (O&D) is the passenger's whole trip. Mangaluru to Trivandrum via Bengaluru is one O&D on two legs. Planners judge a route by the network revenue it feeds, not only by its own seats. *This model does not include that feed revenue.*
- **Hub-and-spoke vs point-to-point.** A hub funnels many small markets through one airport so they can connect to each other. Point-to-point flies direct.
- **Banks and minimum connect time (MCT).** A hub clusters arrivals, then departures, so passengers can transfer. MCT is the shortest workable transfer. If an arrival lands 30 minutes before a departure and MCT is 45, that connection does not exist.
- **Block time, turnaround, rotation, utilization.** Block time runs pushback to gate. Turnaround is ground time between flights. A rotation is one aircraft's chain of flights. Utilization is how many hours a day it flies.
- **Demand, seasonality, spill.** Demand is forecast per market and season. If a flight is full and more people wanted it, the excess is spill.
- **Fleet assignment.** Putting the right aircraft on each flight. A big jet on a thin route loses money; a small aircraft on a hot route spills passengers.
- **Slots and seasons.** Airlines schedule by IATA season (summer starts late March, winter late October). Congested airports allocate slots.
- **Schedule files.** Airlines and vendors exchange schedules in standard formats (IATA's SSIM is the common one). Many support issues are files that fail validation.

## Unit measures

| Measure | Formula |
|---|---|
| ASK (available seat-km) | seats x distance |
| RPK (revenue passenger-km) | passengers x distance |
| Load factor | RPK / ASK |
| Yield | revenue / RPK |
| RASK / CASK | revenue / ASK, cost / ASK |
| Breakeven load factor | cost / revenue at 100% full |

Useful identity: **RASK = yield x load factor**. A route can fail because planes are too empty or because fares are too low for the cost.

## Worked example from the workbook: Trivandrum (TRV)

A320, 180 seats, 505 km, 4 daily flights each way, average fare ₹4,500, 160 passengers per flight (640 demand / 4).

- Block time: 505 / 800 + 0.5 = **1.13 hours**
- Cost per flight: 1.131 x ₹4,80,000 + ₹1,50,000 = **₹6.93 lakh**
- Revenue per flight: 160 x ₹4,500 = **₹7.20 lakh**; profit ₹27,000 per flight, ₹2.16 lakh/day over 8 flights
- ASK per flight: 180 x 505 = 90,900. CASK = 693,000 / 90,900 = **₹7.62**. RASK = 720,000 / 90,900 = **₹7.92**
- Breakeven load factor: 693,000 / (4,500 x 180) = **85.6%**. Actual: 88.9%. Cushion: **3.3 points**

A small fare cut or cost rise erases that cushion, which is why TRV is "hold, but watch".

## Why short routes struggle

Fixed cost per departure and the taxi/climb allowance are paid on every flight, whatever the distance. On a 290 km hop (Chennai) an A320 spends a large share of its cost on overhead, which is why a turboprop (ATR72) can win there.

## Why full does not mean add

Mumbai spills 80 passengers per direction (8% of demand). A sixth A320 offers 180 more seats but only 80 passengers would fill them, about 44%. The extra flight costs more than the extra revenue, so profit falls ₹8.0 lakh/day. Better first levers: price, aircraft size, or timing.
