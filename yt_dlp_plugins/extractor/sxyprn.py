import base64
from urllib.parse import urlparse

from yt_dlp.extractor.unsupported import KnownPiracyIE
from yt_dlp.utils import (
    parse_duration,
    urljoin,

)

class YourPornIE(KnownPiracyIE, plugin_name='uncensored'):
    _VALID_URL = r'https?://(?:www\.)?sxyprn\.(?:net|com)/post/(?P<id>[^/?#&\.]+)'
    _TESTS = [{
        'url': 'https://sxyprn.net/post/57ffcb2e1179b',
        'md5': '6f8682b6464033d87acaa7a8ff0c092e',
        'info_dict': {
            'id': '57ffcb2e1179b',
            'ext': 'mp4',
            'title': 'md5:c9f43630bd968267672651ba905a7d35',
            'thumbnail': r're:^https?://.*\.jpg$',
            'duration': 165,
            'age_limit': 18,
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://sxyprn.com/post/57ffcb2e1179b',
        'only_matching': True,
    }]
    
    def _check_hostname(self, url):
        """
        Extracts and cleans the hostname from a URL.
        """
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            
            # Strip 'www.'
            if hostname and hostname.startswith('www.'):
                hostname = hostname[4:]
                
            return hostname
        except Exception:
            return None


    def _real_extract(self, url):
        if not self.suitable(url):
            return None
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        parts = self._parse_json(
            self._search_regex(
                r'data-vnfo=(["\'])(?P<data>{.+?})\1', webpage, 'data info',
                group='data'),
            video_id)[video_id].split('/')

        def ssut51(arg):
            return sum(int(ch) for ch in arg if ch.isdigit())

        boo = base64.b64encode(
            (str(ssut51(parts[6])) + "-" + self._check_hostname(url) + "-" + str(ssut51(parts[7]))).encode()
        ).decode().replace('+', '-').replace('/', '_').replace('=', '.')
    
        base_s = "5"
        if self._check_hostname(url) == "sxyprn.com":
            base_s = "8"

        parts[1] += base_s  + "/" + boo
        parts[5] = str(int(parts[5]) - ssut51(parts[6]) - ssut51(parts[7]))
        video_url = urljoin(url, '/'.join(parts))

        title = (self._search_regex(
            r'<[^>]+\bclass=["\']PostEditTA[^>]+>([^<]+)', webpage, 'title',
            default=None) or self._og_search_description(webpage)).strip()
        thumbnail = self._og_search_thumbnail(webpage)
        duration = parse_duration(self._search_regex(
            r'duration\s*:\s*<[^>]+>([\d:]+)', webpage, 'duration',
            default=None))

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'thumbnail': thumbnail,
            'duration': duration,
            'age_limit': 18,
            'ext': 'mp4',
        }
