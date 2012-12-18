#cofing=utf-8
from httptoolkit import HttpToolkit
import json
import time
def test():
    domain = "10.0.0.11:9100"
    while True:
        try:
            httptool = HttpToolkit()
            ids_url = "http://%s/photo/get-from-rr-ids" % domain
            res = httptool.get(ids_url)
            ids = json.loads(res)["data"]
            print ids
        
            for rr_id in ids:
                print rr_id, 
                url = "http://%s/photo/get-from-rr?rr_id=%d" % (domain, rr_id)
                res = httptool.get(url)
                print res
                if '"code": 0' not in res:
                    time.sleep(1)
        except Exception, e:
            print e
     
if __name__ == "__main__":
    test()