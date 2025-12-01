"""
测试cURL命令解析器
"""
import sys
import io

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from http_parser import HTTPRequestParser, parse_curl_command


def test_parse_curl_get_request():
    """测试解析cURL GET请求"""
    curl_command = 'curl https://api.example.com/users'

    print("=" * 80)
    print("测试 cURL GET 请求解析")
    print("=" * 80)

    result = HTTPRequestParser.parse_curl_command(curl_command)

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
    assert result['url'] == 'https://api.example.com/users'

    print("\n✓ cURL GET 请求解析测试通过")
    return True


def test_parse_curl_post_request():
    """测试解析cURL POST请求"""
    curl_command = 'curl -X POST -H "Content-Type: application/json" -d \'{"name":"John","email":"john@example.com"}\' https://api.example.com/users'

    print("\n" + "=" * 80)
    print("测试 cURL POST 请求解析")
    print("=" * 80)

    result = HTTPRequestParser.parse_curl_command(curl_command)

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
    assert result['url'] == 'https://api.example.com/users'
    assert result['headers']['Content-Type'] == 'application/json'
    assert 'name' in result['body']

    print("\n✓ cURL POST 请求解析测试通过")
    return True


def test_parse_curl_with_headers():
    """测试解析带请求头的cURL请求"""
    curl_command = 'curl -H "Authorization: Bearer token123" -H "Accept: application/json" https://api.example.com/users'

    print("\n" + "=" * 80)
    print("测试带请求头的 cURL 请求解析")
    print("=" * 80)

    result = HTTPRequestParser.parse_curl_command(curl_command)

    print(f"解析结果: {'成功' if result['success'] else '失败'}")
    if not result['success']:
        print(f"错误: {result['error']}")
        return False

    print(f"方法: {result['method']}")
    print(f"URL: {result['url']}")
    print(f"请求头数量: {len(result['headers'])}")

    print("\n请求头:")
    for key, value in result['headers'].items():
        print(f"  {key}: {value}")

    assert result['method'] == 'GET'
    assert result['url'] == 'https://api.example.com/users'
    assert result['headers']['Authorization'] == 'Bearer token123'
    assert result['headers']['Accept'] == 'application/json'

    print("\n✓ 带请求头的 cURL 请求解析测试通过")
    return True


def test_parse_curl_form_data():
    """测试解析表单数据的cURL请求"""
    curl_command = 'curl -X POST -F "username=john" -F "email=john@example.com" https://api.example.com/login'

    print("\n" + "=" * 80)
    print("测试表单数据 cURL 请求解析")
    print("=" * 80)

    result = HTTPRequestParser.parse_curl_command(curl_command)

    print(f"解析结果: {'成功' if result['success'] else '失败'}")
    if not result['success']:
        print(f"错误: {result['error']}")
        return False

    print(f"方法: {result['method']}")
    print(f"URL: {result['url']}")
    print(f"请求头数量: {len(result['headers'])}")

    print("\n请求头:")
    for key, value in result['headers'].items():
        print(f"  {key}: {value}")

    print(f"\n请求体:\n{result['body']}")

    assert result['method'] == 'POST'
    assert result['url'] == 'https://api.example.com/login'
    assert 'username' in result['body']
    assert 'email' in result['body']

    print("\n✓ 表单数据 cURL 请求解析测试通过")
    return True


def test_invalid_curl():
    """测试无效的cURL命令"""
    curl_command = 'invalid command'

    print("\n" + "=" * 80)
    print("测试无效cURL命令")
    print("=" * 80)

    result = HTTPRequestParser.parse_curl_command(curl_command)

    print(f"解析结果: {'成功' if result['success'] else '失败'}")
    if not result['success']:
        print(f"错误: {result['error']}")

    # 无效命令应该解析失败
    if not result['success']:
        print("\n✓ 无效cURL命令测试通过")
        return True
    else:
        print("\n✗ 无效cURL命令测试失败：应该解析失败但实际成功")
        return False


def test_format_form_data():
    """测试表单数据格式化"""
    form_data = "name=John%20Doe&email=john%40example.com&age=25"

    print("\n" + "=" * 80)
    print("测试表单数据格式化")
    print("=" * 80)

    result = HTTPRequestParser.format_form_data(form_data)

    print(f"原始数据: {form_data}")
    print("\n格式化结果:")
    for key, value in result.items():
        print(f"  {key}: {value}")

    assert result['name'] == 'John Doe'
    assert result['email'] == 'john@example.com'
    assert result['age'] == '25'

    print("\n✓ 表单数据格式化测试通过")
    return True


def test_format_query_string():
    """测试查询字符串格式化"""
    query_string = "search=python&page=2&limit=10"

    print("\n" + "=" * 80)
    print("测试查询字符串格式化")
    print("=" * 80)

    result = HTTPRequestParser.format_query_string(query_string)

    print(f"原始查询字符串: {query_string}")
    print("\n格式化结果:")
    for key, value in result.items():
        print(f"  {key}: {value}")

    assert result['search'] == 'python'
    assert result['page'] == '2'
    assert result['limit'] == '10'

    print("\n✓ 查询字符串格式化测试通过")
    return True


if __name__ == "__main__":
    print("\n开始测试 cURL 命令解析器\n")

    tests = [
        test_parse_curl_get_request,
        test_parse_curl_post_request,
        test_parse_curl_with_headers,
        test_parse_curl_form_data,
        test_invalid_curl,
        test_format_form_data,
        test_format_query_string
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