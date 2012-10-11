import anyjson

class LicenseFinder:
  def load_requirements(self, *options, **kwargs):
    return (open(kwargs['file'], 'r').read())

  def parse(self, str):
    return str.split('\n')

if __name__ == "__main__":
  pass
