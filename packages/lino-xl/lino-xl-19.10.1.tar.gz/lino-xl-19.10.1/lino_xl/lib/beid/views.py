# -*- coding: UTF-8 -*-
# Copyright 2018 Rumma 6 Ko Ltd
# License: BSD (see file COPYING for details)

"""Views for `lino.modlib.bootstrap3`.

"""
from __future__ import division

from os.path import join
import time
import json
# from django import http
# from django.conf import settings
from django.views.generic import View
# from django.core import exceptions
from lino.utils import AttrDict
from lino.core.views import json_response
from lino.api import dd, _


def read_card_data_from_file(fn):
    fp = open(fn)
    rv = json.load(fp)
    fp.close()
    # dd.logger.info("20181002 json.load({}) returned {}".format(
    #     fn, rv))

    if 'success' not in rv:
        raise Warning(
            _("Got invalid card data {} from eidreader.").format(rv))

    data = AttrDict(rv)
    # quick hack to fix #2393. a better solution would be to
    # make eidreader not POST every key-value using requests
    # but to send a single field card_data which would be a
    # json encoded dict.
    # if isinstance(data.success, six.string_types):
    #     data.success = parse_boolean(data.success.lower())
    if not data.success:
        raise Warning(_("No card data found: {}").format(
            data.message))
    return data


def load_card_data(uuid):
    # raise Exception("20180412 {}".format(uuid))
    fn = dd.plugins.beid.data_cache_dir.child(uuid)
    timeout = dd.plugins.beid.eidreader_timeout
    count = 0
    while True:
        try:
            return read_card_data_from_file(fn)
        except IOError as e:
            dd.logger.info("20181002 I/O error reading %s : %s", fn, e)
            time.sleep(1)
            count += 1
            if count > timeout:
                raise Warning(_("Abandoned after {} seconds").format(
                    timeout))
                # rv = dict(success=False)
                # break
            # continue


class EidStore(View):
    # def get(self, request, uuid, **kw):
    #     print("20180412 GET {} {}".format(uuid, request.GET))
    #     return json_response()

    def post(self, request, uuid, **kw):
        # uuid = request.POST.get('uuid')
        card_data = request.POST.get('card_data')
        # card_data = json.loads(card_data)

        # msg = "20180412 raw data {}".format(request.body)
        # dd.logger.info(msg)

        # if not card_data:
        #     raise Exception("No card_data found in {}".format(
        #         request.POST))
        fn = dd.plugins.beid.data_cache_dir.child(uuid)
        # pth = dd.plugins.beid.data_cache_dir
        # pth = join(pth, uuid)
        try:
            fp = open(fn, 'w')
            fp.write(card_data)
            # json.dump(card_data, fp)
            fp.close()
            # msg = "20181002 wrote {} : {}".format(fn, card_data)
            # dd.logger.info(msg)
            return json_response(dict(success=True, message="OK"))
        except IOError as e:
            dd.logger.warning(
                "Failed to store data to file %s : %s", fn, e)
            return json_response(
                dict(success=False, message=str(e)),
                status=502)
        # username = request.POST.get('username')
        # return http.HttpResponseRedirect(target)
