
# bomail.config.optconfig
# Options not in bomailrc (may edit)


# how many new emails to process at a time, -1 for no limit
process_new_limit = -1

# how many new emails to process in a batch, decrease to save memory
# for very large imports
process_batch_size = 1000

# tag drafts with same tags as parent
autotag_draft_replies = True

## Replying to emails
## Will replace %from, %to, %cc, %date, %time, %subject, %body
##   with the corresponding text from the quoted email.

# quote_format = """\n
# %from wrote on %date at %time:
# %body"""

quote_format = """\n
From: %from
Date: %date at %time
Subject: %subject

%body"""



## %a is day of week; %Y,%m,%d are year/month/date
## %H,%M are hour/minute; %Z is timezone name, %z is timezone offset +hh
quote_date_fmt = "%a, %Y-%m-%d"
quote_time_fmt = "%H:%M UTC%z"
quote_line_prefix = "> "

