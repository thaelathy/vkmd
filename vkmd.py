#-=-coding:utf-8-=-
import re
import os
import sys
import getopt
import logging
import time

import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TRCK, TIT2, TPE1, TALB, TDRC, TCON, COMM, ID3NoHeaderError

logging.basicConfig(filename='vkmd.log', level=logging.DEBUG)
logging.info('Started')

class VkAgent:
    def __init__(self, params):
        logging.debug('Getting main page')
        r = requests.get('http://m.vk.com/')
        url = re.findall(r'action="(.*?)"', r.text)[0]
        r = requests.post(url, params=params)
        self.headers = r.request.headers
        self.cookies = r.cookies

    def get(self, url):
        time.sleep(1)
        r = requests.get(url, headers=self.headers, cookies=self.cookies)
        return r.content
        
def main(email, passw, uid, folder=''):
    vk = VkAgent(params={"email": email, "pass": passw})
    try:
        data = vk.get("http://m.vk.com/audios%s" % uid)
        cnt = int(re.findall(r'<em class\="tab_counter">([0-9,]+)<\/em>', data)[0].replace(',', ''))
        logging.debug(cnt)
    except:
        logging.error("Can't count audios")
        exit()
    try:
        os.mkdir(folder)
        logging.debug('Created dir %s' % folder)
    except OSError:
        logging.error("Can't create dir, writing to .")
        pass
    for page in range(0, cnt, 50):
        logging.info(u"Offset %s" % page)
        data = vk.get("http://m.vk.com/audios%s?offset=%s" % (uid, page))
        data_list = data.split('<div class="ai_label">')[1:]
        for d in data_list:
            artist = re.findall(r'"ai_artist">(.*?)<\/span>', d)[0]
            title = re.findall(r'"ai_title">(.*?)<\/span>', d)[0]
            link = re.findall(r'<input type="hidden" value="(.*?)"', d)[0]
            
            fname = "%s - %s" % (artist, title)
            fname = fname.replace("/", " ").replace('&quot;', '"').replace('&gt;','>').replace('&lt;','<').replace('&amp;','&')[:200] + ".mp3"
            logging.info(u"Saving file")
            if not os.path.isfile(fname):
                f = open(folder + '/' + fname, 'wb')
                content = vk.get(link)
                f.write(content)
                f.close()
                logging.debug(u'Saved')
                logging.debug(u'Handling tags')
                try:
                    audio = MP3(folder + '/' + fname)
                    audio['TIT2'] = TIT2(encoding=3, text=[audio['TIT2'] if audio.get('TIT2') else title])
                    audio['TPE1'] = TPE1(encoding=3, text=[audio['TPE1'] if audio.get('TPE1') else artist])
                    audio['TRCK'] = TRCK(encoding=3, text=[audio['TRCK'] if audio.get('TRCK') else ''])
                    audio['TALB'] = TALB(encoding=3, text=[audio['TALB'] if audio.get('TALB') else ''])
                    audio.save()
                except Exception, e:
                    try:
                        audio = ID3(folder + '/' + fname)
                        audio.add(TIT2(encoding=3, text=[audio['TIT2'] if audio.get('TIT2') else title]))
                        audio.add(TPE1(encoding=3, text=[audio['TPE1'] if audio.get('TPE1') else artist]))
                        audio.add(TRCK(encoding=3, text=[audio['TRCK'] if audio.get('TRCK') else '']))
                        audio.add(TALB(encoding=3, text=[audio['TALB'] if audio.get('TALB') else '']))
                        audio.save()
                    except:
                        logging.error(u'Failed to write ID3 tags')
                logging.debug(u'Finished writing tags') 
                

            

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "u:p:i:f:", ["help", "output="])
    param = dict(opts)
    main(param['-u'], param['-p'], param['-i'], param['-f'])
