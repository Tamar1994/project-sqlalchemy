from sqlalchemy.orm import (
    declarative_base,
    relationship,
    Session
)

from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    ForeignKey,
    create_engine,
    inspect,
    select,
    func
)

Base = declarative_base()



class Client(Base):
    __tablename__  = "db_client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    cpf = Column(String(12))
    address = Column(String(50))

    bankaccount = relationship(
        "BankAccount", back_populates="client"
    )

    def __repr__(self):
        return f"Client(id={self.id}, " \
               f"name={self.name}, " \
               f"cpf={self.cpf}, " \
               f"address={self.address})"


class BankAccount(Base):
    __tablename__ = "bank_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20))
    agencia = Column(String(10))
    saldo = Column(DECIMAL)
    id_client = Column(Integer, ForeignKey("db_client.id"), nullable=False)

    client = relationship(
        "Client", back_populates="bankaccount"
    )

    def __repr__(self):
        return f"BankAccount(id={self.id}, " \
               f"type={self.type}, " \
               f"agencia={self.agencia}, " \
               f"saldo={self.saldo}, " \
               f"id_cliente={self.id_client})"



engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

inspetor_engine = inspect(engine)

print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    adriano = Client(
        name="Adriano Tamar Rodrigues",
        cpf="55588855522",
        address="adriano.tamar@gmail.com",
        bankaccount=[BankAccount(
            type="Conta-corrente",
            agencia="1234",
            saldo=1000.00
        )]
    )

    rafael = Client(
        name="Rafael Geovani Ramos Pinto",
        cpf="55588899925",
        address="rafael.pinto@email.com",
        bankaccount=[BankAccount(
            type="Poupança",
            agencia="1234",
            saldo=300.00
        )]
    )

    session.add_all([adriano, rafael])

    session.commit()

print("\nRealizando Select no DB Cliente")
stmt = select(Client)

for user in session.scalars(stmt):
    print(user)

print("\nRealizando Select no DB BankAccount")
stmt = select(BankAccount)

for account in session.scalars(stmt):
    print(account)

print("\nRealizando Join das tabelas")
stmt_join = select(Client.name, Client.cpf, BankAccount.type, BankAccount.agencia, BankAccount.saldo).join_from(Client, BankAccount)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()

for result in results:
    print(result)