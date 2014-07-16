#!/usr/bin/env python
import json
import requests

class Dynapi:

  def __init__(self,user,pw,account,zone):
    self.user = user
    self.pw = pw
    self.account = account
    self.zone = zone
    self.token = None
    self.endpoint = 'https://api2.dynect.net/REST/'
    
  def call_dyn(self,suffix,method='get',data=None):
    '''
    Helper function to make api calls. Requires the suffix for the url
    (everything after https://api2.dynect.net/REST/*), and optionally a method
    (get, delete, put, or post). Data is also optional for put and post.
    '''

    url = self.endpoint + suffix

    if method == 'get':
      url = url + '?detail=y'
  
    header = {
      'content-type': 'application/json',
      'Accept': 'application/json'
    }
  
    if self.token:
      header['Auth-Token'] = self.token
  
    try:
      resp = json.loads(getattr(requests,method)(url,headers=header,data=data))
    except Exception, e:
      raise
  
    if resp['status'] != 'success':
      raise Exception(resp['msgs'][0]['INFO'])

    return resp
  
  def initialize(self):
    '''
    Make a call to dyn and get our session token.
    '''

    suffix = 'Session/'
    data = {
      'customer_name': self.account,
      'user_name': self.user,
      'password': self.pw
    }
  
    resp = self.call_dyn(suffix,method='post',data=data)
    self.token = resp['data']['token']

    return resp
  
  def create_record(self,address,value,type,ttl):
    '''
    Create an address record. Requires an address, value, and TTL.
    '''
    if type == 'cname':
      suffix = 'CNAMERecord/%s/%s/' % (self.zone, address)
    elif type == 'address':
      suffix = 'ARecord/%s/%s/' % (self.zone, address)
    else:
      raise Exception('Only supported types are cname and A records')

    payload = {
      'rdata': {
        type: value
      },
      'ttl': ttl
    }

    resp = self.call_dyn(suffix,method='post',data=payload)
    return resp

  def update_address(self,address,type,value=None,ttl=None):
    '''
    Update and existing record. Requires an address, value, and type (address,
    or cname). Because the endpoints are different you need to specify the
    type.
    '''
    if type == 'address':
      suffix = "ARecord/%s/%s/" % (self.zone,address)
    elif type == 'cname':
      suffix = "CNAMERecord/%s/%s/" % (self.zone,address)

    payload = {
      'rdata': {}
    }

    if value:
      payload['rdata'] = {
        type: value 
      }
    if 'ttl':
      payload['ttl'] = ttl
  
    resp = self.call_dyn(suffix,method='put',data=payload)

    if resp['msgs'][0]['INFO'] == 'id: You did not reference a specific record':
      raise Exception('Unable to update record.')

    return resp
  
  def delete_record(self,address,type):
    '''
    Delete a record. Requires address and type (address or cname).
    '''
    if type == 'address':
      suffix = 'ARecord/%s/%s/' % (self.zone, address)
    elif type == 'cname':
      suffix = 'CNAMERecord/%s/%s/' % (self.zone, address)
    else:
      raise Exception("Unknown type declared: %s" % type)

    resp = self.call_dyn(suffix,method='delete')
  
    if resp['msgs'][0]['INFO'] == 'delete: 0 records deleted':
        raise Exception('No records deleted. Check spelling and record type')

    return resp

  def publish(self):
    '''
    Publish changes we've made to dyn. No going back from here.
    '''
    suffix = "Zone/%s/" % self.zone

    data = {
      'publish': 1
    }
  
    resp = self.call_dyn(suffix,method='put',data=data)
    return resp

  def end_session(self):
    '''
    Though not strictly necessary it's good to end the session so the token can
    no longer be used.
    '''
    suffix = 'Session/'
  
    resp = self.call_dyn(suffix,method='delete')
    return resp
