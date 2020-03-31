import argparse
import falcon
from hyperparams import Hyperparams as hp
import os
from synth import Synthesizer


html_body = ''' '''


class UIResource:
  def on_get(self, req, res):
    res.content_type = 'text/html'
    with open("app.html", 'r') as f:
            res.body = f.read()
    #res.body = html_body


class SynthesisResource:
  def on_get(self, req, res):
    if not req.params.get('text'):
      raise falcon.HTTPBadRequest()
    res.data = synth.synthesize(req.params.get('text'))
    res.content_type = 'audio/wav'


synth = Synthesizer()
api = falcon.API()
api.add_route('/synthesize', SynthesisResource())
api.add_route('/', UIResource())


if __name__ == '__main__':
  from wsgiref import simple_server

  synth.load()
  print("\n *****************************************************************************************************")
  print('\nNamaskaram,\n Visit : http://127.0.0.1:5000/ from your browser (Chrome/Firefox).\nPranam,\nYou Know Who!')
  simple_server.make_server('0.0.0.0', 5000, api).serve_forever()


