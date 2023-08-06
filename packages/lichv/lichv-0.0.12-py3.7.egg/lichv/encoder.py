#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

if __name__ == "__main__":
    pass