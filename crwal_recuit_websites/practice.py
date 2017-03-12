#-*- coding:utf-8 -*-
import json
import textwrap
from bs4 import BeautifulSoup

# with open('zhilian_test.txt','r') as f:
#     all_info = f.read().encode('utf-8').decode('utf-8')
#     # all_info = f.read()
#
# all_info = json.loads(all_info)
# # print(all_info)
# a = all_info['zhilian1']
#
# for i,j in a.items():
#     print(i,':',j)

a = '''     <div class="tab-inner-cont">
                        <!-- SWSStringCutStart -->
                        <p>岗位职责</p><p>1. 根据用户的需求开发公司的前端系统 ;</p><p>2. 对负责模块进行单元测试；</p><p>3. 在能力范围内指导其他开发者；</p><p>4. 编写技术文档。</p><p>&nbsp;</p><p>岗位要求</p><p>1. 计算机及相关专业毕业，大学本科以及以上学历；</p><p>2. 出色的Python Web 应用开发能力；</p><p>3. 熟悉一种关系型数据库；</p><p><br/></p><p><br/></p><p>&nbsp;（薪资会根据经验做适当调整）</p>
                        <!-- SWSStringCutEnd -->

                        <b>工作地址：</b>
                        <h2>
                            上海浦东新区陆家嘴世纪金融广场

                        </h2>


                        <p>
                            <button id="applyVacButton1" class="button-small" title="申请职位" onclick="zlzp.searchjob.ajaxApplyBrig3('1');dyweTrackEvent('bjobsdetail14gb','directapply_middle');"></button>
                        </p>

                    </div>
'''

b = '''
<ul class="terminal-ul clearfix">
                <li><span>职位月薪：</span><strong>20001-30000元/月&nbsp;<a href="http://www.zhaopin.com/gz_shanghai/" target="_blank" title="上海工资计算器"><img src="http://jobs.zhaopin.com/images/calculator.png" alt="上海工资计算器" /></a></strong></li>
                <li><span>工作地点：</span><strong><a target="_blank" href="http://www.zhaopin.com/shanghai/">上海</a></strong></li>
                <li><span>发布日期：</span><strong><span id="span4freshdate">2017-03-10</span></strong></li>
                <li><span>工作性质：</span><strong>全职</strong></li>
                <li><span>工作经验：</span><strong>3-5年</strong></li>
                <li><span>最低学历：</span><strong>本科</strong></li>
                <li><span>招聘人数：</span><strong>1人 </strong></li>
                <li><span>职位类别：</span><strong><a target="_blank" href="http://jobs.zhaopin.com/shanghai/sj079/">软件研发工程师</a></strong></li>
            </ul>


'''

c = '''
  <div class="inner-left fl">
                <h1>Senior Python</h1>
                <h2><a onclick="recordOutboundLink(this, 'terminalpage', 'tocompanylink3');" href="http://company.zhaopin.com/CC246060339.htm" target="_blank">上海洛书投资管理有限公司</a></h2>
                <div style="width:683px;" class="welfare-tab-box"> <span>五险一金</span><span>年终分红</span><span>包吃</span><span>带薪年假</span><span>补充医疗保险</span><span>定期体检</span><span>员工旅游</span><span>节日福利</span> </div>
                <div class="lightspot"></div>
            </div>


'''

d = '''
            <div class="tab-inner-cont" style="display:none;word-wrap:break-word;">

                        <h5><a rel="nofollow" href="http://company.zhaopin.com/CC246060339.htm" onclick="recordOutboundLink(this, 'terminalpage', 'tocompanylink4');" target="_blank">上海洛书投资管理有限公司</a><a target="_blank" class="color-blue fr see-other-job" href="http://company.zhaopin.com/CC246060339.htm" rel="nofollow" onclick="recordOutboundLink(this, 'terminalpage', 'tocompanylink2');">该公司其他职位</a></h5>
                        <p>
                            <div style="TOP: 0px"><span style="FONT-SIZE: 10.5pt; FONT-FAMILY: 宋体; mso-ascii-font-family: 'Songti SC'; mso-hansi-font-family: 'Songti SC'; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA"><span style="FONT-SIZE: 10.5pt; FONT-FAMILY: 宋体; mso-ascii-font-family: 'Songti SC'; mso-hansi-font-family: 'Songti SC'; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA">上海洛书投资管理有限公司是一家具有全球化视野的数量化交易公司，</span>专注于量化交易系统和策略研发。创始人曾任职于华尔街顶级金融机构并拥有丰富的量化交易经验。公司总部设立于上海，并在世界主要的金融中心设有办公室或联系人。技术团队是公司最核心的部门，以开发高性能、稳定可靠的量化交易平台为己任，响应变化、敏捷开发和快速迭代；我们提倡专业高效的工作和平等直接的沟通，依靠团队协作，共同面对各种挑战。</span></div>
<p><span style="FONT-SIZE: 10.5pt; FONT-FAMILY: 宋体; mso-ascii-font-family: 'Songti SC'; mso-hansi-font-family: 'Songti SC'; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA">我们在如今飞速发展的金融市场中坚实成长，并创造性地将科技引入传统金融业，为产业革新作出贡献。我们致力于打造一个以团队协作、认真实干的企业环境。我们的核心价值是乐享工作，才智为先，互相尊重。</span></p>
<p><span style="FONT-SIZE: 10.5pt; FONT-FAMILY: 宋体; mso-ascii-font-family: 'Songti SC'; mso-hansi-font-family: 'Songti SC'; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA">我们诚邀愿意在上海发展的优秀人才加盟共同发展。</span></p>
                        </p>



                        <h3></h3>
                        <p>

                        </p>

                    </div>
                </div>
            </div>

            <div class="today_recommend">
                <ul class="tab-ul">
                    <li class="current">最新职位推荐</li>
                    <li>今日相似推荐</li>
                </ul>
            </div>


'''

e = '''
     <div class="company-box">

                <p class="company-name-t"><a rel="nofollow" href="http://company.zhaopin.com/CC246060339.htm" target="_blank">上海洛书投资管理有限公司</a></p>
                <ul class="terminal-ul clearfix terminal-company mt20">
                    <li><span>公司规模：</span><strong>20-99人</strong></li>
                    <li><span>公司性质：</span><strong>民营</strong></li>



                    <li><span>公司行业：</span><strong><a target="_blank" href="http://jobs.zhaopin.com/shanghai/in180000/">基金/证券/期货/投资</a></strong></li>

                    <li><span>公司主页：</span><strong><a rel="nofollow" href="http://www.luoshucapital.com/" target="_blank">http://www.luoshucapital.com/</a></strong></li>

                    <li>
                        <span>公司地址：</span><strong>
                            上海浦东新区陆家嘴世纪金融广场<br>

                        </strong>
                    </li>
                </ul>
                <!--是否是反馈通-->
                <input type="hidden" id="displayRegionScopeId" name="displayRegionScopeId" value="0" />
            </div>
            <div class="terminalpage-advertising">
                <ul id="job-advertising"></ul>
            </div>
        </div>
    </div>


'''

soup = BeautifulSoup(e,'lxml')
# soup_div = soup.find('div',class_='tab-inner-cont',style=False)
job_dict = {}

soup_ul_2 = soup.find('ul',class_="terminal-ul clearfix terminal-company mt20")
for li in soup_ul_2.find_all('li'):
    key = li.span.string
    value = li.strong.get_text().strip()
    job_dict[key] = value

print(job_dict)

# a = u'\u7537'
# print a
