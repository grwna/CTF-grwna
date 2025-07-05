def destroy():
    data = open("stage_play.pdf", "rb").read()
    intact = data[:16]
    result = intact + data[16:][::-1]
    open("stage-play.pdf", "wb").write(result)

def build():
    data = open("stage-play.pdf", "rb").read()
    intact = data[:16]
    result = intact + data[16:][::-1]
    open("chall.pdf", "wb").write(result)

build()
