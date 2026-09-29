# Before the site goes live

The contact details and hours are now real. What is left below still needs
your input.

## 1. Contact details — edit `content.py`

All of these live in one dict at the top of `content.py`.

Done:

| Field | Value | Where it shows |
|---|---|---|
| `phone_display` / `phone_tel` | `09-7730201` | Footer, menu, hero call button |
| `mobile_display` / `mobile_tel` | `054-445-2833` | Under the landline everywhere; the mobile bar calls this one |
| `mobile2_display` / `mobile2_tel` | `052-708-1255` | Right after the first mobile; `None` hides it |
| `whatsapp` | `972544452833` | WhatsApp buttons (events enquiry, footer) |
| `address_he` / `address_fr` | Hotel Blue Weiss, Netanya | Footer, "how to get here" |
| `instagram` / `facebook` | set | Footer icons |

Still open:

| Field | Current | Why it matters |
|---|---|---|
| `lat` / `lng` | `None` | Waze + Google Maps links |
| `tiktok` | `None` | Icon stays hidden until set |

**On `lat`/`lng`:** while these are `None`, the map links search by the
address string. Filling in coordinates makes Waze open directly into
navigation, which is much more reliable. Get them by right-clicking the
restaurant in Google Maps and copying the numbers.

## 2. Opening hours — done

Sunday–Thursday 16:00–22:00, Friday and Saturday closed.

**Hours live in the database, not in a file.** `DEFAULT_HOURS` in
`seed_data.py` is only used to fill an empty table — editing it does nothing
to a database that already has hours in it. Two ways to change them:

- **/admin/hours** — the normal way. Each day has a lunch pair and a dinner
  pair; leave the dinner pair blank for a day with one service.
- `python3 seed_data.py --reset-hours` — forces `DEFAULT_HOURS` back over
  whatever the database holds.

The homepage shows a live "open now / closed now" badge driven by these
hours, and it now respects the afternoon break.

## 3. Admin password — done

The old password was written in this file, which made it a published
password. It has been rotated, and there is no default in the code any more.

To change it, from `neomi-restaurant/`:

    python3 seed_data.py --set-admin-password

It asks twice, hides your typing, and requires at least 10 characters. On a
host with no terminal, set `NEOMI_ADMIN_PASSWORD` in the dashboard instead
and run the same command. With neither, it generates a strong one and prints
it once.

Never write the password back into this file or any other file in the repo.

## 4. The story — done

You supplied it on 25/08/2026 and it is live at **`/about`** ("הסיפור שלנו" /
"Notre histoire"), in the top navigation and the footer. Five chapters: the
roots (Mamie Neomi in Tunis), the kitchen, the kashrut, the table, and
events. The Hebrew is close to your own words; the French
is a translation of them, using the printed menu's spellings (Brick,
Banatagge, Complet Poisson, Chakchouka).

**Neomi has passed away, and the page is written accordingly.** She is
spoken of in the past tense throughout, the recipes are described as having
passed to the family, and the first mention in each language carries the
traditional honorific — **ז״ל** in Hebrew, *de mémoire bénie* in French.

Please read chapter 1 and tell me if any of it sits wrong. Three choices
there were mine, and any of them is a one-line change:

- **The honorific.** I added ז״ל because on a kosher-lemehadrin restaurant's
  own site its absence would read as carelessness. If the family would
  rather it were not there, it comes out in one edit.
- **How plainly the passing is stated.** The page says *"סבתא נעמי כבר
  איננה, אבל המתכונים שלה נשארו במשפחה"* — gentle, and it does not dwell.
  It can be softened further (leaving only the past tense to carry it) or
  made more explicit, whichever the family prefers.
- **A dedication.** The page does not carry one. If you would like a line
  in her memory — a date, a place, or simply *לזכרה* — tell me the wording
  and I will set it properly.

