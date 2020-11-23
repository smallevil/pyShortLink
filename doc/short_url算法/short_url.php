<?php
/**
 * 算法描述：使用6个字符来表示短链接，我们使用ASCII字符中的'a'-'z','0'-'5'，共计32个字符做为集合。每个字符有32种状态，六个字符就可以表示32^6（1073741824），那么如何得到这六个字符，描述如下：
 * 对传入的长URL进行Md5，得到一个32位的字符串，这个字符串变化很多，是16的32次方，基本上可以保证唯一性。将这32位分成四份，每一份8个字符，这时机率变成了16的8次方，是4294967296，这个数字碰撞的机率也比较小啦，关键是后面的一次处理。我们将这个8位的字符认为是16进制整数，然后取0-30位，每5个一组，算出他的整数值，然后映射到我们准备的32个字符中，最后就能够得到一个6位的短链接地址。
 */
function ShortUrl($input, $length=6) {

                $base32 = array (

                        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',

                        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',

                        'q', 'r', 's', 't', 'u', 'v', 'w', 'x',

                        'y', 'z', '0', '1', '2', '3', '4', '5'

                );



                $hex = md5($input);

                $hexLen = strlen($hex);

                $subHexLen = $hexLen / 8;   // 划分为4段，保留4组结果

                $resultArray = array();



                for ($i = 0; $i < $subHexLen; $i++) {

                    $subHex = '0x' . substr($hex, $i * 8, 8);         // 分成4段，每段取8位字符
                    $int = 0x3FFFFFFF & hexdec($subHex);       // 8位字节与16进制取与操作
                    $out = '';



                    for ($j = 0; $j < $length; $j++) {

                        $val = 0x0000001F & $int;   // 取0~31之间的整数

                        $out .= $base32[$val];      // 从数组中获取对应字符

                        $int = $int >> (30/$length);

                    }



                    $resultArray[] = $out;

                }



                return $resultArray;

            }

$url = ShortUrl('https://tb666.top/dingwei.html');
print_r($url);

$url = ShortUrl('https://xxuuoo.net/');
print_r($url);
?>