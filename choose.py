from PIL import Image


def make_hash(im_name):
        img = Image.open(im_name)

        img2 = img.resize((10, 10))
        pixels = img2.load()
        img.close()

        all_pixes = get_grey(pixels)
        mid = sum(all_pixes) / 100

        return get_bits(mid, all_pixes)


def get_grey(pixels) -> list:
    all_pixs = []
    for i in range(10):
        for j in range(10):
            r, g, b = pixels[i, j]
            bw = (r + g + b) // 3
            pixels[i, j] = bw, bw, bw
            all_pixs.append(bw)
    return all_pixs


def get_bits(mid, all_pixes) -> str:
    bits = []
    for i in range(100):
        bits.append(str(int(all_pixes[i] > mid)))
    return ''.join(bits)


if __name__ == '__main__':
    hash1 = make_hash("image_1.jpg")
    hash2 = make_hash("image_2.jpg")
    cou = 0
    for i in range(100):
        if hash1[i] == hash2[i]:
            cou += 1
    print(str(cou) + '%')
