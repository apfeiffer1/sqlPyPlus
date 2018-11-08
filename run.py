#!/usr/bin/env python

from app import app

app.run(debug=True, port=5000, host='::1')
