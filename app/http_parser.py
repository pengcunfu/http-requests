"""
HTTP请求解析器
解析原始HTTP请求文本，提取方法、URL、请求头和请求体
"""
import re
import json
import urllib.parse
from typing import Dict, Tuple, Optional, List


class HTTPRequestParser:
    """HTTP请求解析器"""

    @staticmethod
    def parse(raw_request: str) -> Dict[str, any]:
        """
        解析原始HTTP请求文本

        Args:
            raw_request: 原始HTTP请求文本

        Returns:
            包含解析结果的字典:
            {
                'method': str,      # 请求方法 (GET, POST, etc.)
                'path': str,        # 请求路径
                'url': str,         # 完整URL
                'protocol': str,    # HTTP协议版本
                'headers': dict,    # 请求头字典
                'body': str,        # 请求体
                'success': bool,    # 是否解析成功
                'error': str        # 错误信息（如果有）
            }
        """
        result = {
            'method': '',
            'path': '',
            'url': '',
            'protocol': 'HTTP/1.1',
            'headers': {},
            'body': '',
            'success': False,
            'error': ''
        }

        try:
            # 分离请求头和请求体
            parts = raw_request.split('\n\n', 1)
            if len(parts) == 0:
                parts = raw_request.split('\r\n\r\n', 1)

            header_section = parts[0]
            body_section = parts[1] if len(parts) > 1 else ''

            # 按行分割请求头部分
            lines = header_section.strip().split('\n')
            if not lines:
                result['error'] = '请求文本为空'
                return result

            # 解析请求行 (第一行)
            request_line = lines[0].strip()
            method, path, protocol = HTTPRequestParser._parse_request_line(request_line)

            if not method:
                result['error'] = '无法解析请求行'
                return result

            result['method'] = method
            result['path'] = path
            result['protocol'] = protocol

            # 解析请求头
            headers = {}
            host = ''

            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue

                # 解析 Key: Value 格式
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    headers[key] = value

                    # 提取Host用于构建完整URL
                    if key.lower() == 'host':
                        host = value

            result['headers'] = headers

            # 构建完整URL
            if host:
                # 判断协议 (http/https)
                scheme = 'https' if ':443' in host or 'https' in host.lower() else 'http'
                result['url'] = f"{scheme}://{host}{path}"
            else:
                result['url'] = path

            # 解析请求体
            result['body'] = body_section.strip()

            result['success'] = True

        except Exception as e:
            result['error'] = f'解析失败: {str(e)}'
            result['success'] = False

        return result

    @staticmethod
    def _parse_request_line(line: str) -> Tuple[str, str, str]:
        """
        解析HTTP请求行

        Args:
            line: 请求行文本 (例如: "GET /api/data HTTP/1.1")

        Returns:
            (method, path, protocol) 元组
        """
        parts = line.strip().split()

        if len(parts) < 2:
            return '', '', ''

        method = parts[0].upper()
        path = parts[1]
        protocol = parts[2] if len(parts) > 2 else 'HTTP/1.1'

        # 验证HTTP方法
        valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE']
        if method not in valid_methods:
            return '', '', ''

        return method, path, protocol

    @staticmethod
    def format_headers_for_table(headers: Dict[str, str]) -> list:
        """
        将请求头字典格式化为表格数据

        Args:
            headers: 请求头字典

        Returns:
            列表，每项为 (enabled, key, value) 元组
        """
        return [(True, key, value) for key, value in headers.items()]

    @staticmethod
    def validate_request(raw_request: str) -> Tuple[bool, str]:
        """
        验证HTTP请求文本是否有效

        Args:
            raw_request: 原始HTTP请求文本

        Returns:
            (is_valid, error_message) 元组
        """
        if not raw_request or not raw_request.strip():
            return False, '请求文本为空'

        lines = raw_request.strip().split('\n')
        if len(lines) < 1:
            return False, '请求格式不正确'

        # 验证请求行格式
        request_line = lines[0].strip()
        parts = request_line.split()

        if len(parts) < 2:
            return False, '请求行格式不正确，应为: METHOD PATH [PROTOCOL]'

        # 验证HTTP方法
        valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE']
        method = parts[0].upper()

        if method not in valid_methods:
            return False, f'不支持的HTTP方法: {method}'

        return True, ''

    @staticmethod
    def parse_curl_command(curl_command: str) -> Dict[str, any]:
        """
        解析cURL命令，转换为HTTP请求格式

        Args:
            curl_command: cURL命令字符串

        Returns:
            包含解析结果的字典，格式与parse方法相同
        """
        result = {
            'method': 'GET',
            'path': '',
            'url': '',
            'protocol': 'HTTP/1.1',
            'headers': {},
            'body': '',
            'success': False,
            'error': ''
        }

        try:
            import shlex
            args = shlex.split(curl_command)

            url = ''
            method = 'GET'
            headers = {}
            data = ''

            i = 0
            while i < len(args):
                arg = args[i]

                if arg == 'curl':
                    # 下一个参数是URL（除非是其他选项）
                    if i + 1 < len(args) and not args[i + 1].startswith('-'):
                        url = args[i + 1]
                        i += 1
                elif arg == '-X':
                    # HTTP方法
                    if i + 1 < len(args):
                        method = args[i + 1].upper()
                        i += 1
                elif arg == '-H' or arg == '--header':
                    # 请求头
                    if i + 1 < len(args):
                        header_line = args[i + 1]
                        if ':' in header_line:
                            key, value = header_line.split(':', 1)
                            headers[key.strip()] = value.strip()
                        i += 1
                elif arg == '-d' or arg == '--data' or arg == '--data-raw':
                    # 请求数据
                    if i + 1 < len(args):
                        data = args[i + 1]
                        i += 1
                elif arg == '--data-urlencode':
                    # URL编码的数据
                    if i + 1 < len(args):
                        data = args[i + 1]
                        i += 1
                elif arg == '--form' or arg == '-F':
                    # 表单数据
                    if i + 1 < len(args):
                        form_data = args[i + 1]
                        if '=' in form_data:
                            key, value = form_data.split('=', 1)
                            if not data:
                                data = ''
                            if data:
                                data += '&'
                            data += f"{urllib.parse.quote(key)}={urllib.parse.quote(value)}"
                        i += 1
                elif arg.startswith('-') and not arg.startswith('--'):
                    # 单字符选项可能带参数
                    single_char_opts = ['d', 'H', 'X', 'F']
                    for opt in single_char_opts:
                        if arg.startswith(f'-{opt}') and len(arg) > 2:
                            # -d"data" 格式
                            param = arg[2:]
                            if opt == 'd':
                                data = param.strip('"\'')
                            elif opt == 'H':
                                if ':' in param:
                                    key, value = param.split(':', 1)
                                    headers[key.strip()] = value.strip()
                            elif opt == 'X':
                                method = param.upper()
                elif arg.startswith('--') and '=' in arg:
                    # 长选项带等号格式
                    if arg.startswith('--data='):
                        data = arg[7:].strip('"\'')
                    elif arg.startswith('--header='):
                        header_line = arg[9:].strip('"\'')
                        if ':' in header_line:
                            key, value = header_line.split(':', 1)
                            headers[key.strip()] = value.strip()

                i += 1

            # 如果没有找到URL，尝试从参数中提取
            if not url:
                for arg in args:
                    if not arg.startswith('-') and arg != 'curl' and ('http://' in arg or 'https://' in arg):
                        url = arg
                        break

            # 如果还是没有URL，尝试查找任何看起来像URL的参数
            if not url:
                for arg in args:
                    if not arg.startswith('-') and arg != 'curl' and '.' in arg and '/' in arg:
                        url = arg
                        break

            if not url:
                result['error'] = '无法从cURL命令中提取URL'
                return result

            # 确定协议和路径
            if url.startswith('http://') or url.startswith('https://'):
                # 完整URL
                parsed = urllib.parse.urlparse(url)
                path = parsed.path or '/'
                if parsed.query:
                    path += '?' + parsed.query
                if parsed.fragment:
                    path += '#' + parsed.fragment

                result['url'] = url
                result['path'] = path
            else:
                # 相对URL
                result['path'] = url
                result['url'] = url

            # 设置方法
            result['method'] = method

            # 自动设置Content-Type
            if data and not any(h.lower() == 'content-type' for h in headers.keys()):
                if data.startswith('{') or data.startswith('['):
                    headers['Content-Type'] = 'application/json'
                elif data.startswith('<'):
                    headers['Content-Type'] = 'application/xml'
                else:
                    headers['Content-Type'] = 'application/x-www-form-urlencoded'

            # 如果有数据但没有设置方法，自动设置为POST
            if data and method == 'GET':
                result['method'] = 'POST'

            # 添加请求头
            result['headers'] = headers

            # 设置请求体
            result['body'] = data

            result['success'] = True

        except Exception as e:
            result['error'] = f'cURL命令解析失败: {str(e)}'
            result['success'] = False

        return result

    @staticmethod
    def format_form_data(data: str) -> Dict[str, str]:
        """
        格式化表单数据

        Args:
            data: 表单数据字符串

        Returns:
            解析后的表单数据字典
        """
        result = {}

        try:
            # 解析URL编码的表单数据
            pairs = data.split('&')
            for pair in pairs:
                if '=' in pair:
                    key = urllib.parse.unquote(pair.split('=')[0])
                    value = urllib.parse.unquote(pair.split('=', 1)[1])
                    result[key] = value
                else:
                    result[pair] = ''
        except Exception:
            # 如果解析失败，返回原始数据
            result['raw'] = data

        return result

    @staticmethod
    def format_query_string(query: str) -> Dict[str, str]:
        """
        格式化查询字符串

        Args:
            query: 查询字符串

        Returns:
            解析后的查询参数字典
        """
        result = {}

        try:
            params = urllib.parse.parse_qs(query, keep_blank_values=True)
            for key, values in params.items():
                result[key] = values[0] if values else ''
        except Exception:
            # 如果解析失败，返回原始查询字符串
            result['raw'] = query

        return result


# 便捷函数
def parse_http_request(raw_request: str) -> Dict[str, any]:
    """
    解析HTTP请求的便捷函数

    Args:
        raw_request: 原始HTTP请求文本

    Returns:
        解析结果字典
    """
    return HTTPRequestParser.parse(raw_request)


def parse_curl_command(curl_command: str) -> Dict[str, any]:
    """
    解析cURL命令的便捷函数

    Args:
        curl_command: cURL命令字符串

    Returns:
        解析结果字典
    """
    return HTTPRequestParser.parse_curl_command(curl_command)
