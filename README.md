# Deepface-Server
Deepface+yolo的flask服务端封装，默认端口1234。

node_client.js是测试客户端

请求使用POST方法，body中用raw格式，详细见node_client.js。

返回数据格式：
```json
{
  "instance_1": {
    "dominant_race": "white",
    "race": {
      "asian": 1.6358125067241494,
      "black": 22.144736179395686,
      "indian": 3.734629823841442,
      "latino hispanic": 7.368712566418204,
      "middle eastern": 10.927203948927161,
      "white": 54.18891037636461
    },
    "region": { "h": 194, "w": 120, "x": 540, "y": 251 }
  },
  "instance_2": {
    "dominant_race": "white",
    "race": {
      "asian": 1.6358125067241494,
      "black": 22.144736179395686,
      "indian": 3.734629823841442,
      "latino hispanic": 7.368712566418204,
      "middle eastern": 10.927203948927161,
      "white": 54.18891037636461
    },
    "region": { "h": 194, "w": 120, "x": 540, "y": 251 }
  },
  "seconds": 4.223340034484863,
  "trx_id": "85de636d-bdfc-4d62-a4d1-bfddb0d6c308"
}
```

依赖:
```bash
pip install deepface==0.0.75

cd client
npm install node-fetch
```

服务器启动：
```bash
python Deepface.py
```

客户端运行：
```bash
node node_client.js
```
