# coding: spec

from license_finder import LicenseFinder

from mock import MagicMock, call
import requests

describe LicenseFinder:
  describe "reading the requirements":
    before_each:
      self.requirements_fixture = "test/fixtures/requirements.txt"

      requests.get = MagicMock()

      self.license_finder = LicenseFinder(api_client=requests)
      self.file = self.license_finder.load_requirements(file=self.requirements_fixture)

    it "loads the file":
      self.license_finder.requirements.should.equal(["Django", "Fabric"])

    it "creates a datastructure":
      self.license_finder.requirements[0].should.equal("Django")
      self.license_finder.requirements[1].should.equal("Fabric")

    it "makes a request for the JSON data for a package":
      requests.get.side_effect = lambda x: MagicMock(json="{}")

      self.license_finder.request_data(self.license_finder.requirements[0]).should.equal("{}")

      requests.get.assert_called_with('http://pypi.python.org/pypi/Django/json')

    it "makes a request for all the requirements":
      self.license_finder.load_data()

      self.license_finder.req_data['Django'].should_not.be.none
      self.license_finder.req_data['Fabric'].should_not.be.none

      requests.get.call_args_list == [call('http://pypi.python.org/pypi/Django/json'), call('http://pypi.python.org/pypi/Fabric/json')]

    describe "license_from_dict":
      it "pulls license data out of the dict":
        license = self.license_finder.license_from_dict({"info": {"classifiers": ["Intended Audience :: Developers", "License :: OSI Approved :: BSD License"]}})
        license.should.equal(["License :: OSI Approved :: BSD License"])

      it "ignores unknown top-level licenses":
        license = self.license_finder.license_from_dict({"info": {"license":"UNKNOWN", "classifiers": ["Intended Audience :: Developers", "License :: OSI Approved :: BSD License"]}})
        license.should.equal(["License :: OSI Approved :: BSD License"])

      it "handles missing data gracefully":
        license = self.license_finder.license_from_dict({})
        license.should.equal([])

      it "pulls top-level license data":
        license = self.license_finder.license_from_dict({"info": {"license":"BSD"}})
        license.should.equal(["BSD"])
