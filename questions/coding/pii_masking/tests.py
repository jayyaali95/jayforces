from check import table

table(globals(), 1, lambda s, t: s.mask_emails(t), [
    ("basic", "jane.doe@lyft.com", "j***@lyft.com"),
    ("in sentence", "mail bob@ex.io today", "mail b***@ex.io today"),
    ("subdomain", "x_y@mail.corp.lyft.com", "x***@mail.corp.lyft.com"),
    ("plus tag", "a+rides@gmail.com.", "a***@gmail.com."),
    ("two emails", "a@b.co, c@d.org", "a***@b.co, c***@d.org"),
    ("not an email", "meet @ 5pm at lyft.com", "meet @ 5pm at lyft.com"),
    ("short tld rejected", "a@b.c", "a@b.c"),
])
table(globals(), 2, lambda s, t: s.mask_phones(t), [
    ("plain digits", "4155550123", "***-***-0123"),
    ("dashes", "call 415-555-0123", "call ***-***-0123"),
    ("parens", "call (415) 555-0123 now", "call ***-***-0123 now"),
    ("dots", "415.555.0123", "***-***-0123"),
    ("country code", "+1 415-555-0123", "***-***-0123"),
    ("one dash prefix", "1-415-555-0123", "***-***-0123"),
    ("long number untouched", "order 123456789012", "order 123456789012"),
    ("short number untouched", "code 55501", "code 55501"),
    ("two phones", "4155550123 or 6505551111", "***-***-0123 or ***-***-1111"),
])
table(globals(), 2, lambda s, t: s.mask_all(t), [
    ("both", "jane@lyft.com / 415-555-0123", "j***@lyft.com / ***-***-0123"),
    ("nothing to mask", "rider was happy", "rider was happy"),
])
