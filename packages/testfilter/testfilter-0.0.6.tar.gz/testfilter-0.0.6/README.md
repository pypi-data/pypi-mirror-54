# testfilter
unittest 用例执行过滤， 可选择用例级别或用例级别进行过滤

### 如何使用它?

```shell
>>> pip install testfilter
```


```python

import unittest
from testfilter import runIf, Filter

# 设置执行环境 执行级别
Filter.env = 'test'  # test uat prod/production 不区分大小写
Filter.level = 'p2'  # smoke/p1 p2 p3 p4 不区分大小写


class Demo(unittest.TestCase, metaclass=Filter.Meta):
    @runIf.env.NOT_PROD  # 非正式环境下执行
    def test_001(self):
        self.assertEqual(1, 1)

    @runIf.env.TEST  # 仅在测试环境下执行
    def test_002(self):
        self.assertEqual(1, 1)

    @runIf.env.UAT
    @runIf.env.TEST
    @runIf.level_in.P3   # 测试环境和 UAT 环境下，且用例优先级在 P3 以上执行
    def test_003(self):
        self.assertEqual(1, 1)

    @runIf.level_in.SMOKE
    def test_004(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':

    unittest.main()

```
![image](http://mocobk.test.upcdn.net/image/2019-04-14-112321.jpg)

### 用例环境

| Tag |  英文 | 中文 |
|:----|:------|:-----|
|TEST|Testing|测试|
|UAT|User Acceptance Test|用户验收测试|
|PROD|Production|正式/生产|


### 用例级别
**Level:** 

|SMOKE/P0|P1|P2|P3|P4|
|----|----|----|----|-----|

### [用例级别参考](https://www.jianshu.com/p/4903856cd6c5)

P0/SMOKE 冒烟：

    1、挑一些基本的、带有针对性、关键的用例进行测试，不会很细
    2、划分依据：主流程或者必须实现的功能测试
    3、该级别的测试用例在每一轮版本测试前执行

P1/Level1 基本：

    1、该类用例设计系统基本功能，1级用例的数量应受到控制
    2、划分依据：该用例执行的失败会导致多处重要功能无法运行的，如：表单维护中的增加功能、最平常的业务使用等。可以认为是发生概率较高的而经常这样使用的一些功能用例。
    3、该级别的测试用例在每一轮版本测试中都必须执行

P2/Level2 重要：

    1、2级测试用例实际系统的重要功能。2级用例数量较多。
    2、划分依据：主要包括一些功能交互相关、个种应用场景、使用频率较高的正常功能测试用例
    3、在非回归的系统测试版本中基本上都需要进行验证，以保证系统所有的重要功能都能够正常实现。在测试过程中可以根据版本当前的具体情况进行安排是够进行测试。

P3/Level3 一般：

    1、3级测试用例设计系统的一半功能，3级用例数量也较多。
    2、划分依据：使用频率较低于2级用例。例如：数值或数组的便捷情况、特殊字符、字符串超长、与外部件交互消息失败、消息超时、事物完整性测试、可靠性测试等等。
    3、在非回归的系统测试版本中不一定都进行验证，而且在系统测试的中后期并不一定需要每个版本都进行测试
    
P4/Level4 生僻：如果没有可以不适用该级别

    1、该级别用例一半非常少。
    2、划分依据：该用例对应较生僻的预置条件和数据设置。虽然某些测试用例发现过较严重的错误，但是那些用例的处罚条件非常特殊，仍然应该被植入4级用例中。如界面规范化的测试也可归入4级用例。在实际使用中使用频率非常低、对用户可有可无的功能。
    3、在版本测试中有某些正常原因（包括：环境、人力、时间等）经过测试经理同意可以不进行测试。


