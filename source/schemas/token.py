from schemas.base import BaseSchema

# class RefreshToken(BaseSchema):
#     __tablename__ = "refresh_tokens"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
#     token = Column(String, unique=True, index=True, nullable=False)
#     expires_at = Column(DateTime, nullable=False)
#     user_agent = Column(String, nullable=True)

#     user = relationship("User", back_populates="refresh_tokens")


class TokenData(BaseSchema):
    user_id: str
    refresh_token: str | None = None
