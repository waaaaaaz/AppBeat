# AppBeat

app智能遍历工具，支持安卓和IOS双端


## 需求
- 自动触发app, 配合其他移动端测试工具完成专项测试
- 尽量简化配置, 减少维护成本
- 遍历规则更贴合业务场景(业务逻辑不同, 通用性需求平衡)
- 方便二次开发, 统一技术栈, 后期移动端测试平台的重要组成


## 参考
- https://github.com/seveniruby/AppCrawler
- https://github.com/lgxqf/UICrawler


## 安装

- 安装安卓开发环境
- 安装IOS开发环境及wda
- 安装appium开发环境
- 目前只支持mac下运行

## 执行模式

- BFS: 
  - 整个app所有页面组成树的数据结构
  - 每个页面(参考安卓activity)作为树的节点
  - 自动获取节点可点击元素及相对坐标
  - 每个页面可能包含多个dom，支持上滑
  - 广度遍历整个app
  
- DFS: 
  - 如上
  - 深度遍历整个app
  
- Monkey: 
  - 参考adb monkey
  - 基于appium模拟monkey动作, 动作可扩展
  - 支持安卓和IOS双端
  - 动作随机比例可配置
  - 所有点击操作(点击, 双击, 长按)只点可点击元素
 
- Target: 
  - 通过配置xpath，只遍历目标页面
  - 广度遍历目标页面
  
- 执行及参数

```bash
#查看帮助文档
python run.py --help
#运行
python run.py -T android -U 123uads -M target -F ./AppBeat/config/android_config.yml
```

- 配置文件：
  - 参考 [example_config.yml](config/example_config.yml)  内附说明
  
- 其他功能：
  - 记录所有执行步骤及结果, 异步缓存在本地
  - 所有点击生成截图, 截图标记出点击位置
  - 执行完成后生成视频
  - 可按时间和动作次数配置执行
  - crash后记录, 自动重启
  - 执行记录上报, 性能搜集等功能需要配合其他工具
  
- License
  - MIT
  

