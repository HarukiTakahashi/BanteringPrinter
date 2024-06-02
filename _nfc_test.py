# とりあえずNFCリーダーで教員証が読み込めるかどうかをチェック
# あとで学生証も借りてやってみる
import nfc


def on_connect(tag: nfc.tag.Tag) -> bool:
    print(tag.dump())

    try:
        if tag != None:
            print("connected")
            tag.dump()

            print("==========")

            #print(dir(tag))
            servc = 0x1A8B
            service_code = [nfc.tag.tt3.ServiceCode(servc >> 6, servc & 0x3F)]
            bc_id = [nfc.tag.tt3.BlockCode(0)]
            bd_id = tag.read_without_encryption(service_code,bc_id)
            # print(bd_id)
            print(bd_id.decode("utf-8")[2:-2])
    except:
        print("Error")
        pass

    return True  # Trueを返しておくとタグが存在しなくなるまで待機され、離すとon_releaseが発火する


def on_release(tag: nfc.tag.Tag) -> None:
    print("released")


with nfc.ContactlessFrontend("usb") as clf:
    while True:
        clf.connect(rdwr={"on-connect": on_connect, "on-release": on_release})
