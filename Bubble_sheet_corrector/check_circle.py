def count_good_pixels(image, a, b, th = 180):
    cnt = 0
    for y in range(a-25, a+26):
        for x in range(b-25, b+26):
            if image[x, y] < th: cnt+=255-image[x, y]
    return cnt