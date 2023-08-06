# PyTls
<p align="center">
<img alt="PyPI" src="https://img.shields.io/pypi/v/PyTls.svg"></a>
<a href="https://travis-ci.org/sladesha/PyTls"><img src="https://travis-ci.org/sladesha/PyTls.svg?branch=master"></a>
<img alt="PyPI - License" src="https://img.shields.io/pypi/l/PyTls.svg"></a>
</p>

- 使用手册请参考：[Python自用工具包PyTls手册](http://www.shataowei.com/2019/10/22/Python自用工具包PyTls/)
- 各自的测试用例参考：[demos](demos.py#L6)
- 更新方式：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  --upgrade PyTls`

**目录：**
+ __init__.py
+ dictt.py
    + [get_map_value()](PyTls/dictt.py#L12)
    字典迭代取值
    + [update_map_value()](PyTls/dictt.py#L34)
    + [sort_map_key()](PyTls/dictt.py#L60)
    + [sort_map_value()](PyTls/dictt.py#L64)
    字典排序
    + [get_tree()](PyTls/dictt.py#L65)
    树结构
    + [swap()](PyTls/dictt.py#L71)
    kv交换
    + [merge()](PyTls/dictt.py#L76)
    合并两个dict
    + [func_dict()](PyTls/dictt.py#L93)
    对func生成一个字典，比如func：2n，ret = func_dict(func)，ret[2]会生成2*2，且ret存储一个2:4的键对
    + [WordCount()](PyTls/dictt.py#L104)
    字典树，快速查询和高效存储，支持string和list/tuple；支持计数、查找、位置校验三个核心功能
    + [json_loads()](PyTls/dictt.py#L158)
    安全加载json，解决json里面的"和'混用的问题
+ StrBuffer.py
参考java中的StringButter
    + [append()](PyTls/StrBuffer.py#L22)
    + [index_at()](PyTls/StrBuffer.py#L37)
    + [sort()](PyTls/StrBuffer.py#L47)
    + [reverse()](PyTls/StrBuffer.py#L50)
    + [char_at()](PyTls/StrBuffer.py#L53)
    + [to_str()](PyTls/StrBuffer.py#L58)
    + [storge()](PyTls/StrBuffer.py#L64)
+ strt.py
    + [str_reverse()](PyTls/strt.py#L14)
    + [str_repeat()](PyTls/strt.py#L18)
    + [str_splits()](PyTls/strt.py#L29)
    字符串批切割
    + [judge_anagrams()](PyTls/strt.py#L46)
    判断目标文本中是否有近似的待查找文本
+ typet.py
    + [is_none()](PyTls/typet.py#L11)
    + [is_type()](PyTls/typet.py#L15)
    + [is_empty()](PyTls/typet.py#L25)
    + [is_has_attr()](PyTls/typet.py#L35)
+ loaddatat.py
    + [readbunchobj()](PyTls/loaddatat.py#L13)
    + [writebunchobj()](PyTls/loaddatat.py#L19)
    读存数据
+ randomt.py
    + [get_random()](PyTls/randomt.py#L32)
+ Chinese2num.py
数字相关，提取数字更加强大的功能建议参考[YMMNlpUtils](https://github.com/sladesha/machine_learning/blob/master/YMMNlpUtils/YMMNlpUtils/YMMNlpUtils.py)
    + [Chinese_2_num()](PyTls/Chinese2num.py#L20)
    + [isdigit()](PyTls/Chinese2num.py#L33)
+ matht.py
    + [entropy()](PyTls/matht.py#L14)
    + [condition_entropy()](PyTls/matht.py#L33)
    条件熵，求和 H（X|Y）= Σ p(Y=yi)*H（X|Y=yi)
    + [MI()](PyTls/matht.py#L60)
    来自于条件概率计算法：H(x)-H(x/y)
    + [NMI()](PyTls/matht.py#L66)
    来自于公式计算：2`*`∑pxylog(pxy/(px`*`py))/(H(x)+H(y))
    + [ln()](PyTls/matht.py#L93)
    + [word_edit_distince()](PyTls/matht.py#L98)
    比较两个字符串的文本编辑距离
    + [BM25()](PyTls/matht.py#L114)
    BM25算法，计算相似度匹配
    + [relative_entropy()](PyTls/matht.py#L183)
    相对熵，也叫KL散度，H(p||q) = ∑pxl`*`og(px/py),如果px与py分布一致，则return 0，差异越大return的值越大;H(p||q) = H(p,q) - H(p)
    + [cross_entropy()](PyTls/matht.py#L198)
    交叉熵，H(p,q) = -∑pi*log(qi) , H(p||q) = H(p,q) - H(p)
    + [JSD()](PyTls/matht.py#L213)
    衡量两个多项分布的距离，衡量两个多项分布的相似度
    + [Hellinger_Distince()](PyTls/matht.py#L230)
    海林格距离，用来衡量概率分布之间的相似性
    + [isOdds()](PyTls/matht.py#L243)
+ listt.py    
    + [index_hash_map()](PyTls/listt.py#L10)
    list元素出现位置，等同于numpy array中的`np.where`
    + [Pi()](PyTls/listt.py#L26)
    + [single_one()](PyTls/listt.py#L38)
    从list找出非两两成对的单样本
    + [subset()](PyTls/listt.py#L44)
    子集
    + [permute()](PyTls/listt.py#L56)
    全排列
    + [flatten()](PyTls/listt.py#L70)
    高维列表展开
    + [duplicates()](PyTls/listt.py#L85)
    原序去重
    + [topn()](PyTls/listt.py#L95)
    高频统计
    + [getindex()](PyTls/listt.py#L109)
    返回list中最大/最小元素的位置
    + [split()](PyTls/listt.py#L125)
    list按照指定个数切分，比如split([1,2,3,4],3)-->[(1,2,3)]
    + [unzip()](PyTls/listt.py#L135)
    把zip后的数据还原
    + [ContactList()](PyTls/listt.py#L139)
    通过类继承的形式完善list类，提供search方法
+ trickt.py
    + [choose_method()](PyTls/trickt.py#L10) 
    条件选择函数，根据参数不同逻辑不同，进行不同函数运算
    + [Timer()](PyTls/trickt.py#L17)
    计时器
+ textt.py
    + [is_chinese()](PyTls/textt.py#L11) 
    判断一个unicode是否是汉字
    + [is_chinese_string()](PyTls/textt.py#L21)
    判断是否全为汉字
    + [is_number()](PyTls/textt.py#L29)
    判断一个unicode是否是数字
    + [is_alphabet()](PyTls/textt.py#L39)
    判断一个unicode是否是英文字母
    + [is_alphabet_string()](PyTls/textt.py#L49)
    判断是否全为字母
    + [stringB2Q()](PyTls/textt.py#L57)
    半角转全角
    + [stringQ2B()](PyTls/textt.py#L71)
    把字符串全角转半角
    + [remove_punctuation()](PyTls/textt.py#L85)
    去除标点符号
    + [uniform()](PyTls/textt.py#L94)
    格式化字符串，完成全角转半角，大写转小写的工作
    + [get_homophones_by_char()](PyTls/textt.py#L102)
    根据汉字取同音字
    + [get_homophones_by_pinyin()](PyTls/textt.py#L117)
    根据拼音取同音字
    + [LocationTire()](PyTls/textt.py#L144)
    地址相似度检索
+ wrappert.py
    + [timespend()](PyTls/wrappert.py#L8) 
    函数耗时装饰器