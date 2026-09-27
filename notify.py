# -*- coding: utf-8 -*-
"""Telling somebody a booking has come in.

A reservation that only lands in the database is a reservation nobody
answers, so every new one is handed straight to WhatsApp: the customer is
given a pre-filled message to send from their own phone, which arrives
instantly where staff already look.

The hand-off is not allowed to lose a booking. The row is committed before
the message is ever built, and /admin/reservations lists every booking
whether or not the customer completed the WhatsApp step.

A server that sends WhatsApp on its own needs the WhatsApp Business API
(Twilio, Meta), which costs money per message and requires business
verification plus pre-approved templates. Nothing here needs an account
anywhere.

Check the message a customer would send, without waiting for a real one:

    python3 notify.py
"""
from urllib.parse import quote

import content


def booking_lines(booking):
    """The booking as labelled lines, ready to drop into a message."""
    lines = [
        f"שם: {booking['customer_name']}",
        f"טלפון: {booking['phone']}",
        f"תאריך: {booking['date']}",
        f"שעה: {booking['time']}",
        f"מספר סועדים: {booking['party_size']}",
    ]
    if booking.get('notes'):
        lines.append(f"הערות: {booking['notes']}")
    return lines


def whatsapp_text(booking, lang='he'):
    """The message the customer sends, written from their side."""
    if lang == 'fr':
        head = f"Bonjour, je souhaite réserver une table chez {content.RESTAURANT['name_latin']} :"
        body = [
            f"Nom : {booking['customer_name']}",
            f"Téléphone : {booking['phone']}",
            f"Date : {booking['date']}",
            f"Heure : {booking['time']}",
            f"Nombre de convives : {booking['party_size']}",
        ]
        if booking.get('notes'):
            body.append(f"Remarques : {booking['notes']}")
    else:
        head = f'היי, אני רוצה להזמין שולחן ב"{content.RESTAURANT["name_he"]}":'
        body = booking_lines(booking)
    return head + "\n\n" + "\n".join(body)


def whatsapp_url(booking, lang='he'):
    return f"https://wa.me/{content.RESTAURANT['whatsapp']}?text={quote(whatsapp_text(booking, lang))}"


if __name__ == '__main__':
    # A dry run, so the hand-off can be read before a real customer
    # depends on it.
    sample = {
        'customer_name': 'בדיקה', 'phone': '050-0000000',
        'date': '2026-09-01', 'time': '19:00', 'party_size': 2,
        'notes': 'הודעת בדיקה מהאתר',
    }
    print(f"sends to : wa.me/{content.RESTAURANT['whatsapp']}\n")
    print("The message the customer would send:\n")
    print(whatsapp_text(sample))
    print("\nThe link behind the button:")
    print("  " + whatsapp_url(sample)[:110] + "...")
