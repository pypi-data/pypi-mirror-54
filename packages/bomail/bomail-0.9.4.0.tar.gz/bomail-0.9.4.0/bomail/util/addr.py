####
# bomail.util.addr
#
# Utilities for dealing with email addresses
# and the "address book", which is stored in config.addr_book_file.
####

import sys
import os
from bisect import bisect_left

from bomail.config.config import pathcfg,sendcfg
import bomail.cli.mailfile as mailfile
import bomail.util.merge_lines as merge_lines
import bomail.util.util as util

####
# Address book file format: each line is
#    email_addr, N M
# where N and M are integers for num emails sent and received respectively.
# i.e. the user has sent N emails to them and received M emails from them.
#
# Python 'types' used:
# pr      A pair of strings of the form (display name, local@domain)
# prlist  A list of the form [pr, pr, ...]
#
# Plain text stuff:
#
# email_addr  An email address string of the form
#             display name <local@domain>
#             or local@domain
#             (see notes on RFC 5322 below)
####

# Ideally: email addresses could be any RFC 5322 valid recipient
# Currently: groups are not supported
# Currently: comments and quoted parts of email addresses not supported
#   (if you haven't read RFC 5322, you don't know what that is and that's ok)
# So for us, email address is local@domain where
# local and domain can contain any characters except @ < > and space

# An address-list is a comma-separated list of address strings.
# An address string is either
# (1) [display-name] <addr-spec>
# (2) addr-spec
# and addr-spec is a valid email address, which here we parse as above
# A display name can be a space-separated list of words if it doesn't contain special characters,
# else it must be a quoted string.

# My parsing rules:
# if there is no space character before the first @, then it's an addr-spec (possibly with < > around it)
# otherwise, find everything up to that space character, strip whitespace; that's the display name

RFC5322_specials = ["(" , ")" , 
                    "<" , ">",
                    "[" , "]",
                    ":" , ";",
                    "@" , "\\",
                    "," , ".",
                    '"']

RFC5322_specials_set = set(RFC5322_specials)

WHITESPACE = [' ', '\t', '\n', '\r']
MYSKIP_CHARS = [' ', '\t', '\n', '\r', ',']

def is_valid_quotestr(s):
  if len(s) < 2:
    return False
  if s[0] != '"':
    return False
  i = 1
  while i < len(s)-1:
    if s[i] == '\\':
      i += 1  # skip escaped character
    elif s[i] == '"':
      return False  # error: ended early 
    i += 1
  if i != len(s)-1 or s[-1] != '"':
    return False
  return True

def contains_specials(s):
  for c in s:
    if c in RFC5322_specials_set:
      return True
  return False

# check it either contains no special characters, or is already quoted properly
def needs_quoting(s):
  if not contains_specials(s):
    return False  # it's fine
  if is_valid_quotestr(s):
    return False
  return True

# return s, beginning and ending with a quote, and with any \ or " chars quoted
def quote(s):
  newlist = ['"']
  for c in s:
    if c == '\\' or c == '"':
      newlist.append('\\')
    newlist.append(c)
  newlist.append('"')
  return ''.join(newlist)

# This is just to guess when the user is the recipient of a message (err on the side of yes)
# canonical version that ignores case, dots, and +stuff in
# email address
# input is the second part of a pair (e.g. "local@domain")
def canon(s):
  if "@" not in s:
    return s  # no idea what's going on
  words = s.split("@")
  local, domain = words[0], words[1]
  local = local.lower()
  if "+" not in local and "." not in local:
    return s
  if "+" in local:
    local = local[:local.index("+")]
  if "." in local:
    local = local.replace(".","")
  return local + "@" + domain


# GLOBAL VARIABLE
# the user's list of email addresses
my_canon_addr_list = [canon(a) for a in sendcfg.my_aliases + sendcfg.email_addrs]



# should work on <local@domain> or local@domain
# return address (with < > stripped), end_index
# return None, None if could not parse
def get_first_addr_from_nodisp(addr_str):
  if "@" not in addr_str:
    return None, None  # no idea what to do
  at_ind = addr_str.index("@")
  end_ind = at_ind + 1
  while end_ind < len(addr_str) and addr_str[end_ind] not in [' ', ',']:
    end_ind += 1
  mypart = addr_str[:end_ind].strip()
  if len(mypart) >= 1 and mypart[0] == "<":
    mypart = mypart[1:]
  if len(mypart) >= 1 and mypart[-1] == ">":
    mypart = mypart[:-1]
  return mypart, end_ind

