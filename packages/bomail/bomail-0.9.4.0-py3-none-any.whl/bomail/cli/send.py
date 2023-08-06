####
# bomail.cli.send
#
# Send drafts.
####

import os
import sys
import mimetypes
import subprocess, email
import smtplib
import traceback
import socket

from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

from bomail.config.config import pathcfg,sendcfg
import bomail.cli.mailfile as mailfile
import bomail.util.addr as addr
import bomail.util.util as util

usage_str = """
Reads filename(s) from stdin one per line and sends them.
send.py -h to print this help.
"""


# adapted from python library example: https://docs.python.org/3/library/email-examples.html
def add_attachments(msg, attach_list):
  for filename in attach_list:
    if not os.path.exists(filename):
      raise Exception("Did not send. Could not attach (does not exist): " + filename)
    if not os.path.isfile(filename):
      raise Exception("Did not send. Could not attach (is not a file): " + filename)
    ctype, encoding = mimetypes.guess_type(filename)
    if ctype is None or encoding is not None:
      ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
      with open(filename) as fp:
        sub_msg = MIMEText(fp.read(), _subtype=subtype)
    elif maintype == 'image':
      with open(filename, 'rb') as fp:
        sub_msg = MIMEImage(fp.read(), _subtype=subtype)
    elif maintype == 'audio':
      with open(filename, 'rb') as fp:
        sub_msg = MIMEAudio(fp.read(), _subtype=subtype)
    else:
      with open(filename, 'rb') as fp:
        sub_msg = MIMEBase(maintype, subtype)
        sub_msg.set_payload(fp.read())
      encoders.encode_base64(sub_msg)
    sub_msg.add_header('Content-Disposition', 'attachment', filename=os.path.split(filename)[1])
    msg.attach(sub_msg)


# convert file to a python message
# if multiple "from" addresses, use Sender header with sender_str
def file_to_msg(fname, sender_str, mgr):
  data = mgr.get_all(fname)
  attach_list = mgr.get_attachlist(fname)
  if len(attach_list) == 0:  # no attachments
    msg = MIMEText(data[mailfile.BODY_L], 'plain')
  else:
    msg = MIMEMultipart()
    msg.attach(MIMEText(data[mailfile.BODY_L], 'plain'))
    add_attachments(msg, attach_list)
  msg['Subject'] = data[mailfile.SUBJ_L]
  msg['From'] = data[mailfile.FROM_L]
  if len(addr.str_to_pairlist(data[mailfile.FROM_L])) > 1:
    msg['Sender'] = sender_str
  msg['To'] = data[mailfile.TO_L]
  msg['Date'] = email.utils.formatdate()
  msg['Message-ID'] = data[mailfile.MSG_ID_L]
  if len(data[mailfile.CC_L]) > 0:
    msg['CC'] = data[mailfile.CC_L]
  refs = data[mailfile.REFS_L]
  if len(data[mailfile.REPLY_L]) > 0:
    msg['Reply-To'] = data[mailfile.REPLY_L]
  if len(refs) > 0:
    msg['In-Reply-To'] = refs.split(", ")[-1]
    msg['References'] = refs

  recip_lists = data[mailfile.TO_L].split(", ")
  if len(data[mailfile.CC_L]) > 0:
    recip_lists += data[mailfile.CC_L].split(", ")
  if len(data[mailfile.BCC_L]) > 0:
    recip_lists += data[mailfile.BCC_L].split(", ")
  recip_addrs = [addr.str_to_pair(a)[1] for a in recip_lists]
  return recip_addrs, msg


# given list of relative filenames
# return results, msg
# where results is a list of success/not [True, False, ...]
def connect_and_send(user_ind, fnames, fname_to_senderstr, mgr):
  results = [False for f in fnames]

  try:
    if sendcfg.smtp_servernames[user_ind] == "localhost":
      serv = smtplib.SMTP("localhost")
    else:
      myhost = socket.gethostbyname(sendcfg.smtp_servernames[user_ind])  # prefer IPv4
      serv = smtplib.SMTP(myhost, sendcfg.smtp_ports[user_ind])
      serv.ehlo()
      serv.starttls()
      serv.ehlo()
      serv.login(sendcfg.smtp_usernames[user_ind], sendcfg.smtp_passwords[user_ind])
  except Exception as e:
    util.err_log("Sending email, error connecting to server.\n" + traceback.format_exc() + "\n")
    return results, "Error connecting to server: " + str(e)

  email_addr = sendcfg.email_addrs[user_ind]
  for i, fname in enumerate(fnames):
    recip_addrs, msg = file_to_msg(fname, fname_to_senderstr[fname], mgr)
    try:
      serv.sendmail(email_addr, recip_addrs, msg.as_string())
      if sendcfg.smtp_servernames[user_ind] == "localhost": # save the sent mail
        os.makedirs(pathcfg.new_rawmail_dir, exist_ok=True)
        try:
          rawname = util.mime_to_mailfile.get_msgid(m, fname)
          with open(os.path.join(pathcfg.new_rawmail_dir,rawname), "w") as rawfile:
            rawfile.write(msg.as_string())
        except:
          util.err_log("Error saving copy of sent mail:\n" + fname + "\n" + msg.as_string() + "\n")
      results[i] = True
    except Exception as e:
      serv.quit()
      util.err_log("Sending email, error while sending.\n" + traceback.format_exc() + "\n")
      return results, "Error sending message #" + str(i) + " [" + fname + "]: " + str(e)

  serv.quit()
  return results, ""


# given list of pairs, return who is the sender
# as an index into sendcfg.email_addrs
# along with the sender string it matched
def get_sender(fromlist):
  for pr in fromlist:
    try:
      user_ind = sendcfg.email_addrs.index(pr[1])
      return user_ind, addr.pair_to_str(pr[0], pr[1])
    except:
      pass
  raise Exception("no sender in list")


 

# given list of filenames
# return vector of successes [True, False, ...], err_msg
def main(flist, mgr):
  # sort them into different sender addresses and connect to each server once
  userind_to_fnames = [[] for a in sendcfg.email_addrs]
  fname_to_senderstr = {}
  for fname in flist:
    fromline = mgr.get(fname, mailfile.FROM_L)
    fromlist = addr.str_to_pairlist(fromline)
    try:
      user_ind, sender_str = get_sender(fromlist)
      userind_to_fnames[user_ind].append(fname)
      fname_to_senderstr[fname] = sender_str
    except:
      err_s = "Error! Cannot send from any of " + fromline + " in file " + fname
      util.err_log(err_s)
      return [], err_s    # sent no mails
    
  success = set()
  msg = ""
  for user_ind,fnames in enumerate(userind_to_fnames):
    res, msg = connect_and_send(user_ind, fnames, fname_to_senderstr, mgr)
    for i,good in enumerate(res):
      if good:
        success.add(fnames[i])
    if len(msg) > 0:
      break
  # return array with True if message sent
  return [f in success for f in flist], msg



def main_cli():
  if len(sys.argv) >= 2:
    print(usage_str)
    exit(0)

  flist = [f.strip() for f in sys.stdin.readlines()]
  res, err = main(flist, mailfile.MailMgr())
  print("Sent " + str(res) + "/" + str(len(flist)) + " messages.")
  if res < len(flist):
    print(err)


if __name__ == "__main__":
  main_cli()


