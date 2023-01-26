"""
Test soft time out patterns
"""

import time

from documentcloud.addon import SoftTimeOutAddOn


class TestTimeout(SoftTimeOutAddOn):
    """An example Add-On for DocumentCloud."""

    soft_time_limit = 10

    def main(self):
        """The main add-on functionality goes here."""
        self.set_message(f"Processing {self.get_document_count()} documents...")
        print(f"Processing {self.get_document_count()} documents...")
        for document in self.get_documents():
            self.set_message(f"Processing document {document.title}...")
            print(f"Processing document {document.title}...")
            time.sleep(5)


if __name__ == "__main__":
    TestTimeout().main()
