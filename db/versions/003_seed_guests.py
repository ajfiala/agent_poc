"""
003_seed_guests

Revision ID: 0003_seed_guests
Revises: 0002_seed_data
Create Date: 2025-01-09
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_seed_guests'
down_revision = '0002_seed_data'
branch_labels = None
depends_on = None


def upgrade():
    guests = [
        ("Peter Griffin",      "peter.bigbelly@puffy.com",         "(715) 555-0101"),
        ("Lois Griffin",    "lois.lovehandles@chewmail.com",    "(715) 555-0102"),
        ("Chris  Griffin",  "chris.cheeseburger@oddmail.net",   "(715) 555-0103"),
        ("Meg  Griffin",       "meg.muffintop@puffy.com",          "(715) 555-0104"),
        ("Stewie  Griffin",      "stewie.stuffed@breadmail.org",     "(715) 555-0105"),
        ("Brian Griffin",         "brian.bulge@plumpmail.com",        "(715) 555-0106"),
        ("Cleveland Brown", "cleveland.cheese@puffy.com",       "(715) 555-0107"),
        ("Joe Swanson",       "joe.jellyroll@oddmail.net",        "(715) 555-0108"),
        ("Glenn Quagmire",      "glenn.glutton@chewmail.com",       "(715) 555-0109"),
        ("Bonnie Swanson",   "bonnie.butterball@plumpmail.com",  "(715) 555-0110"),
        ("Herbert",           "herbert.heavyhank@puffy.com",      "(715) 555-0111"),
        ("Carter Pewterschmidt", 
                                           "carter.corpulent@oddmail.net",     "(715) 555-0112"),
        ("Barbara Pewterschmidt", 
                                           "barbara.breadstick@puffy.com",     "(715) 555-0113"),
        ("Mort Goldman",       "mort.megameal@chewmail.com",       "(715) 555-0114"),
        ("Neil Goldman",  "neil.double@plumpmail.com",        "(715) 555-0115"),
        ("Bruce",             "bruce.bratwurst@puffy.com",        "(715) 555-0116"),
        ("Tom Tucker",            "tom.tubby@breadmail.org",          "(715) 555-0117"),
        ("Diane Simmons",        "diane.doughy@oddmail.net",         "(715) 555-0118"),
        ("Seamus",           "seamus.seabiscuit@puffy.com",      "(715) 555-0119"),
        ("Angela",                "angela.ample@chewmail.com",        "(715) 555-0120"),
        ("Adam West",          "adam.appetite@plumpmail.com",      "(715) 555-0121"),
        ("Dr. Elmer Hartman",     "doc.extra@puffy.com",              "(715) 555-0122"),
        ("Evil Monkey",        "evil.expanded@oddmail.net",        "(715) 555-0123"),
        ("Connie D'Amico",    "connie.chocolate@breadmail.org",   "(715) 555-0124"),
        ("Jillian Russell",       "jillian.jello@chewmail.com",       "(715) 555-0125"),
        ("Horace",               "horace.hearty@puffy.com",          "(715) 555-0126"),
        ("GreasedUp Deaf Guy", "greasedup.gigantic@oddmail.net",   "(715) 555-0127"),
        ("Bertram",           "bertram.bellybust@breadmail.org",  "(715) 555-0128"),
        ("Olivia Fuller",     "olivia.oversized@puffy.com",       "(715) 555-0129"),
        ("Mayor West",          "mayor.massive@plumpmail.com",      "(715) 555-0130"),
    ]

    for (full_name, email, phone) in guests:
        stmt = sa.text(
            """
            INSERT INTO guests (full_name, email, phone)
            VALUES (:full_name, :email, :phone)
            """
        ).bindparams(full_name=full_name, email=email, phone=phone)
        op.execute(stmt)


def downgrade():
    # Remove only what we added; matching emails ensures we only delete our seeded data.
    emails = [
        "peter.bigbelly@puffy.com",
        "lois.lovehandles@chewmail.com",
        "chris.cheeseburger@oddmail.net",
        "meg.muffintop@puffy.com",
        "stewie.stuffed@breadmail.org",
        "brian.bulge@plumpmail.com",
        "cleveland.cheese@puffy.com",
        "joe.jellyroll@oddmail.net",
        "glenn.glutton@chewmail.com",
        "bonnie.butterball@plumpmail.com",
        "herbert.heavyhank@puffy.com",
        "carter.corpulent@oddmail.net",
        "barbara.breadstick@puffy.com",
        "mort.megameal@chewmail.com",
        "neil.double@plumpmail.com",
        "bruce.bratwurst@puffy.com",
        "tom.tubby@breadmail.org",
        "diane.doughy@oddmail.net",
        "seamus.seabiscuit@puffy.com",
        "angela.ample@chewmail.com",
        "adam.appetite@plumpmail.com",
        "doc.extra@puffy.com",
        "evil.expanded@oddmail.net",
        "connie.chocolate@breadmail.org",
        "jillian.jello@chewmail.com",
        "horace.hearty@puffy.com",
        "greasedup.gigantic@oddmail.net",
        "bertram.bellybust@breadmail.org",
        "olivia.oversized@puffy.com",
        "mayor.massive@plumpmail.com",
    ]
    for email in emails:
        stmt = sa.text(
            """
            DELETE FROM guests
            WHERE email = :email
            """
        ).bindparams(email=email)
        op.execute(stmt)
