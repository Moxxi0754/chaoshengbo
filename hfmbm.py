import heapq
import wave
import numpy as np

letter_freq = {
    'e': 0.12702,
    't': 0.09056,
    'a': 0.08167,
    'o': 0.07507,
    'i': 0.06966,
    'n': 0.06749,
    's': 0.06327,
    'h': 0.06094,
    'r': 0.05987,
    'd': 0.04253,
    'l': 0.04025,
    'c': 0.02782,
    'u': 0.02758,
    'm': 0.02406,
    'w': 0.0236,
    'f': 0.02228,
    'g': 0.02015,
    'y': 0.01974,
    'p': 0.01929,
    'b': 0.01492,
    'v': 0.00978,
    'k': 0.00772,
    'j': 0.00153,
    'x': 0.0015,
    'q': 0.00095,
    'z': 0.00074,
}

# 将字母按照出现频率进行排序
letter_freq = {k: v for k, v in sorted(letter_freq.items(), key=lambda item: item[1], reverse=True)}


def huffman_decode(encoded_sentence, huffman_dict):
    """
    将给定的哈夫曼编码 encoded_sentence 进行译码，并返回原英文字符串
    """
    inv_huffman_dict = {v: k for k, v in huffman_dict.items()}
    decoded_sentence = ""
    i = 0
    while i < len(encoded_sentence):
        for j in range(i + 1, len(encoded_sentence) + 1):
            if encoded_sentence[i:j] in inv_huffman_dict:
                decoded_sentence += inv_huffman_dict[encoded_sentence[i:j]]
                i = j
                break
        else:
            raise ValueError(f"未找到编码 {encoded_sentence[i:j]} 的对应字符")
    print(decoded_sentence)


def huffman_encode(symbols):
    """
    将给定的符号列表 symbols 进行哈夫曼编码，并返回编码字典和编码后的比特串
    """
    heap = [[weight, [symbol, ""]] for symbol, weight in symbols.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        low = heapq.heappop(heap)
        high = heapq.heappop(heap)
        for pair in low[1:]:
            pair[1] = '0' + pair[1]
        for pair in high[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])
    huffman_dict = dict(heapq.heappop(heap)[1:])
    return huffman_dict


def encode_sentence():
    # 英文字母及其在英文语料库中的出现频率

    # 进行哈夫曼编码
    huffman_dict = huffman_encode(letter_freq)
    sentence = input("请输入一句英文：")
    print("录音中……")
    print("录音完成")
    print("开始译码")
    encoded_sentence = ''
    for char in sentence:
        if char in huffman_dict:
            encoded_sentence += huffman_dict[char]
        elif char == ' ':
            encoded_sentence += ' '
        else:
            raise ValueError(f"字符 {char} 不在编码字典中")
    return encoded_sentence


if __name__ == '__main__':
    encoded_sentence = encode_sentence()
    print('哈夫曼编码：', encoded_sentence)
    print("译码结果为：")
    huffman_decode(encoded_sentence, huffman_dict=huffman_encode(letter_freq))
