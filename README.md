<img src="https://capsule-render.vercel.app/api?type=egg&color=ffffe0&height=200&section=header&text=chanhyestars&fontSize=70&fontcolor=ffd700" />

# 💾 Kademlia DHT를 이용한 P2P 파일 공유 시스템

* [Requirements](#requirements)
* [How to use](#how-to-use)
* [Demos](#Demos)
* [Release](#Release)

**P2P 네트워크**란, 중앙 집중화된 서버 없이 Peer나 Node 간 직접 통신을 통하여 데이터를 공유, 분산하는 시스템입니다. 해당 프로젝트에서는 [**Kademlia**](https://en.wikipedia.org/wiki/Kademlia)를 사용하였는데, 이는 P2P 컴퓨터 네트워크를 위해, DHT(Distributed Hash Tables)를 구축하는 프로토콜입니다.


## Requirements
코드는 Python 3.7 version 기반으로 작성되었으며, 필요한 패키지의 정보는 requirments.txt 파일에서 확인과 사용이 가능합니다.

```bash
# requirements.txt에 입력되어 있는 패키지 설치
pip install -r requirements.txt
```


## How to use
### 0. node ip 주소 설정

**def save_ip():** 에서 return 값을 python 코드를 실행하는 서버의 ip 주소를 입력합니다.

<img width="327" alt="KakaoTalk_Photo_2023-06-14-15-46-02" src="https://github.com/chanj99/p2p-KademliaDHT/assets/82193352/71352598-0ff5-4a43-9b61-f95f9bec4a6d">

**async def run():** 부분에서 kademlia DHT에 참여할 주소와 포트 번호를 입력합니다. 

<img width="259" alt="KakaoTalk_Photo_2023-06-14-15-45-52" src="https://github.com/chanj99/p2p-KademliaDHT/assets/82193352/f3fb9828-f64d-4166-8713-8f5862b0ca23">


### 1. 실행 방법
```bash
# python 파일을 실행
python p2p_node_v1.py
```
### 2. 사용 방법
1을 입력하면 파일을 다운로드
2를 입력하면 파일을 업로드
3을 입력하면 프로그램 종료

* 파일 다운로드
- 파일의 경로와 함께 파일이름을 입력
- 실행파일과 같은 디렉토리에 있는 파일은 파일이름만 입력

* 파일 업로드
- DHT에 저장되어 있는 파일 명을 입력하면 파일 다운로드 실행됨


## Demos
해당 데모는 client가 3개인 경우입니다.
각 client들은, "client + [client 번호].txt" 파일을 가지고 있습니다.
자신의 파일을 업로드하고, 다른 client들의 파일을 다운받습니다.

#### client1 🖥️
<img src="https://github.com/chanj99/p2p-KademliaDHT/assets/82193352/41689808-b21b-4e8d-8641-dceca2a4e028" width = "60%" height = "60%">


#### client2 🖥️
<img src="https://github.com/chanj99/p2p-KademliaDHT/assets/82193352/64101953-ea0f-4621-8d5a-35bcf569827b" width = "60%" height = "60%">


#### client3 🖥️
<img src="https://github.com/chanj99/p2p-KademliaDHT/assets/82193352/bda02879-3c8b-4d45-8552-8f5d8d292913" width = "60%" height = "60%">


## Release
* v0.0.1
  * p2p 네트워크 연결을 통하여 파일 업로드, 다운로드 가능


