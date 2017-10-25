import json
import argparse
try:
    from cookielib import Cookie, LWPCookieJar
except ImportError:
    from http.cookiejar import Cookie, LWPCookieJar


class EditThisCookieJsonFileException(Exception):
    pass


def main(arg):
    try:
        with open(arg.input, 'rt') as json_file:
            json_data = json.load(json_file)
    except:
        raise EditThisCookieJsonFileException

    cj = LWPCookieJar(arg.output)

    for cookie in json_data:
        version = cookie.get('version', 0)
        name = cookie.get('name')
        value = cookie.get('value')
        port = cookie.get('port')

        if port is None:
            port_specified = False
        else:
            port_specified = True

        domain = cookie.get('domain').lower()
        domain_specified = domain.startswith(".")
        domain_initial_dot = False

        if domain_specified:
            domain_initial_dot = bool(domain.startswith("."))

        path = cookie.get('path')

        if path != "":
            path_specified = True
        else:
            path_specified = False

        secure = cookie.get("secure", False)
        expires = cookie.get("expirationDate", None)
        discard = cookie.get("discard", False)
        comment = cookie.get("comment", None)
        comment_url = cookie.get("commenturl", None)
        rest = {
            'HttpOnly': cookie.get("httpOnly", None)
        }
        rfc2109 = False

        c = Cookie(version=version,
                   name=name,
                   value=value,
                   port=port,
                   port_specified=port_specified,
                   domain=domain,
                   domain_specified=domain_specified,
                   domain_initial_dot=domain_initial_dot,
                   path=path,
                   path_specified=path_specified,
                   secure=secure,
                   expires=expires,
                   discard=discard,
                   comment=comment,
                   comment_url=comment_url,
                   rest=rest,
                   rfc2109=rfc2109)
        cj.set_cookie(c)
        cj.save(ignore_discard=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert EditThisCookie to LWPCookieJar cookies file.'
    )
    parser.add_argument('-i', '--input-file',
                        help='EditThisCookie dumps json file.',
                        default='EditThisCookie.json'
                        )
    parser.add_argument('-o', '--output-file',
                        help='LWPCookieJar cookies file.',
                        default='LWPCookieJar.txt'
                        )
    arg = parser.parse_args()
    main(arg)
