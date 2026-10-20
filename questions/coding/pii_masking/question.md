---
title: Mask PII in support notes
difficulty: easy
category: coding
tags: regex, strings
---
Support agents paste free text into tickets. Before it is stored we mask emails and phone numbers.

## Part 1: Emails

Implement `mask_emails(text)`. An email is `local@domain.tld` where local uses letters, digits, `.`, `_`, `+`, `-`,
and the domain is one or more dot separated labels of letters, digits and `-`, ending in a tld of 2+ letters.
Replace the local part with its first character followed by `***`, keep the domain:
`jane.doe@lyft.com` becomes `j***@lyft.com`. Everything else stays exactly as it was.

## Part 2: Phones

Implement `mask_phones(text)`. A phone is 10 digits, optionally with a leading `+1 ` or `1-`, written as
`4155550123`, `415-555-0123`, `(415) 555-0123` or `415.555.0123`. Replace the whole match with `***-***-` and the last
4 digits: `call (415) 555-0123 now` becomes `call ***-***-0123 now`. Digits that are part of a longer number
(like an order id `123456789012`) must not be touched.

Finally `mask_all(text)` applies both.
