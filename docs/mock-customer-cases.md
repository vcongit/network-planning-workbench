# Mock customer cases

Practice scenarios showing how I would handle post-sale support: gather facts, reproduce, explain, document. Built on the synthetic workbook, not real customer data.

## Case 1: Schedule file rejected on load
**Channel / priority:** email, High.
**Customer:** "Our summer schedule file was rejected and nothing loaded. We need it live this week."

1. Acknowledge and set expectations. Ask for the file, the exact error text, and the last successful load.
2. Reproduce with a copy. Check in order: record format and field lengths; date ranges and operating-day patterns; aircraft type codes missing from the fleet table; an aircraft scheduled in two places or with too little turnaround.
3. Find the first failing record; later errors are often knock-on effects.
4. Reply briefly: what failed, which line, how to fix it, a corrected sample.
5. Confirm the reload, then log the resolution.

**Wording:** "The load stopped at record 214 because the aircraft type is not in your fleet table. I have attached a corrected line."
**KB article:** "Why a schedule load fails: five checks, in order."

## Case 2: "The route is full, so we want more flights"
**Channel / priority:** chat, Medium.
**Customer:** "Mumbai shows 100% load factor. Why won't your tool recommend adding flights?"

1. Ask what they want: more revenue, fewer spilled passengers, or better connections.
2. Show the numbers: 80 passengers per direction spilled (8%), but a sixth 180-seat flight would run about 44% full on those extra seats.
3. Show the economics: profit falls about ₹8.0 lakh/day with the extra flight.
4. Offer alternatives: a modest fare increase, a different aircraft, retiming for connections.
5. State the limits: no price elasticity, recapture or connecting revenue; their own data should decide.

**Wording:** "Full does not always mean add. The question is what the next flight adds."
**KB article:** "Spill, load factor and when another flight pays."

## Case 3: "None of our Mumbai arrivals connect"
**Channel / priority:** phone, Medium.
**Customer:** "Our connection report shows zero onward connections for the first Mumbai arrival."

1. Confirm the flight and the minimum connect time configured for the hub.
2. Compare arrival to departure banks: it lands 10:21, nine minutes after the 10:30 bank; the next useful bank is over three hours away.
3. Check the configured MCT against the airport's real rule; fix the setting if wrong, retime if right.
4. Test the retime: departing 05:30 lands 09:21, giving 69 minutes to connect.
5. Warn about side effects on the aircraft's next rotation.

**Wording:** "The arrival misses the bank by nine minutes. Departing an hour earlier fixes it, but check the aircraft's next rotation first."
**KB article:** "Why a connection is missing: MCT and bank timing."
