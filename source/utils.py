class URLBuilder:

    def __init__(self,
                 protocol: str,
                 host: str,
                 port: str | int | None = None,
                 path: list[str] = []):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.path = path

    def _path(self) -> str:
        match len(self.path):
            case 0:
                return ''
            case _:
                if self.path[-1][-1] != '/':
                    return '/'.join(self.path) + '/'
                else:
                    return '/'.join(self.path)

    def _semicoloned_port(self) -> str | None:
        if self.port:
            return ':' + str(self.port)
        else:
            return str(self.port)

    def url(self):
        url_list = [self.protocol,
                    '://', self.host,
                    self._semicoloned_port(),
                    '/', self._path()]
        url = ''.join(url_list)
        return url


def split_and_concatenate(string: str) -> str:

    words = []
    prev = ''
    rev_string = string[::-1]
    temp = ''
    for i, letter in enumerate(rev_string):
        if i + 1 == len(string):
            temp += letter
            words.append(temp)
        elif not prev:
            temp += letter
        elif letter.islower() and prev.islower():
            temp += letter
        elif letter.isupper() and prev.islower():
            temp += letter
            words.append(temp)
            temp = ''
            prev = ''
            continue
        elif letter.islower() and prev.isupper():
            words.append(temp)
            temp = ''
            temp += letter
        elif letter.isupper() and prev.isupper():
            temp += letter
        prev = letter
    result = '_'.join(words).lower()[::-1]
    return result


assert split_and_concatenate('MFPNetwork') == 'mfp_network'
assert split_and_concatenate('MFP') == 'mfp'
assert split_and_concatenate('AAbCD') == 'a_ab_cd'
assert split_and_concatenate('AbBCd') == 'ab_b_cd'
assert split_and_concatenate('ABCdDDD') == 'ab_cd_ddd'
