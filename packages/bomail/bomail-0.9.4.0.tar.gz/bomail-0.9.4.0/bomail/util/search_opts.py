####
# bomail.util.search_opts
#
# Parse search options!
####

import os
import shlex
import datetime
import re

import bomail.cli.mailfile as mailfile
import bomail.util.tags as tags
import bomail.util.addr as addr
import bomail.util.datestuff as datestuff
from bomail.util.listmail import ListOpts

options_str = """
All arguments are optional:
 -h               [print this help]
 -n 200           only return first 200 results
 -sortold         list by oldest (default is by newest)

 -a datestr       after date. datestr can be e.g. yyyy-mm-dd
 -b datestr       before date

 -open            state is open
 -scheduled       state is scheduled
 -closed          state is closed
 -draft           is a draft
 -sent            is sent from me
 -attach          has an attachment

 -notags          has no tags
 -to-me           addressed to any of my aliases in config file

Use quotes around "space separated strings" for these:
 -t str           has str as a tag
 -nt str          does not have str as a tag
 -to str          str is in to, cc, or bcc field
 -from str        str is in from field
 -subject str     str is in subject field
 str              str is in email somewhere

Can use -t "str1, str2" as shorthand for -t str1 -t str2.
"""


def with_quotes(q):
  return ('"' if q[0] != '"' else '') + q + ('"' if q[-1] != '"' else '')

# add query q to search string
def get_new_search_str(old_str, q):
  sq = SearchQuery()
  args = shlex.split(old_str)
  sq.parse(args)

  # if no search query in old string, just append this one
  if len(sq.querylist) == 0:
    return old_str + " " + with_quotes(q)

  # otherwise, add it to every search query
  ind = 0
  outargs = []
  while True:
    if ind >= len(args):
      break
    if args[ind] in ['-n', '-a', '-b', '-t', '-nt', '-to', '-from', '-subject']:
      outargs += args[ind:ind+2]
      ind += 2
    elif args[ind] in ['-sortold', '-open', '-scheduled', '-closed', '-draft', '-sent', '-attach', '-notags', '-to-me']:
      outargs += args[ind:ind+1]
      ind += 1
    else:
      outargs.append(with_quotes(args[ind] + ", " + q))
      ind += 1
  return " ".join(outargs)



