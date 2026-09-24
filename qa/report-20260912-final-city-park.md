# 《雨后的天空》城市公园改造验收报告

- 验收地址：`http://127.0.0.1:8060/index.html`
- 验收日期：2026-09-12
- 方式：Playwright Chromium 黑盒操作 + 页面运行时契约检查 + 截图复核
- 总结：**12 项通过，0 项失败**

| 编号 | 结果 | 验收说明与证据 |
|---|---|---|
| BRIDGE-01 | PASS | 桥从河近岸跨到对岸，桥面中间抬高，桥下保留净空；三名行人持续沿桥面高度行走。证据：`qa/shots/city-park-bridge.png`，运行时坐标均高于桥面。 |
| NAV-01 | PASS | 所有河边儿童持续为 `play`，不再触发游泳、蹚水、落水或招手等状态；室外人物到河中心线最小距离 6.57，大于水面半径 5.5。 |
| FISH-01 | PASS | 14 条锦鲤/小鱼沿河曲线游动、转向并摆尾；实测高度 0.07～0.17，低于河面高度 0.28。 |
| SHOP-01 | PASS | 后排 6 间建筑分别为室内游乐场、餐厅、衣服店、化妆品店、超市、玩具店；自动化逐间点击，结果为 `[True, True, True, True, True, True]`。 |
| SHOP-02 | PASS | 六店均有老板、顾客和对应商品；衣服店顾客会换衣服颜色。证据：`city-park-clothes-shop.png`、`city-park-supermarket.png`、`city-park-indoor-play.png`。 |
| GROUND-01 | PASS | 大地图恢复草坪底色，只在游乐场、摊位和商业街使用边界明确的水泥广场，不再出现重复大水泥地。 |
| ROAD-01 | PASS | 弯曲长道路位于商业建筑后方，五种颜色车辆按曲线路径行驶，不穿过房屋。证据：`city-park-traffic.png`。 |
| MOUNTAIN-01 | PASS | 远山改为不规则陡峭山体并使用岩草纹理；石块数量和尺寸受控，10 名登山者沿绳索攀爬。证据：`city-park-mountain.png`。 |
| WEATHER-01 | PASS | 下雨后室外人物打伞，以 4.2 的慢速向桥和建筑移动；登山者沿绳索下撤，游乐设施上的儿童停止室外活动。证据：`city-park-rain-routes.png`。 |
| STALL-01 | PASS | 共 5 个尺寸放大的小摊，包含食品、饮料和玩具，每摊有老板与多件商品。证据：`city-park-stalls.png`。 |
| PLAY-01 | PASS | 滑梯儿童沿滑道下降，秋千儿童坐着摆动，跷跷板两端各坐一人，健身器材有固定使用者，不再原地乱跳。证据：`city-park-playground.png`。 |
| STABILITY-01 | PASS | 页面只有一个 WebGL 画布，完整验收过程中无 console error、page error 或崩溃。 |

## 重点运行结果

```text
canvas: 1
shop count: 6
all shop clicks entered: [True, True, True, True, True, True]
river states: ['play', 'play', 'play', 'play', 'play', 'play', 'play', 'play']
min outdoor river distance: 6.57
fish depths: [0.15, 0.08, 0.08, 0.10, 0.15, 0.16, 0.17, 0.11, 0.16, 0.16, 0.09, 0.10, 0.10, 0.09]
errors: none
```

## 截图目录

全部验收截图保存在 `qa/shots/`。
