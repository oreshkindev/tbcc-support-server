import sqlalchemy

metadata = sqlalchemy.MetaData()

ticket_table = sqlalchemy.Table(
    "tickets",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(100)),
    sqlalchemy.Column("last_name", sqlalchemy.String(100)),
    sqlalchemy.Column("username", sqlalchemy.String(100)),
    sqlalchemy.Column("from_id", sqlalchemy.Integer()),
    sqlalchemy.Column("to_id", sqlalchemy.Integer()),
    sqlalchemy.Column("content", sqlalchemy.Text()),
    sqlalchemy.Column("status", sqlalchemy.Integer()),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime()),
)