# return pair, end_index
# assume first character is "
# return None, None on fail
def get_first_pr_from_quoted(addr_str):
  if len(addr_str) <= 0 or addr_str[0] != '"':
    return None, None
  i = 1
  while i < len(addr_str) and addr_str[i] != '"':
    if addr_str[i] == "\\":
      i += 2
    else:
      i += 1
  if i >= len(addr_str):
    return None, None  # no address part!
  disp_name = addr_str[1:i].strip()
  addr_start = i+1
  addr_part, an_end_ind = get_first_addr_from_nodisp(addr_str[addr_start:])
  if addr_part is None:
    return None, None
  return [disp_name, addr_part], addr_start + an_end_ind

# return pair, end_index
# return None, None if fail
def get_first_pr_from_nonquoted(addr_str):
  if "@" not in addr_str:
    return None, None
  addr_start = 0
  if " " not in addr_str:
    disp_name = ''
  else:
    at_ind = addr_str.index("@")
    split_ind = addr_str.rfind(" ", 0, at_ind)
    disp_name = addr_str[:split_ind].strip()
    addr_start = split_ind + 1
  addr_part, an_end_ind = get_first_addr_from_nodisp(addr_str[addr_start:])
  if addr_part is None:
    return None, None
  return [disp_name, addr_part], addr_start + an_end_ind
  

# given plain-text comma-separated list of email addresses,
# return list of pairs
def str_to_pairlist(addr_str):
  addr_str = addr_str.strip()
  prlist = []
  index = 0
  while index < len(addr_str):
    while index < len(addr_str) and addr_str[index] in MYSKIP_CHARS:
      index += 1
    if index >= len(addr_str):
      break
    at_ind = addr_str.find('@', index)
    if at_ind < 0:
      break  # weird, rest of string has no @ sign
    elif addr_str[index] == '"':
      pair, mylen = get_first_pr_from_quoted(addr_str[index:])
    else:
      space_ind = addr_str.find(' ', index)
      if space_ind < 0 or at_ind < space_ind:  # no space in this email
        addr_part, mylen = get_first_addr_from_nodisp(addr_str[index:])
        pair = None if addr_part is None else ["", addr_part]
      else:
        pair, mylen = get_first_pr_from_nonquoted(addr_str[index:])
    if pair is None:
      break  # couldn't parse this last one
    elif needs_quoting(pair[0]):
      pair[0] = quote(pair[0])
    prlist.append((pair[0], pair[1]))
    index += mylen
  return prlist



def str_to_pairlist2(addr_str, prlist=None):
  if prlist is None:
    prlist = []
  i = 0
  while i < len(addr_str) and addr_str[i] in MYSKIP_CHARS:
    i += 1
  addr_str = addr_str[i:].strip()
  if '@' not in addr_str:
    return prlist  # no idea what this is
  elif addr_str[0] == '"':
    pair, end_ind = get_first_pr_from_quoted(addr_str)
  elif ' ' not in addr_str or addr_str.index("@") < addr_str.index(" "):
    addr_part, end_ind = get_first_addr_from_nodisp(addr_str)
    pair = None if addr_part is None else ["", addr_part]
  else:
    pair, end_ind = get_first_pr_from_nonquoted(addr_str)
  if pair is None:
    return prlist  # couldn't parse the last one

  if needs_quoting(pair[0]):
    pair[0] = quote(pair[0])
  prlist.append((pair[0], pair[1]))
  if end_ind >= len(addr_str):
    return prlist  # done
  return str_to_pairlist(addr_str[end_ind:], prlist)


# opposite direction
def pairlist_to_str(pair_list):
  return ", ".join([pair_to_str(*r) for r in pair_list])

def str_to_pair(auth_str):
  prlist = str_to_pairlist(auth_str)
  if len(prlist) > 0:
    return prlist[0]
  util.err_log("Could not get pair from: " + str(auth_str))
  return ('','')

def pair_to_str(auth, addr):
  if auth == "":
    return addr
  else:
    return auth + " <" + addr + ">"

# given a line from address book,
# return email pair and N, M
def str_to_quad(s):
  if "," not in s:
    p = str_to_pair(s)
    return (p[0], p[1], 0, 0)
  l = s.split(",")
  p = str_to_pair(l[0].strip())
  try:
    counts = l[1].split()
    return (p[0], p[1], int(counts[0].strip()), int(counts[1].strip()))
  except:
    return (p[0], p[1], 0, 0)