One thing that is now true and worth knowing: the portrait on the page is a
framed photograph of her propped in the kitchen, which reads very differently
once you know she has passed. It is, I think, the right photo. Say so if you
disagree and I will change it.

Still open from your text: **מינינה** and **פלפל ממולא** appear in the story
but not on the printed menu, so I have presented them as part of the kitchen
rather than as menu items. Correct me if they belong on the card.

All the copy lives in `i18n.py` under the `about_page_*` and `about_ch*`
keys, so any change is one file.

## 5. The kashrut certificate expires 31/08/2026

The certificate shown at `/kosher` is valid 09/04/2026 – 31/08/2026. After
that date the page stops claiming the restaurant is certified and shows a
"renewed certificate coming soon" notice instead — deliberately, because a
stale kashrut claim is worse than no claim.

To publish the renewal:

1. Photograph the new certificate and save it over
   `photos/לוגו/kosher.JPG` (any orientation — the build reads the EXIF
   rotation and straightens it).
2. Update `kosher_valid_from` and `kosher_valid_until` in `content.py`.
3. `python3 tools/build_assets.py`

## 6. Two more videos are available but unused

ffmpeg is now available to the build (via the `imageio-ffmpeg` package), so
the blocker here is gone — these two simply are not on the site yet:

- `אוירה/ערוך קטעים.MOV`
- `רקע/מסעדת נעמי בואו לטעום(1).mov`

The second one ("בואו לטעום" — *come and taste*) is the site's own tagline
and looks like it belongs on the homepage. To use either, add an entry to
`VIDEOS` in `tools/build_assets.py` copying the shape of the two already
there, then either add it to the gallery in `content.py` or point the
homepage hero at it in `templates/index.html`. Say the word and I will.

## 7. Table bookings reach you through WhatsApp only

The site sends no email. A booking saves a row and hands the customer a
pre-filled WhatsApp message to send from their own phone; nothing is
published from the server on its own.

That has one consequence worth knowing: **a customer who fills in the form
and then closes the tab without tapping the WhatsApp button leaves you a
booking that nothing announces.** It is saved, and it is listed at
`/admin/reservations` — but only if somebody looks. Check that page daily,
the way you would check an answering machine.

If that turns out to be too fragile in practice, say the word and I will add
a notification that does not depend on the customer — a Telegram message to
your phone is free and takes about ten minutes to wire up.

## 8. A server that sends WhatsApp by itself costs money

What is built is a hand-off: the customer taps a button and sends the
message from their own WhatsApp. That is free and instant, but it depends on
the customer completing the step — see the note above.

For the server to send WhatsApp on its own you need the WhatsApp Business
API through Twilio or Meta: roughly $0.005–0.04 per message, a verified
business, and message templates approved in advance. Worth it only if the
hand-off proves unreliable in practice.

## 9. Ordering is built but not promoted — and you do not sell takeaway

You confirmed on 25/08/2026 that **no prepared food for Friday or Shabbat is
made**, so the `/about` page says nothing about it. An earlier draft did;
it has been removed, and there is a note in `i18n.py` next to the events
copy so it does not creep back in.

That leaves `/order` — the delivery-and-pickup page — as the odd one out. It
works with the real menu and prices, but it is only reachable from the
footer and nothing else on the site points at it. Three ways to resolve it:

- **Not offered at all** → I remove the page, the `Order`/`OrderItem`
  models and the cart JavaScript. This is the tidiest outcome if takeaway
  simply is not a thing you do.
- **Pickup only** → I drop the delivery option and the address field, and
  decide with you whether it goes in the navigation.
- **Leave it as it is** → it stays reachable from the footer for anyone who
  finds it. Fine, but it currently accepts orders that nothing notifies you
  about (see §7), which is worse than not having it.

My recommendation is the first, unless you actually take phone orders for
collection.

## 10. Prices show "not including 10% service"

Taken from the printed menu (`service_note` in `i18n.py`). Worth confirming
that is still current.
