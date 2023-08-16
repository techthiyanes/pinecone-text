import pytest
from pinecone_text.dense.openai_encoder import OpenAIEncoder

DEFAULT_DIMENSION = 1536


class TestOpenAIEncoder:
    def setup_method(self):
        self.corpus = [
            "The quick brown fox jumps over the lazy dog",
            "The lazy dog is brown",
            "The fox is brown",
            "The fox is quick",
            "The fox is brown and quick",
            "The fox is brown and lazy",
            "The fox is brown and quick and lazy",
            "The fox is brown and quick and lazy and jumps",
            "The fox is brown and quick and lazy and jumps and over",
        ]
        self.encoder = OpenAIEncoder()

    @staticmethod
    def mocked_embedding_create(input, model):
        return {"data": [{"embedding": [0.1] * DEFAULT_DIMENSION}] * len(input)}

    @pytest.fixture(autouse=True)
    def mock_openai_embedding(self, monkeypatch):
        monkeypatch.setattr("openai.Embedding.create", self.mocked_embedding_create)

    def test_encode_documents(self):
        encoded_docs = self.encoder.encode_documents(self.corpus)
        assert len(encoded_docs) == len(self.corpus)
        assert len(encoded_docs[0]) == DEFAULT_DIMENSION

    def test_encode_single_document(self):
        endoced_doc = self.encoder.encode_documents(self.corpus[0])
        assert len(endoced_doc) == DEFAULT_DIMENSION

    def test_encode_single_document_list(self):
        endoced_docs = self.encoder.encode_documents([self.corpus[0]])
        assert len(endoced_docs) == 1
        assert len(endoced_docs[0]) == DEFAULT_DIMENSION

    def test_encode_queries(self):
        encoded_queries = self.encoder.encode_queries(self.corpus)
        assert len(encoded_queries[0]) == DEFAULT_DIMENSION

    def test_encode_single_query(self):
        encoded_query = self.encoder.encode_queries(self.corpus[0])
        assert len(encoded_query) == DEFAULT_DIMENSION

    def test_encode_single_queries_list(self):
        encoded_queries = self.encoder.encode_queries([self.corpus[0]])
        assert len(encoded_queries) == 1
        assert len(encoded_queries[0]) == DEFAULT_DIMENSION
