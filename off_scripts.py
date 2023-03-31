# -*- encoding=utf8 -*-
__author__ = "harperdelaviga"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report
from seo_utils import extract_to_be_test, AndroidPhone
import os


def main():

    # init airtest
    if not cli_setup():
        auto_setup(__file__, logdir=True, devices=["Android:///", ], project_root=os.path.dirname(os.path.realpath(__file__)))
    
    # get domains to be tested
    to_be_test = extract_to_be_test("seo_domain.ini")
    log(to_be_test)

    # print selected domains
    log('抽取出待測試的域名為:')
    for key, value in to_be_test.items():
        log(f"寫死域名: {key}")
        log(f"網址: {value}")


    # init AndroidPhone
    realme_narzo50i = AndroidPhone("seo_domain.ini")

    # test start
    success_list = []
    failure_list = []
    pending_list = []

    try:
        for domain in to_be_test:
            for url in to_be_test[domain]:
                log(f"測試網址: {url}")
                log(f"預期域名: {domain}")

                # open chrome with private mode
                realme_narzo50i.chrome_private_mode()

                # downloas and open landing page
                realme_narzo50i.chrome_download(url)

                # login if needed
                if exists(Template(r"tpl1669445067455.png", record_pos=(-0.224, -0.761), resolution=(720, 1600))):
                    realme_narzo50i.bty_login()

                # assert domain name
                realme_narzo50i.bty_get_domainname(url)
                try:
                    assert_equal(realme_narzo50i.image_to_string(url, domain), True, "断言写死域名")
                    success_list.append(url)
                except AssertionError:
                    log("写死域名不匹配")
                    failure_list.append(url)
                except:
                    log("未能执行")
                    pending_list.append(url)

                # close app and kill processes
                realme_narzo50i.kill_processes()

        log('所有测项已跑完，回到主页')
        home()

        log(f"成功清单： {success_list}")
        log(f"失败清单： {failure_list}")
        log(f"未完成清单： {pending_list}")
    except Exception as e:
        # handle exception
        log(f"发生异常：{str(e)}")
        simple_report(__file__, logpath=True)
    finally:
        # generate html report
        simple_report(__file__, logpath=True)

if __name__ == '__main__':
    main()