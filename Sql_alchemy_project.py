from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///users.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    university = Column(String)

    def __repr__(self):
        return f"[{self.id}] {self.name}, {self.age} years old, studies at {self.university}"


Base.metadata.create_all(engine)

# Append user
def add_user():
    name = str(input("Name: "))
    age = int(input("Age: "))
    uni = str(input("University: "))

    user = User(name=name, age=age, university=uni)

    session.add(user)
    session.commit()
    print("✅ Added:", user)

def show_users():
    users = session.query(User).all()
    if not users:
        print("No users found.")
    for user in users:
        print(user)

def remove_user():
    user_id = input("Enter user ID to remove: ")
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print("✅ Removed:", user)
    else:
        print("❌ User not found")


def find_user_by_name():
    name = input("Enter name to search: ")
    users = session.query(User).filter_by(name=name).all()
    if not users:
        print("❌ No users found")
    else:
        for u in users:
            print(u)

def edit_user():
    user_id = input("Enter ID to edit: ")
    user = session.query(User).filter_by(id=user_id).first()

    if not user:
        print("❌ User not found")
        return

    new_name = input(f"New name (leave blank to keep '{user.name}'): ")
    new_age = input(f"New age (leave blank to keep '{user.age}'): ")
    new_uni = input(f"New university (leave blank to keep '{user.university}'): ")

    if new_name:
        user.name = new_name
    if new_age.isdigit():
        user.age = int(new_age)
    if new_uni:
        user.university = new_uni

    session.commit()
    print("✅ Updated:", user)


def main_menu():
    while True:
        print("\n📋 MENU")
        print("[1] Show all users")
        print("[2] Add user")
        print("[3] Remove user by ID")
        print("[4] Find users by name")
        print("[5] Edit user by ID")
        print("[0] Exit")

        choice = input("Choose option: ")

        if choice == "1":
            show_users()
        elif choice == "2":
            add_user()
        elif choice == "3":
            remove_user()
        elif choice == "4":
            find_user_by_name()
        elif choice == "5":
            edit_user()
        elif choice == "0":
            print("👋 Exiting...")
            break
        else:
            print("❗ Invalid option")

main_menu()

