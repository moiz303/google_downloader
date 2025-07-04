from PIL import Image


def make_hash(im_name):
        img = Image.open(im_name)

        img2 = img.resize((10000, 10000))
        pixels = img2.load()
        img.close()

        all_pixes = get_grey(pixels)
        mid = sum(all_pixes) / 1000000000

        return get_bits(mid, all_pixes)


def get_grey(pixels) -> list:
    all_pixs = []
    for i in range(10000):
        for j in range(10000):
            r, g, b = pixels[i, j]
            bw = (r + g + b) // 3
            pixels[i, j] = bw, bw, bw
            all_pixs.append(bw)
    return all_pixs


def get_bits(mid, all_pixes) -> str:
    bits = []
    for i in range(100000000):
        bits.append(str(int(all_pixes[i] > mid)))
    return ''.join(bits)


def percenting(im1: str, im2: str):
    hash1 = make_hash(im1)
    hash2 = make_hash(im2)
    cou = 0
    for i in range(100000000):
        if hash1[i] == hash2[i]:
            cou += 1
    return cou


if __name__ == '__main__':
    print(percenting("image_1.jpg", "image_3.jpg"),  '\n' +
          'Дубликаты' if percenting("image_1.jpg", "image_3.jpg") > 87 else '')
