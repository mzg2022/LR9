from sqlalchemy.orm import Session
from app.models import User, Transaction
from app.schemas import UserCreate, TransactionCreate
from app.auth import hash_password
from app.observers import BonusObserver

def create_user(db: Session, user: UserCreate):
    """Create a new user."""
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()

def create_transaction(db: Session, transaction_data: dict):
    """Create a new transaction and update sender's bonus level."""
    transaction = Transaction(**transaction_data)
    sender = db.query(User).filter(User.id == transaction.sender_id).first()
    if sender:
        sender.balance -= transaction.amount
        BonusObserver(sender).update_level()

    receiver = db.query(User).filter(User.id == transaction.receiver_id).first()
    if receiver:
        receiver.balance += transaction.amount

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_transactions_by_user(db: Session, user_id: int):
    """Get all transactions for a user."""
    return db.query(Transaction).filter(
        (Transaction.sender_id == user_id) | (Transaction.receiver_id == user_id)
    ).all()

