from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exception import (
    general_exception_handler,
    http_exception_handler,
    integrity_error_handler,
    sqlalchemy_error_handler,
)


def register_exception_handlers(app):
    """
    注册全局异常处理器: 子类在前，父类在后，确保子类异常被优先处理
    :param app: FastAPI应用实例
    """
    app.add_exception_handler(HTTPException, http_exception_handler)    # HTTP异常
    app.add_exception_handler(IntegrityError, integrity_error_handler)  # 完整性异常
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)    # SQLAlchemy异常
    app.add_exception_handler(Exception, general_exception_handler)     # 未捕获的异常
