# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 18:47:08 2012

@author: avsh
"""

import vkontakte as api
import re

__urlIsVMediaRe = re.compile("""^(photo|video|audio|doc)\\d+_\\d+$""")
__urlToVMediaRe = re.compile("""((?:photo|video|audio|doc)\\d+_\\d+)""")


def urlIsVMedia(url):
    return __urlIsVMediaRe.match(url) and True or False


def urlToVMedia(url):
    results = __urlToVMediaRe.finditer(url)
    try:
        result = next(results)
        return result.groups()[0]
    except StopIteration:
        raise RuntimeError('wrong url: %s' % url)


class Consumer(object):
    def __init__(self, apiId=None, apiSecret=None, token=None, owner=None):
        self.owner = owner

        # try to default to the given token
        self.token = token
        if self.token == None:
            self.api = api.API(apiId, apiSecret)
            self.token = self.api.token
        else:
            self.api = api.API(token=token)
            self.token = token

    def consume(self, post, attachment=None, **kwargs):
        args = {'message': post}
        if self.owner != None:
            args['owner_id'] = self.owner
            # if id is negative, it's a group, post on its behalf
            if self.owner[0] == '-':
                args['from_group'] = 1
        if 'attachments' in kwargs and type(kwargs['attachments']) == str and\
                                            kwargs['attachments']  != '':
            # convert from \n separator to ',' and ensure that urls are in
            # correct format
            args['attachments'] = ",".join(
                map(lambda u: urlToVMedia(u),
                    kwargs['attachments'].split('\n')))

        # post with retrieved params
        reply = self.api.wall.post(**args)

        if type(reply) == dict and 'post_id' in reply and\
           reply['post_id'] != None:
            return reply['post_id']
        else:
            raise RuntimeError('wrong reply from VK, message: %s, reply: %s' %\
                (post, str(reply)))