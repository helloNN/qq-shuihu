from .futureBase import Base


class Test(Base):
    def test_write(self, coord, content):
        """
        测试输入框输入内容
        :param coord: 普通坐标
        :param content 输入的内容
        """
        self.util.type_content(coord, content)

    def test_log(self):
        self.logger.info(self.qq)
