from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="author_id")
    posts: Mapped[List["Comment"]] = relationship(back_populates="author")

    follower: Mapped[List["Follower"]] = relationship(back_populates="user_from")
    following: Mapped[List["Follower"]] = relationship(back_populates="user_to")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author_id: Mapped["User"] = relationship(back_populates="posts")

    post_id: Mapped[List["Comment"]] = relationship(back_populates="post_user")
    post_id: Mapped[List["Media"]] = relationship(back_populates="post_user")

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post_user: Mapped["Post"] = relationship(back_populates="post_id")

class Media_type_enum(enum.Enum):
    POST = "Post"
    REEL = "Reel"
    STORY = "Story"


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(Enum(Media_type_enum), default=Media_type_enum.POST)
    url: Mapped[str] = mapped_column(db.Text, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    
    post_user: Mapped["Post"] = relationship(back_populates="post_id")


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user_from: Mapped["User"] = relationship(back_populates="follower")
    user_to: Mapped["User"] = relationship(back_populates="following")