# Modify the following if you will be replicating to a secondary djbdns server
# and replace [secondary_dns] with the IP address of your secondary djbdns server
#
#remote: data.cdb
#	rsync -az -e ssh data.cdb [secondary_dns]:/var/service/tinydns/root/data.cdb

it: build data.cdb

data.cdb: data
	/usr/local/bin/tinydns-data
build: zone*
	sort -u zone*|grep -v "#" >data
