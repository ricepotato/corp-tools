from dataclasses import dataclass
import os
import logging
import tempfile
import requests
import zipfile
from xml.etree.ElementTree import parse

from compapi import Company


log = logging.getLogger(f"app.{__name__}")


CHUNK_SIZE = 1024 * 1024


class DartAPI:
    def __init__(self):
        self.API_KEY = os.environ.get(
            "DART_API_KEY", "dba4950446e850591874436d32861606430db875"
        )

    def get_corp_code(self):
        if os.path.exists("CORPCODE.xml"):
            return self._parse_corp_file("CORPCODE.xml")

        with tempfile.TemporaryDirectory() as dir:
            corp_zip = self._download_corp_xml(dir)
            corp_xml = self._unzip_corp(corp_zip, dir)
            return self._parse_corp_file(corp_xml)

    def _download_corp_xml(self, dir):
        params = {"crtfc_key": self.API_KEY}
        r = requests.get("https://opendart.fss.or.kr/api/corpCode.xml", params=params)
        r.raise_for_status()

        filepath = os.path.join(dir, "corpcode.zip")
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(CHUNK_SIZE):
                f.write(chunk)
        return filepath

    def _unzip_corp(self, corp_file, dir):
        with zipfile.ZipFile(corp_file) as f:
            f.extractall(dir)
            return os.path.join(dir, "CORPCODE.xml")

    def _parse_corp_file(self, corp_xml_file):
        tree = parse(corp_xml_file)
        root = tree.getroot()
        corp_list = root.findall("list")

        return [
            Company(
                code=corp.findtext("corp_code").strip(),
                name=corp.findtext("corp_name").strip(),
                stock_code=corp.findtext("stock_code").strip(),
                modify_date=corp.findtext("modify_date").strip(),
                reports=[],
            )
            for corp in corp_list
        ]
