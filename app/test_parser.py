"""
测试HTTP请求解析器
"""
import sys
import io
from http_parser import HTTPRequestParser

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_parse_get_request():
    """测试解析GET请求"""
    raw_request = """GET /admin/inspection.Report/getInspectionData HTTP/1.1
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: no-cache
Connection: keep-alive
Host: localhost:8000
Origin: http://localhost:1818
Pragma: no-cache
Referer: http://localhost:1818/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0
ba-user-token: 2d7f3b9f-f256-4f1a-b338-ed4f2bc117c5
batoken: b3d35eae-e142-4f4f-b429-71d19f14aa77
sec-ch-ua: "Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
server: true
think-lang: zh-cn"""

    print("=" * 80)
    print("测试 GET 请求解析")
    print("=" * 80)

    result = HTTPRequestParser.parse(raw_request)

    print(f"解析结果: {'成功' if result['success'] else '失败'}")
    if not result['success']:
        print(f"错误: {result['error']}")
        return False

    print(f"方法: {result['method']}")
    print(f"路径: {result['path']}")
    print(f"URL: {result['url']}")
    print(f"协议: {result['protocol']}")
    print(f"请求头数量: {len(result['headers'])}")

    print("\n请求头:")
    for key, value in result['headers'].items():
        print(f"  {key}: {value}")

    print(f"\n请求体: {result['body'] if result['body'] else '(空)'}")

    assert result['method'] == 'GET'
    assert result['path'] == '/admin/inspection.Report/getInspectionData'
    assert 'localhost:8000' in result['url']
    assert 'Host' in result['headers']
    assert result['headers']['Host'] == 'localhost:8000'

    print("\n✓ GET 请求解析测试通过")
    return True


def test_parse_post_request():
    """测试解析POST请求"""
    raw_request = """POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer token123
User-Agent: TestClient/1.0

{"username": "test", "email": "test@example.com"}"""

    print("\n" + "=" * 80)
    print("测试 POST 请求解析")
    print("=" * 80)

    result = HTTPRequestParser.parse(raw_request)

    print(f"解析结果: {'成功' if result['success'] else '失败'}")
    if not result['success']:
        print(f"错误: {result['error']}")
        return False

    print(f"方法: {result['method']}")
    print(f"路径: {result['path']}")
    print(f"URL: {result['url']}")
    print(f"协议: {result['protocol']}")
    print(f"请求头数量: {len(result['headers'])}")

    print("\n请求头:")
    for key, value in result['headers'].items():
        print(f"  {key}: {value}")

    print(f"\n请求体:\n{result['body']}")

    assert result['method'] == 'POST'
    assert result['path'] == '/api/users'
    assert 'api.example.com' in result['url']
    assert result['headers']['Content-Type'] == 'application/json'
    assert '"username"' in result['body']

    print("\n✓ POST 请求解析测试通过")
    return True


def test_parse_https_request():
    """测试HTTPS请求解析"""
    raw_request = """GET /secure/data HTTP/1.1
Host: secure.example.com:443
Content-Type: application/json"""

    print("\n" + "=" * 80)
    print("测试 HTTPS 请求解析")
    print("=" * 80)

    result = HTTPRequestParser.parse(raw_request)

    print(f"解析结果: {'成功' if result['success'] else '失败'}")
    print(f"URL: {result['url']}")

    assert result['success']
    assert result['url'].startswith('https://')

    print("\n✓ HTTPS 请求解析测试通过")
    return True


def test_invalid_request():
    """测试无效请求"""
    raw_request = "Invalid Request"

    print("\n" + "=" * 80)
    print("测试无效请求")
    print("=" * 80)

    result = HTTPRequestParser.parse(raw_request)

    print(f"解析结果: {'成功' if result['success'] else '失败'}")
    if not result['success']:
        print(f"错误: {result['error']}")
    else:
        print(f"警告: 期望解析失败，但实际成功了")
        print(f"解析的方法: {result['method']}")

    # 即使解析成功，如果method为空也应该算失败
    if not result['method']:
        print("\n✓ 无效请求测试通过（方法为空）")
        return True

    # 或者解析结果标记为失败
    if not result['success']:
        print("\n✓ 无效请求测试通过")
        return True

    print("\n✗ 无效请求测试失败：应该解析失败但实际成功")
    return False


if __name__ == "__main__":
    print("\n开始测试 HTTP 请求解析器\n")

    tests = [
        test_parse_get_request,
        test_parse_post_request,
        test_parse_https_request,
        test_invalid_request
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n✗ 测试失败: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 80)

    if failed == 0:
        print("\n所有测试都通过了！")
    else:
        print(f"\n有 {failed} 个测试失败")
