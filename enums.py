import enum


class EnumRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class EnumNotificationCategory(enum.Enum):
    FRIEND_REQUEST = "friend_request"
    FRIEND_ACCEPTED = "friend_accepted"
    BLOG_LIKE = "blog_like"
    BLOG_COMMENT = "blog_comment"
    BLOG_SHARE = "blog_share"
    BLOG_PUBLISH = "blog_publish"


class EnumStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
