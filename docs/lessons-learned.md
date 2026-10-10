# Lessons learned

## 1. My first recommendation rule was wrong
**What I built:** flag a route "ADD capacity" when spill exceeds 5% of demand.
**What I found:** Mumbai spills 80 passengers per direction, so the rule said add. Testing a sixth A320 showed profit falls ₹8.0 lakh/day, because 80 passengers fill only 44% of 180 extra seats.
**Fix:** a new column (`Route_PnL`, column X) computes the profit change from adding one daily flight each way. ADD now needs spill above the threshold **and** a positive change. Otherwise the route shows "HOLD: spill too small to fill another flight - test pricing".
**Lesson:** judge a flight by the incremental economics, not by how full the existing ones are.

## 2. Check your own distances
I first quoted Trivandrum as about 700 km in an illustration. The great-circle distance is about 505 km. The workbook uses rounded great-circle values, labelled as assumptions. Sanity-check inputs against a reference before building on them.

## 3. Edge flags are noise
My first connection check flagged the first departures and last arrivals of the day, which naturally have no feeder or onward connection. I limited the flag to arrivals before the last departure, so what remains points at real timing problems.

## 4. Smaller can be better, but not free
Switching Chennai to the ATR72 turns a loss into a profit, but a turboprop has fewer seats and spills some demand. Fixing one cost problem can create a capacity one, so the trade-off has to be stated.
