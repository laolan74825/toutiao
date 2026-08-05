from models.database import Base  # 先导入基类
from models.favorite import Favorite  # 最后导入引用了别人的表
from models.news import News  # 先导入被引用的基础表
from models.users import User, UserToken  # 先导入被引用的基础表