# given email pair and two counts,
# return a line for the address book
def quad_to_str(q):
  return pair_to_str(q[0], q[1]) + " , " + str(q[2]) + " " + str(q[3])


# check if the emails go to the same place
# not used! deprecated
#def is_recip_eq(p1, p2):
#  return canon(p1) == canon(p2)

def is_pair_me(pr):
  return canon(pr[1]) in my_canon_addr_list

def is_str_me(s):
  return is_pair_me(str_to_pair(s))


# pair_to_count is a dictionary mapping (name, email) to (#sent, #recv)
def write_addr_file(pair_to_count):
  # add my entry_quads to the dict, then flatten it to a list and write to disk
  entry_quads = [(p[0], p[1], c[0], c[1]) for p,c in pair_to_count.items()]
  entry_quads.sort()
  s = "\n".join([quad_to_str(q) for q in entry_quads])
  with open(pathcfg.addr_book_file, "w") as f:
    f.write(s)



# Mostly, this class is just used to read the list of addresses
# and to write new ones into the text file
class AddrBook:
  def __init__(self):
    self.pair_to_count = {}    # map (name, email_addr) to (send_count, recv_count)
    self.address_to_pair = {}    # map email_addr to (name, email_addr)
    self.load()


  def load(self):
    if not os.path.exists(pathcfg.addr_book_file):
      with open(pathcfg.addr_book_file, "w") as f:
        pass
    else:
      with open(pathcfg.addr_book_file) as f:
        lines = f.readlines()
      for l in [ll for ll in lines if ll.strip() != ""]:
        q = str_to_quad(l)
        self.pair_to_count[(q[0], q[1])] = (q[2], q[3])
        self.address_to_pair[q[1]] = (q[0], q[1])


  def check_for_new(self, prlist):
    added = False
    for pr in prlist:
      tuple_pr = (pr[0], pr[1])
      if tuple_pr not in self.pair_to_count:
        self.pair_to_count[tuple_pr] = (0, 0)
        self.address_to_pair[pr[1]] = tuple_pr
        added = True
    if added:
      self.rewrite_file()


  # delete all addresses in pairlist
  def remove_addresses(self, pairlist):
    rmlist = [p for p in pairlist if p in self.pair_to_count]
    if len(rmlist) != 0:
      for p in rmlist:
        del self.pair_to_count[p]
        if p[1] in self.address_to_pair:
          del self.address_to_pair[p[1]]
      self.rewrite_file()


  # delete all addresses in pairlist and add their
  # send/receive counts to merge_to
  def merge_addresses(self, merge_to, pairlist):
    c1, c2 = self.pair_to_count[merge_to]
    for pr in pairlist:
      t1, t2 = self.pair_to_count[pr]
      c1 += t1
      c2 += t2
      del self.pair_to_count[pr]
      del self.address_to_pair[pr[1]]
    self.pair_to_count[merge_to] = (c1, c2)
    self.rewrite_file()


  # look up pr in the book
  # if not present, but pr only contains an address
  # that is present, then change to that address
  def lookup_and_change(self, pr):
    if pr in self.pair_to_count:
      return pr
    if pr[0] == "" and pr[1] in self.address_to_pair:
      return self.address_to_pair[pr[1]]
    return pr


  # update our data to include any new addresses and new
  # send/receive counts
  def update_for_new(self, maildatas):
    for data in maildatas:
      fromlist = str_to_pairlist(data[mailfile.FROM_L])
      tolist = str_to_pairlist(data[mailfile.TO_L]) + str_to_pairlist(data[mailfile.CC_L]) + str_to_pairlist(data[mailfile.BCC_L])
      fromlist = [self.lookup_and_change(pr) for pr in fromlist]
      tolist = [self.lookup_and_change(pr) for pr in tolist]
      # make default entries for everything we haven't seen
      for p in [pr for pr in fromlist+tolist if pr not in self.pair_to_count]:
        self.pair_to_count[p] = (0, 0)
        self.address_to_pair[p[1]] = p
      # increment counts depending on if sent or received
      if data[mailfile.SENT_L] == "True":
        for p in tolist:
          cnt = self.pair_to_count[p] if p in self.pair_to_count else (0, 0)
          self.pair_to_count[p] = (cnt[0] + 1, cnt[1])
      else:
        for p in fromlist:
          cnt = self.pair_to_count[p] if p in self.pair_to_count else (0, 0)
          self.pair_to_count[p] = (cnt[0], cnt[1] + 1)
    self.rewrite_file()

 
  # save our address book to the text file
  def rewrite_file(self):
    write_addr_file(self.pair_to_count)