class SearchQuery:
  def __init__(self):
    self.max_num = -1  # indiciates unlimited
    self.reverse = False

    self.listopts = ListOpts()
    self.can_list_only = True      # True if ListOpts can list all matching files
    self.can_filename_only = True  # True if only need filename
    self.orig_after_str = None
    self.orig_before_str = None
    self.after_str = None
    self.before_str = None

    # Can be found by listing (without opening files)
    self.open = None
    self.scheduled = None
    self.draft = None
    self.attach = None

    # Cannot be found by listing
    self.sent = None
    self.closed = None

    self.tagset = None      # must match all
    self.not_tagset = None  # must not match any
    self.tolist = None      # must match all
    self.fromlist = None    # ditto
    self.subjectlist = None # ditto

    self.rough_regex_list = []  # regular expression to 'grep' with

    self.notags = None  # or True
    self.tome = None    # or True

    self.querylist = None  # must match all


  def parse(self, old_arglist):
    arglist = list(old_arglist)
    if "-n" in arglist:
      i = arglist.index("-n")
      del arglist[i]
      if len(arglist) > i:
        try:
          self.max_num = int(arglist[i])
        except:
          self.max_num = 0
        del arglist[i]

    if "-sortold" in arglist:
      self.reverse = True
      arglist.remove("-sortold")

    if "-a" in arglist:
      i = arglist.index("-a")
      del arglist[i]
      if len(arglist) > i:
        s = arglist[i]
        self.orig_after_str = s
        del arglist[i]
    if "-b" in arglist:
      i = arglist.index("-b")
      del arglist[i]
      if len(arglist) > i:
        s = arglist[i]
        self.orig_before_str = s
        del arglist[i]
  
    # check draft first because it comes from a separate list
    # so it is always handled by listmail, not filter
    if "-draft" in arglist:
      self.listopts.source = "draft"
      self.draft = True
      arglist.remove("-draft")
    if "-open" in arglist:
      self.can_filename_only = False
      if self.listopts.source == "all":
        self.listopts.source = "open"
      else:
        self.can_list_only = False  # must check both draft and open
      self.open = True
      arglist.remove("-open")
    if "-scheduled" in arglist:
      self.can_filename_only = False
      if self.listopts.source == "all":
        self.listopts.source = "scheduled"
      else:
        self.can_list_only = True
      self.scheduled = True
      arglist.remove("-scheduled")
    if "-attach" in arglist:
      self.can_filename_only = False
      if self.listopts.source == "all":
        self.listopts.source = "attach"
      else:
        self.can_list_only = False
      self.attach = True
      arglist.remove("-attach")

    if "-sent" in arglist:
      self.can_filename_only = False
      self.sent = True
      self.can_list_only = False
      arglist.remove("-sent")
    if "-closed" in arglist:
      self.can_filename_only = False
      self.closed = True
      self.can_list_only = False
      arglist.remove("-closed")

    while "-t" in arglist:
      self.can_filename_only = False
      self.can_list_only = False
      i = arglist.index("-t")
      del arglist[i]
      if len(arglist) < i:
        break
      tagstr = arglist[i]
      myset = tags.get_tagset_from_str(tagstr, include_folders=False)
      if len(myset) > 0:
        self.rough_regex_list.extend(myset)
        if self.tagset is None:
          self.tagset = myset
        else:
          self.tagset.update(myset)
      del arglist[i]

    while "-nt" in arglist:
      self.can_filename_only = False
      self.can_list_only = False
      i = arglist.index("-nt")
      del arglist[i]
      if len(arglist) < i:
        break
      tagstr = arglist[i]
      myset = tags.get_tagset_from_str(tagstr, include_folders=False)
      if len(myset) > 0:
        if self.not_tagset is None:
          self.not_tagset = myset
        else:
          self.not_tagset.update(myset)
      del arglist[i]

    while "-to" in arglist:
      self.can_filename_only = False
      self.can_list_only = False
      i = arglist.index("-to")
      del arglist[i]
      if len(arglist) < i:
        break
      mylist = [s.strip() for s in arglist[i].split(",")]
      self.rough_regex_list.extend(mylist)
      if self.tolist is None:
        self.tolist = mylist
      else:
        self.tolist.extend(mylist)
      del arglist[i]

    while "-from" in arglist:
      self.can_filename_only = False
      self.can_list_only = False
      i = arglist.index("-from")
      del arglist[i]
      if len(arglist) < i:
        break
      mylist = [s.strip() for s in arglist[i].split(",")]
      self.rough_regex_list.extend(mylist)
      if self.fromlist is None:
        self.fromlist = mylist
      else:
        self.fromlist.extend(mylist)
      del arglist[i]

    while "-subject" in arglist:
      self.can_filename_only = False
      self.can_list_only = False
      i = arglist.index("-subject")
      del arglist[i]
      if len(arglist) < i:
        break
      mylist = [s.strip() for s in arglist[i].split(",")]
      self.rough_regex_list.extend(mylist)
      if self.subjectlist is None:
        self.subjectlist = mylist
      else:
        self.subjectlist.extend(mylist)
      del arglist[i]

    if "-notags" in arglist:
      self.can_filename_only = False
      self.can_list_only = False
      self.notags = True
      arglist.remove("-notags")

    if "-to-me" in arglist:
      self.can_filename_only = False
      self.can_list_only = False
      self.tome = True
      arglist.remove("-to-me")

    if len(arglist) > 0:
      self.can_filename_only = False
      self.can_list_only = False
      self.rough_regex_list.extend(arglist)
      self.querylist = [re.compile(re.escape(s)) for s in arglist]

    for i in range(len(self.rough_regex_list)):
      self.rough_regex_list[i] = re.compile(re.escape(self.rough_regex_list[i]))


  # generate python code that only checks the files for items in the query
  def do_compile(self):
    slist = ["matched_inds = []\n"]
    slist.append("for ind,f in enumerate(flist):\n")

    # do filename-based stuff first
    # use that we store filenames with date in them (except drafts!)
    need_date = self.after_str is not None or self.before_str is not None
    if need_date:
      slist.append("  if not filename_matches_date(f, self.after_str, self.before_str):\n")
      slist.append("    continue\n")
    if self.draft is not None:
      slist.append("  if f[-5:] != \"draft\":\n")
      slist.append("    continue\n")

    # now do non-filename-based stuff
    if not self.can_filename_only:
      self.get_compile_data_checks(slist)

    # if we made it to the end of the loop, this one matches
    slist.append("  matched_inds.append(ind)\n")

    # stop the loop if we've found enough
    if self.max_num > 0:
      slist.append("  if len(matched_inds) >= " + str(self.max_num) + ":\n")
      slist.append("    break\n")


     # save the compiled search query to file
    with open("compile_log.txt", "w") as myf:
      myf.write("".join(slist))
    return compile("".join(slist), '<string>', 'exec')
    

  # for compiling a query, get all the checks that involve file data
  def get_compile_data_checks(self, slist):
    slist.append("  with open(f) as my_file:\n")
    slist.append("    contents = my_file.read()\n")

    # do a rough check through the file before exact checks
    if len(self.rough_regex_list):
    #### if self.case_sensitive...
      slist.append("  if not all([myre.search(contents) for myre in self.rough_regex_list]):\n")
      slist.append("    continue\n\n")

    slist.append("  data = mailfile.parse_file_contents(contents, f)\n")

    if self.notags:
      slist.append("  if len(data[mailfile.TAGS_L]) > 0:\n")
      slist.append("    continue\n")
    
    if self.open is not None:
      slist.append("  if not data[mailfile.STATE_L].startswith(\"open\"):\n")
      slist.append("    continue\n")
    if self.scheduled is not None:
      slist.append("  if not data[mailfile.STATE_L].startswith(\"scheduled\"):\n")
      slist.append("    continue\n")
    if self.closed is not None:
      slist.append("  if not data[mailfile.STATE_L].startswith(\"closed\"):\n")
      slist.append("    continue\n")
    if self.sent is not None:
      slist.append("  if not data[mailfile.SENT_L] == \"True\":\n")
      slist.append("    continue\n")
    if self.attach is not None:
      slist.append("  if len(data[mailfile.ATTACH_L]) == 0:\n")
      slist.append("    continue\n")

    if self.tome is not None:
      slist.append("  prlist_list = [addr.str_to_pairlist(data[j]) for j in [mailfile.TO_L, mailfile.CC_L, mailfile.BCC_L]]\n")
      slist.append("  if not any([any([addr.is_pair_me(pr) for pr in prlist]) for prlist in prlist_list]):\n")
      slist.append("    continue\n")

    # need to match all of a set
    if self.tagset is not None or self.not_tagset is not None:
      slist.append("  data_tagset = tags.get_tagset_from_str(data[mailfile.TAGS_L], include_folders=True)\n")
    if self.tagset is not None:
      slist.append("  if self.tagset.issubset(data_tagset):\n")
      slist.append("    continue\n")
    # if we match any of these, skip
    if self.not_tagset is not None:
      slist.append("  if self.not_tagset & data_tagset:\n")
      slist.append("    continue\n")
    # need to match all addresses
    if self.tolist is not None:
      slist.append("  if not all([s in data[mailfile.TO_L] or s in data[mailfile.CC_L] or s in data[mailfile.BCC_L] for s in self.tolist]):\n")
      slist.append("    continue\n")
    if self.fromlist is not None:
      slist.append("  if not all([s in data[mailfile.FROM_L] for s in self.fromlist]):\n")
      slist.append("    continue\n")
    if self.subjectlist is not None:
      slist.append("  if not all([s in data[mailfile.SUBJ_L] for s in self.subjectlist]):\n")
      slist.append("    continue\n")

    # every query must have all their strings somewhere
    if self.querylist is not None:
      #if self.case_sensitive:
        slist.append("  if not all([any([q.search(s, re.IGNORECASE) for s in data]) for q in self.querylist]):\n")
        slist.append("    continue\n")
      #else:
      #  slist.append("  if not all([any([re.search(q, s) for s in data]) for q in self.querylist])\n")
      #  slist.append("    continue\n")
  # end of extra search steps


  # convert relative dates and time zones to absolute UTC
  def interpret_dates(self):
    self.after_str = None
    self.before_str = None
    if self.listopts is not None:
      self.listopts.after_str = None
      self.listopts.before_str = None
    if self.orig_after_str is not None:
      self.after_str = datestuff.parse_schedstr_to_utcstr(self.orig_after_str)
      if self.listopts is not None:
        self.listopts.after_str = self.after_str[:10]
    if self.orig_before_str is not None:
      self.before_str = datestuff.parse_schedstr_to_utcstr(self.orig_before_str)
      if self.listopts is not None:
        self.listopts.before_str = self.before_str[:10]
                        

  # list all files matching basic part of query
  # (should filter them after this, unless self.can_list_only)
  def listmail(self, mgr):
    self.interpret_dates()
    flist = self.listopts.listmail(mgr)
    if self.reverse:
      flist.reverse()
    return flist

  # return list of indices matching our query on filenames
  def filter(self, mgr, flist):
    self.interpret_dates()
    compiled_obj = self.do_compile()
    namespace ={"re": re, "self": self, "addr": addr, "filename_matches_date": datestuff.filename_matches_date, "mailfile": mailfile, "tags": tags, "flist": flist}
    exec(compiled_obj, namespace)
    return namespace["matched_inds"]

  def search(self, mgr):
    result = self.listmail(mgr)
    if not self.can_list_only:
      matched_inds = self.filter(mgr, result)
      result = [result[i] for i in matched_inds] 
    if self.max_num > 0:
      return result[:self.max_num]
    return result


