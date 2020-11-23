# -*- coding: utf-8 -*-
import hashlib

#算法描述：使用6个字符来表示短链接，我们使用ASCII字符中的'a'-'z','0'-'5'，共计32个字符做为集合。每个字符有32种状态，六个字符就可以表示32^6（1073741824），那么如何得到这六个字符，描述如下：
#对传入的长URL进行Md5，得到一个32位的字符串，这个字符串变化很多，是16的32次方，基本上可以保证唯一性。将这32位分成四份，每一份8个字符，这时机率变成了16的8次方，是4294967296，这个数字碰撞的机率也比较小啦，关键是后面的一次处理。我们将这个8位的字符认为是16进制整数，然后取0-30位，每5个一组，算出他的整数值，然后映射到我们准备的32个字符中，最后就能够得到一个6位的短链接地址。

def __original_shorturl(url):

  base32 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
       'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
       'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
       'y', 'z','0', '1', '2', '3', '4', '5'
  ]
  m = hashlib.md5()
  m.update(url)
  hexStr = m.hexdigest()
  hexStrLen = len(hexStr)
  subHexLen = hexStrLen / 8
  output = []
  for i in range(0,subHexLen):
    subHex = '0x'+hexStr[i*8:(i+1)*8]
    res = 0x3FFFFFFF & int(subHex,16)
    out = ''
    for j in range(6):
      val = 0x0000001F & res
      out += (base32[val])
      res = res >> 5
    output.append(out)
  return output

print __original_shorturl('https://tb666.top/dingwei.html')