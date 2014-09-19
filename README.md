# Dyn DNS cli tool
### Usage
```
usage: dyncli [-h] [-e ENDPOINT] [-c CREATE] [--cname] [-v VALUE] [-t TTL]
              [-d DELETE] [-u UPDATE_RECORD] [-U USER] [-P PASSWORD]
              [-A ACCOUNT] [-Z ZONE] [-l] [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT, --endpoint ENDPOINT
                        The endpoint to make API requests.
  -c CREATE, --create CREATE
                        Create a new record. Defaults to A record unless
                        --cname is set.
  --cname               Create a cname record instead of an A record.
  -v VALUE, --value VALUE
                        The value to set the DNS record to. Eg 10.0.0.101.
  -t TTL, --ttl TTL     TTL of record in seconds.
  -d DELETE, --delete DELETE
                        Delete an existing record
  -u UPDATE_RECORD, --update UPDATE_RECORD
                        Perform a DNS update on an existing record.
  -U USER, --user USER  The username to connect to the dyn api. Can also be
                        set as DYN_USER in environment.
  -P PASSWORD, --password PASSWORD
                        The password to use with the dyn api. Can also be set
                        as DYN_PW in environment.
  -A ACCOUNT, --account ACCOUNT
                        The account name used to make API requests. Can be set
                        as DYN_ACCOUNT in environment.
  -Z ZONE, --zone ZONE  The zone to take action on. Eg example.com. Can be set
                        as DYN_ZONE in environment.
  -l, --list            List all dns records as a csv file.
  --verbose             Print out api responses.
```

Dyn is a nice DNS service. It's an alternative to Amazon's Route 53. Though I do not believe that dyn's API is as robust as amazone, with the right set of tools is just dandy.

This tool allows for the manipulation of DNS records via the restful API.

It currently supports the following:
* Create A and CNAME records
* Update A and CNAME records
* Delete A and CNAME records
* List all of the records as a CSV

### Requirements
The requests & argparse packages are required but not currently part of the standard library. Get them with pip: 
```
pip install -r requirements.txt
```

You can pass your username and password directly into the script, but it's better if you setup a few environment variables. dyncli will take advantage of the following environment variables if they are present:
```
DYN_USER
DYN_PW
DYN_ZONE
DYN_ACCOUNT
```

You can activate these by appending them to your ```~/.bash_profile```:
```
export DYN_USER='foo'
export DYN_PW='bar'
export DYN_ZONE='example.com'
export DYN_ACCOUNT='example'
```

### Creating a record
Right now both A and CNAME record creation is supported. Create a record uses the ```-c``` flag along with the optional ```--cname``` flag if that's your desired record type.

The default record type is an address (A) record.
```
# Create an A record with default TTL
$ ./dyncli -c myfqdn.example.net -v 10.0.0.100

# Create an A record with custom TTL
$ ./dyncli -c myfqdn.example.net -v 10.0.0.100 --ttl 3600

# Create a CNAME record
$ ./dyncli -c myfqdn.example.net -v otherfqdn.example.net --cname
```

### Updating a record
Once records are created, they can be easily updated with the ```-u``` or ```--update``` flag.

```
# Update the TTL of an existing record
$ ./dyncli -u myfqdn.example.net --ttl 3600

# Update the value of an existing cname record
$ ./dyncli -u myfqdn.example.net -v someotherfqdn.example.net
```

## Deleting a record
Records are deleted by passing the ```-d``` or ```--delete``` flag.
```
# Delete an address (A) record
$ ./dyncli -d myfqdn.example.net

# Delete a cname record (requires the --cname flag)
$ ./dyncli -d myfqdn.example.net --cname
```

### List all records (csv format)
Sometimes it's useful to list all of the records. We use this to do a simple nightly backup of our DNS zone.

The output format is a simple CSV file. Beware that if you have commas in your TXT record, they'll be translated to a pipe (```|```).
```
$ ./dyncli --list
zone,ttl,fqdn,record_type,data
example.net,300,test.example.net,CNAME,test2.example.net
example.net,300,foo.example.net,A,172,16.0.100
example.net,3600,example.net,TXT,public_key=sdjflksdj
..
```

Sometimes it's also useful to check if a zone exists before you go creating one willy nilly
```
$ ./dyncli --list | grep database
example.net,300,database.example.net,A,172.16.0.100
example.net,300,database.internal.example.net,A,172.16.0.100
example.net,300,database.something.example.net,A,172.16.0.100

(See what happens when you go on creating records without checking first?)
```

If you notice any bugs please open an issue.
