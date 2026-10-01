# Outreach runbook (each scheduled wake-up)
Sender: Victor Nweze (connected Gmail). Lists: invoice "ready" rows first, then German real estate "ready" rows (outreach/queue.json).
Pace: one email per wake, next wake 20–35 min later; Mon–Fri 09:00–17:00 recipient local time; daily cap 20 (week 1), 30 (week 2), 40 after.

1. Replies: mcp__Gmail__search_threads query `in:inbox -from:me newer_than:3d` (and `from:mailer-daemon newer_than:3d`).
   For each thread whose id/sender matches outreach/state.json "sent" and whose email has no status yet:
   - Bounce -> `python3 outreach/outreach.py mark <email> bounced`.
   - Opt-out ("no thanks", unsubscribe, not interested) -> mark optout; send one short polite confirmation; never email again.
   - Any other reply -> read thread (get_thread PLAIN_TEXT), reply as Victor Nweze: thank them, answer briefly and honestly
     (no prices, promises or invented facts), propose a short call and ask for a good time; mark replied with a 1-line summary.
   - Notify the user (PushNotification + chat line) for every reply: company, gist, what was answered.
2. Send: `python3 outreach/outreach.py next`. If it returns an email -> mcp__Gmail__send_message (to/subject/body exactly),
   then `python3 outreach/outreach.py record <idx> <id> <threadId>`.
3. Commit + push outreach/ and the two spreadsheets.
4. Reschedule with mcp__Claude_Code_Remote__send_later: delay_after minutes, or `at` = wait_until. Stop when {"done":true}.
