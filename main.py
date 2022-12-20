"""
Test soft time out patterns
"""

import time

from documentcloud.addon import AddOn

ADDON_ID = 242


class TestTimeout(AddOn):
    """An example Add-On for DocumentCloud."""

    soft_time_limit = 10
    addon_id = ADDON_ID

    def __init__(self):
        super().__init__()
        self._start = time.time()
        self._document_generator = None

    def rerun_addon(self, documents):
        """Re-run the add on with the same parameters with the remaining documents"""
        self.client.post(
            "addon_runs/",
            json={
                "addon": self.addon_id,
                "parameters": self.data,
                "documents": [d.id for d in documents],
            },
        )

    def get_documents(self):
        """Get documents from either selected or queried documents"""

        if self.documents:
            documents = self.client.documents.list(id__in=self.documents)
        elif self.query:
            documents = self.client.documents.search(self.query)

        for document in documents:
            if self.soft_timeout():
                self.rerun_addon(documents)
                self.set_message(
                    "Soft time out, continuing rest of documents in a new run"
                )
                break
            yield document

    def soft_timeout(self):
        return time.time() - self._start > self.soft_time_limit

    def main(self):
        """The main add-on functionality goes here."""
        print(f"Processing {self.get_document_count()} documents...")
        for document in self.get_documents():
            print(f"Processing document {document.title}...")
            self.set_message(f"processing document {document.title}...")
            time.sleep(5)


if __name__ == "__main__":
    TestTimeout().main()
