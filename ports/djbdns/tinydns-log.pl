#!/usr/bin/perl -p

# tinydns log formatting utility
# based on Faried Nawaz's logfile formatter for dnscache
# by Kenji Rikitake <kenji.rikitake@acm.org> 29-JUL-2000
# please put this on dnscache.com ftp site.

# convert addresses in hex to dotted decimal notation.
s/\b([a-f0-9]{8})\b/join(".", unpack("C*", pack("H8", $1)))/eg;

### clean up some messages
# convert stuff like 127.0.0.2:0422:05be to something more descriptive.
# query tai64n host:port:qid flag qtype thing
# keep tai64n header as is - use tai64nlocal to convert it to TAI

s/^(@[a-f0-9]+) \b([\d.]+):(\w+):(\w+) ([\+\-\I\/]) \b([a-f0-9]+) \b([-.\w]+)/$1." ".printQueryLine($2,$3,$4,$5,$6,$7)/e;

### subs

sub printQueryLine {
  my ($host, $port, $query_id, $flag, $query_type, $query) = @_;

  # pad hostname

  my $ret = "$host:";
  $ret .= hex($port);
  $ret .= ":" . hex($query_id);
  $ret .= " " . $flag;
  $ret .= " " . queryType(hex($query_type)) . " $query";
  
  return $ret;
}

sub queryType {
  my ($type) = shift;

  my $ret = "";
 
 # i only list the ones that are in dnscache's dns.h.
 SWITCH: {
    ($type == 1)        && do { $ret = "a";     last SWITCH; };
    ($type == 2)        && do { $ret = "ns";    last SWITCH; };
    ($type == 5)        && do { $ret = "cname"; last SWITCH; };
    ($type == 6)        && do { $ret = "soa";   last SWITCH; };
    ($type == 12)       && do { $ret = "ptr";   last SWITCH; };
    ($type == 13)       && do { $ret = "hinfo"; last SWITCH; };
    ($type == 15)       && do { $ret = "mx";    last SWITCH; };
    ($type == 16)       && do { $ret = "txt";   last SWITCH; };
    ($type == 17)       && do { $ret = "rp";    last SWITCH; };
    ($type == 24)       && do { $ret = "sig";   last SWITCH; };
    ($type == 25)       && do { $ret = "key";   last SWITCH; };
    ($type == 28)       && do { $ret = "aaaa";  last SWITCH; };
    ($type == 252)      && do { $ret = "axfr";  last SWITCH; };
    ($type == 255)      && do { $ret = "any";   last SWITCH; };
    do { $ret .= "$type "; last SWITCH; };
  }
  return $ret;
}

