from api.datastore.datastore import data_store


class TransactionManager:
    def __init__(self):
        self.transaction_stack = []
        self.current_transaction = {}
        self.transaction_initiator = None

    def begin_transaction(self):
        self.transaction_stack.append(self.current_transaction.copy())

    def rollback_transaction(self):
        if not self.transaction_stack:
            raise ValueError("Нет активных транзакций")
        self.current_transaction = self.transaction_stack.pop()

    def commit_transaction(self):
        if not self.transaction_stack:
            raise ValueError("Нет активных транзакций")
        data_store.data.update(self.current_transaction)
        data_store.save_data_to_file()
        self.transaction_stack = []


transaction_manager = TransactionManager()
