# coding: spec

from license_finder import LicenseFinder

describe LicenseFinder:
  describe "reading the requirements.txt":
    before_each:
      self.requirements_fixture = "test/fixtures/requirements.txt"

      self.license_finder = LicenseFinder()
      self.file = self.license_finder.load_requirements(file=self.requirements_fixture)
      self.data = self.license_finder.parse(self.file)

    it "loads the file":
      self.file.should.equal(open(self.requirements_fixture, 'r').read())

    it "creates a datastructure":
      self.data[0].should.equal("django")
      self.data[1].should.equal("fabric")

    it "makes a request for the JSON data for a package":
      django_data = self.license_finder.request_data(self.data[0])
