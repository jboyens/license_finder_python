import anyjson
import requests
import os

class LicenseFinder:
  def __init__(self, *options, **kwargs):
    self.api_client = kwargs['api_client'] or requests

  def load_requirements(self, *options, **kwargs):
    file = open(kwargs['file'], 'r')
    self.requirements = [x.rstrip(os.linesep).strip() for x in file if x]

  def load_data(self):
    self.req_data = {}
    for requirement in self.requirements:
      self.req_data[requirement] = self.request_data(requirement)

  def request_data(self, dep):
    return requests.get("http://pypi.python.org/pypi/{0}/json".format(dep)).json

  def license_from_dict(self, dict):
    info = dict.get('info', {})

    if info.get('license', 'UNKNOWN') in ['UNKNOWN']:
      return [x for x in info.get('classifiers', []) if x.startswith("License")]
    else:
      return [info['license']]

if __name__ == "__main__":
  pass
