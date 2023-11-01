from api.datastore.datastore import data_store


class TransactionManager:
    def __init__(self):
        self.stack = []
        self.current_transaction = {}
        self.initiator = None

    def begin(self):
        self.stack.append(self.current_transaction.copy())

    def rollback(self):
        if not self.stack:
            raise ValueError("Нет активных транзакций")
        self.current_transaction = self.stack.pop()

    def commit(self):
        if not self.stack:
            raise ValueError("Нет активных транзакций")
        data_store.data.update(self.current_transaction)
        data_store.save_data_to_file()
        self.stack = []


transaction_manager = TransactionManager()
