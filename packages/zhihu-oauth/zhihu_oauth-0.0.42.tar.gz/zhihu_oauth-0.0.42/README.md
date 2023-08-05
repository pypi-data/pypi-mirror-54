# Zhihu-OAuth

[![author][badge-author]][my-zhihu] [![ci-dev][ci-dev-img]][ci-page] [![ci-master][ci-master-img]][ci-page] [![docs][badge-docs]][rtds-home] [![version][badge-version]][pypi] [![py-version][badge-py-version]][pypi] [![state][badge-state]][pypi] [![license][badge-license]][license]

## 近况

由于知乎给 Github 发了 [DMCA][zhihu-dmca] 要求删除 [zhihu-oauth 仓库][github-repo]，所以 Github 把仓库设置为不可公开访问了。所以目前我只能把最新版代码同步到我自己个人的 Git Server 上了。

虽然一直有用户和我反馈还在使用这个库，并且某些功能也确实可以继续正常使用，但由于本人已经不用知乎多年，所以这个库其实有两年多没更新过了。

这次移动到个人站点之后，由于本站点不对外开放注册，游客就没法使用 Issue 和 PR 功能，所以可以预见的未来估计也不会有什么更新了，这里基本只提供代码备份和下载功能。

由于以上原因，README 中的捐款渠道也已一并删除。

如果你有想交流的问题，请使用邮件，或者 [Twitter][my-twitter] 联系我。

—— 2019.10.19

## 简介

**同学们，由于知乎新的 API 验证 UA，0.0.14 之前的版本已经不可用了，请尽快升级到 0.0.14 以上版本。**

最近在尝试解析出知乎官方未开放的 OAuth2 接口，顺便提供优雅的使用方式，作为 [zhihu-py3][zhihu-py3-github] 项目的继任者。

恩，理论上来说会比 zhihu-py3 更加稳定，原因如下：

- 知乎 API 相比前端 HTML 来说肯定更加稳定和规范
- 这次的代码更加规范
- 网络请求统一放在基类中
- 属性解析统一放在装饰器中，各知乎类只用于声明有哪些属性可供使用
- 统一翻页逻辑，再也不用一个地方一个逻辑了
- 翻页时的自动重试机制（虽然不知道有没有用吧）

这一新库与 zhihu-py3 相比速度更快。有关速度对比的详细信息请点击[这里][speed-compare]。

**这个库是 Py2 和 Py3 通用的！** 但是 Py3 的优先级比 Py2 高，也就是说，我会优先保证在 Py3 下的稳定性和正确性。毕竟在我学的时候选了 Py3，所以对 2 与 3 的差异了解不是很清楚，Py2 只能尽力而为了，

后期的计划是这样的：

- 0.0.x 这个阶段是 alpha 期，主要做的是补齐功能的工作。基本上 TODO 里的功能都会在这个时期实现。其中 0.0.5 版本计划完成和 zhihu-py3 同样多的功能（**已完成**）。
- 0.1.x 这个阶段是 beta 期，主要做完善测试，修复 bug，提升性能，改善架构之类的工作吧。以上两个阶段变化很大，有可能出现不兼容老版本的更新。使用需要注意。
- 0.2.x 及以后就是 stable 期，只要 API 不变，基本上代码结构就不会变了，接口可能会增加但一定不会减。

由于现在使用的 CLIENT_ID 和 SECRET 的获取方法并不正当，所以请大家暂时不要大规模宣传，自己用用就好啦，Thanks。

等我什么时候觉得时机成熟（等知乎真•开放 OAuth 申请？），会去知乎专栏里宣传一波的。

## 最近更新

目前版本是 0.0.41，没更新的快更新一下，更新说明在[这里][changelog]。

0.0.41 版本修复了 Feed 流的一些问题，加上了 `Topic.activities` 接口。

0.0.40 版本增加了 Feed 首页信息流的支持。

## 使用

### 安装

```bash
pip install -U zhihu_oauth
```

如果安装遇到问题，请查看文档：[安装][rtds-install]

### 登录

请参见文档：[登录][rtds-login]

### 获取基础信息

代码：

