import os
import hashlib
import aioconsole
import uuid
import socket
import asyncio
import json

from kademlia.network import Server

# 현재 노드의 IP 주소 확인
def local_ip():
    return [local IP 주소('000.000.000.000')]

# 파일 업로드 함수
async def upload_file(file_path, server, node_id):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # 파일 메타데이터 생성
    metadata = {
        'name': file_name,
        'size': file_size,
        'blocks': []
    }

    block_size = 1024  # 블록 크기 (여기서는 1KB로 설정)
    # 파일을 열어서 1024 크기만큼 잘라서 blocks (블록 메타 데이터에 추가)
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(block_size)
            if not data:
                break

            # 블록에 대한 해시 값 계산
            block_hash = hashlib.sha256(data).hexdigest()

            # 블록을 Kademlia DHT의 키-값 저장소에 저장
            await server.set(block_hash, data)

            # 블록 메타데이터 추가
            metadata['blocks'].append(block_hash)
    # 파일 이름이 중복될 수도 있어서 hash 사용

    # 파일 메타데이터를 Kademlia DHT의 키-값 저장소에 저장
    # hashlib.sha256(file_name.encode()).hexdigest() 파일 이름을 해시하여 file_hash를 생성
    file_hash = hashlib.sha256(file_name.encode()).hexdigest()
    # metadata는 파일의 메타데이터를 담고 있는 딕셔너리
    # 파일 이름, 파일 크기, 블록 해시 값이 저장
    metadata_json = json.dumps(metadata)  # metadata를 JSON 형식으로 
    # server.set() file_hash가 키, metadata_json 이 값으로 Kademaila DHT의 키-값 저장소에 저장
    await server.set(file_hash, metadata_json)  # metadata_json 사용
    print(f"파일 업로드 완료: {file_name} ({file_size} bytes)")

# 파일 다운로드 함수
async def download_file_by_name(file_name, server, node_id):
    # 파일 이름이름을 해시해서 file_hash 생성하고, Kademlia DHT 에서 파일 메타데이터를 조회
    # file_name : 다운로드할 파일 이름
    file_hash = hashlib.sha256(file_name.encode()).hexdigest()
    # server.get() 주어진 키에 해당하는 값을 반환
    metadata_json = await server.get(file_hash)
    if not metadata_json:
        print("해당 파일이 존재하지 않습니다.")
        return

    metadata = json.loads(metadata_json)
    file_size = metadata['size']
    blocks = metadata['blocks']

    # 다운로드할 파일명 설정
    # 같은 이름으로 다운되면 헷갈려서 뒤에 _p2p를 붙였음
    download_file_name = (
        metadata['name'].rsplit('.', 1)[0]
        + "_p2p."
        + metadata['name'].rsplit('.', 1)[1]
        if '.' in metadata['name']
        else metadata['name'] + "_p2p"
    )

    # 다운로드할 파일 경로 
    # 현재 파이썬 파일이 실행되고 있는 현재 디렉토리랑 + 파일 이름(_p2p 붙었음)
    download_file_path = os.path.join(os.getcwd(), download_file_name)

    # 다운로드할 파일 생성
    with open(download_file_path, 'wb') as file:
        for block_hash in blocks:
            # 블록 데이터 조회
            block_data = await server.get(block_hash)
            if block_data:
                file.write(block_data)
            else:
                print(f"블록 다운로드 실패: {block_hash}")

    print(f"파일 다운로드 완료: {download_file_name} ({file_size} bytes)")


# 사용자 인터페이스 함수
async def user_interface(server, node_id):
    print("1. 파일 다운로드")
    print("2. 파일 업로드")
    print("3. 종료")
    # await aioconsole.ainput 비동기적으로 사용자에게 입력을 받음
    choice = await aioconsole.ainput("원하는 작업을 선택하세요: ")

    # 파일 업로드, 다운로드를 비동기로 실행
    if choice == "1":
        file_name = await aioconsole.ainput("다운로드할 파일의 이름을 입력하세요: ")
        await download_file_by_name(file_name, server, node_id)
    elif choice == "2":
        file_path = await aioconsole.ainput("업로드할 파일의 경로를 입력하세요: ")
        await upload_file(file_path, server, node_id)
    elif choice == "3":
        return False
    else:
        print("잘못된 선택입니다. 다시 시도해주세요.")
    return True

async def run():
    # Kademlia DHT에 참여하는 노드들 작성
    bootstrap_nodes = [
        ([다른 노드의 ip 주소], 0000),
        ([다른 노드의 ip 주소], [포트번호]),
        (local_ip(), [포트번호])
    ]

    # node_id : 현재 노드의 고유 식별자를 생성하고 할당
    node_id = uuid.uuid1()
    # server 객체 생성
    server = Server()
    #server.listen() Kademlia DHT 서버가 지정한 포트에서 연결할 수 있게 설멍
    await server.listen(8468)  # 원하는 포트 번호로 수정
    # 부트스트랩 노드에게 연결 시도, Kademlia DHT 네트워크에 접속
    await server.bootstrap(bootstrap_nodes)
    
    # 메뉴 계속 보여주기
    flag = True
    while flag:
        flag = await user_interface(server, node_id)
    
    server.stop()

# 메인 프로그램 실행
asyncio.run(run())