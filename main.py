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
        document_ids = [d.id for d in documents]
        if len(document_ids) >= self.get_document_count():
            self.set_message("No progress was made, not re-running")
            print("No progress was made, not re-running")
            return

        self.client.post(
            "addon_runs/",
            json={
                "addon": self.addon_id,
                "parameters": self.data,
                "documents": document_ids,
            },
        )

    def get_documents(self):
        """Get documents from either selected or queried documents"""

        if self.documents:
            documents = self.client.documents.list(id__in=self.documents)
        elif self.query:
            documents = self.client.documents.search(self.query)

        # turn documents into an iterator, so that documents that get yielded are
        # consumed and not re-used when we rerun
        documents = iter(documents)
        for document in documents:
            yield document
            if self.soft_timeout():
                self.rerun_addon(documents)
                print("soft time out")
                self.set_message(
                    "Soft time out, continuing rest of documents in a new run"
                )
                break

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