```python
from zhihu_oauth import ZhihuClient

client = ZhihuClient()

client.load_token('token.pkl')

me = client.me()

print('name', me.name)
print('headline', me.headline)
print('description', me.description)

print('following topic count', me.following_topic_count)
print('following people count', me.following_count)
print('followers count', me.follower_count)

print('voteup count', me.voteup_count)
print('get thanks count', me.thanked_count)

print('answered question', me.answer_count)
print('question asked', me.question_count)
print('collection count', me.collection_count)
print('article count', me.articles_count)
print('following column count', me.following_column_count)
```

输出：

```text
name 7sDream
headline 二次元普通居民，不入流程序员，http://0v0.link
description 关注本AI的话，会自动给你发私信的哟！
following topic count 35
following people count 101
followers count 1294
voteup count 2493
get thanks count 760
answered question 258
question asked 18
collection count 9
article count 7
following column count 11
```

更多功能请参见文档：[使用方法][rtds-usage]

## 文档

完整的文档可以在[这里][rtds-home] 找到。我写的文档好吧，可详细了……有啥问题先去找文档。我写的那么累你们看都不看我好不服啊！

（貌似 ReadTheDocs 在伟大的国家访问速度有点慢，建议自备手段。）

## TODO

- [x] 保证对 Python 2 和 3 的兼容性
- [x] 用户私信支持
- [x] Live 支持
- [x] Pin（分享）支持
- [x] 搜索功能（还差电子书搜索）
- [x] 用户首页 Feed
- [ ] 知乎电子书
- [ ] 获取用户消息。新关注者，新评论，关注的回答有新问题
- [ ] Token check/refresh
- [ ] Setting
- [ ] 规范、完善的测试
- [ ] article.voters 文章点赞者，貌似 OAuth2 没有这个 API
- [ ] collection.followers 这个 API 不稳定，没法返回所有关注者

## 协助开发

### 通过代码

1. Fork
2. 从 dev 分支新建一个分支
3. 编写代码，更新 Changelog 和 sphinx 文档，如果可能的话加上测试
4. PR 到原 dev 分支

### 通过捐款

由于开发不积极，不再接受捐款。

[捐款记录][donate-record]

## LICENSE

MIT


[zhihu-py3-github]: https://github.com/7sDream/zhihu-py3
[speed-compare]: https://github.com/7sDream/zhihu-oauth/blob/master/compare.md
[changelog]: https://github.com/7sDream/zhihu-oauth/blob/master/changelog.md

[rtds-home]: http://zhihu-oauth.readthedocs.io/zh_CN/latest
[rtds-install]: http://zhihu-oauth.readthedocs.io/zh_CN/latest/guide/install.html
[rtds-login]: http://zhihu-oauth.readthedocs.io/zh_CN/latest/guide/login.html
[rtds-usage]: http://zhihu-oauth.readthedocs.io/zh_CN/latest/guide/use.html

[badge-author]: https://img.shields.io/badge/Author-7sDream-blue.svg
[badge-docs]: https://readthedocs.org/projects/zhihu-oauth/badge/?version=latest
[badge-version]: https://img.shields.io/pypi/v/zhihu_oauth.svg
[badge-py-version]: https://img.shields.io/pypi/pyversions/zhihu_oauth.svg
[badge-state]: https://img.shields.io/pypi/status/zhihu_oauth.svg
[badge-license]: https://img.shields.io/pypi/l/zhihu_oauth.svg

[my-zhihu]: https://www.zhihu.com/people/7sdream
[ci-page]: https://travis-ci.org/7sDream/zhihu-oauth
[ci-dev-img]: https://api.travis-ci.org/7sDream/zhihu-oauth.svg?branch=dev
[ci-master-img]: https://api.travis-ci.org/7sDream/zhihu-oauth.svg?branch=master
[pypi]: https://pypi.python.org/pypi/zhihu_oauth
[license]: https://github.com/7sDream/zhihu-oauth/blob/master/LICENSE

[donate-record]: https://github.com/7sDream/zhihu-oauth/blob/donate/donate.md

[my-twitter]: https://twitter.com/7sDream
[zhihu-dmca]: https://github.com/github/dmca/blob/master/2019/10/2019-10-17-Zhizhetianxia.md
[github-repo]: https://github.com/7sDream/zhihu-oauth